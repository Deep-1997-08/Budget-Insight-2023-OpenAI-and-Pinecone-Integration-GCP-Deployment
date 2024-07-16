from flask import Flask, request, jsonify, render_template
import openai
import pinecone
import pdfplumber
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import PineconeVectorStore
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.schema import Document
from langchain.chains.question_answering import load_qa_chain
import os

app = Flask(__name__)
load_dotenv('.env')

openai_api = os.getenv('OPENAI_API_KEY')
pinecone_api = os.getenv('PINECONE_API_KEY')
pinecone_host = os.getenv('PINECONE_HOST')
index_name = "pinecone-chatbot"

openai.api_key = openai_api

@app.route('/')
def index():
    return render_template('index.html')

def read_doc(file_path):
    documents = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            documents.append(Document(page_content=page.extract_text(), metadata={'source': file_path}))
    return documents

def chunk_data(docs, chunk_size=800, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    doc = text_splitter.split_documents(docs)
    return doc

@app.route('/process', methods=['POST'])
def process_documents():
    file_path = 'data/budget_speech.pdf'
    documents = read_doc(file_path)
    chunked_documents = chunk_data(documents)
    
    embeddings = OpenAIEmbeddings(api_key=openai_api)
    vectorstore = PineconeVectorStore.from_documents(chunked_documents, embeddings, index_name=index_name)
    
    from pinecone import Pinecone
    pc = Pinecone(api_key=pinecone_api)
    index = pc.Index(index_name)

    vectors = [
        {"id": str(doc.id), "values": [float(x) for x in embeddings.embed_query(doc.page_content)], "metadata": doc.metadata}
        for doc in chunked_documents
    ]
    index.upsert(vectors=vectors, index_name=index_name)
    
    return f"Documents processed and vectors upserted. Vectors count: {len(vectors)}"

@app.route('/query', methods=['POST'])
def query_vectorstore():
    query = request.form['query']
    if not query:
        return "No query provided", 400
    
    embeddings = OpenAIEmbeddings(api_key=openai_api)
    query_vector = embeddings.embed_query(query)
    
    from pinecone import Pinecone
    pc = Pinecone(api_key=pinecone_api)
    index = pc.Index(index_name)

    matching_results = index.query(vector=query_vector, top_k=2, include_metadata=True)
    
    llm = OpenAI(api_key=openai_api, model_name="gpt-3.5-turbo", temperature=0.5)
    chain = load_qa_chain(llm, chain_type="stuff")
    response = chain.run(input_documents=matching_results, question=query)
    
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
