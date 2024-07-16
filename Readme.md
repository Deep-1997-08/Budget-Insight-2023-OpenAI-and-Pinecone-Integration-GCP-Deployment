# Budget Insight 2023: OpenAI and Pinecone Integration, GCP Deployment

Budget Insight 2023 is an advanced web application designed to provide in-depth analysis and insights into the Government of India's Budget for 2023-2024. This project leverages cutting-edge technologies including OpenAI for natural language processing, Pinecone for vector storage, and is deployed on Google Cloud Platform (GCP) for scalable and reliable access.

## Project Overview

The primary goal of this project is to facilitate easy querying and detailed analysis of the budget document. Users can submit queries related to the budget, and the system will provide relevant insights using advanced language models and vector search capabilities.

## Technologies Used

- **Python**: The core programming language used for backend development.
- **Flask**: A lightweight web framework used to build the web application.
- **OpenAI**: Utilized for natural language processing and generating responses to user queries.
- **Pinecone**: A vector database service used for storing and querying vectorized representations of the budget document.
- **pdfplumber**: A library for extracting text from PDF documents.
- **langchain**: A library used for document processing and integrating with Pinecone.
- **Docker**: Containerization technology used to package the application for deployment.
- **Google Cloud Platform (GCP)**: The cloud service provider used for hosting the application.
  - **Cloud Run**: A managed compute platform for running containerized applications.
  - **Google Container Registry**: For storing Docker images.

## Key Features

- **Advanced Querying**: Users can ask detailed questions about the budget, and the system will provide accurate and relevant answers.
- **Scalable Deployment**: The application is deployed on GCP, ensuring it can handle multiple requests efficiently.
- **Automated Processing**: The budget document is automatically processed and vectorized for quick and efficient querying.

## File Structure

- **main.py**: The main Flask application file containing the backend logic.
- **templates/**
  - **index.html**: The main HTML file for the web interface.
- **static/css/**
  - **styles.css**: The CSS file for styling the web interface.
- **requirements.txt**: Lists the Python dependencies required for the project.
- **Dockerfile**: Contains instructions to build the Docker image for the application.
- **app.yaml**: Configuration file for deploying the application on GCP.
- **.env**: Environment variables file (not included in version control).

## Deployment

The application is containerized using Docker and deployed on Google Cloud Platform's Cloud Run for scalable and managed hosting.

## Usage

1. **Query the Budget**: Enter your query in the input field on the main page and receive detailed insights from the budget document.


