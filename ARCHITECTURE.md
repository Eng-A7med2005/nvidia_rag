# System Architecture

## Overview

The Smart Contract Assistant v2 is a Retrieval-Augmented Generation (RAG) system designed to provide accurate answers from legal documents. It combines document ingestion, vector storage, and an LLM-powered chat interface.

## Components

### 1. Ingestion Pipeline
The ingestion process transforms raw documents into a searchable vector index.

*   **Loaders**: The system supports multiple file types:
    *   `PyMuPDFLoader` for **PDFs**.
    *   `TextLoader` for **text files**.
    *   `UnstructuredFileLoader` for **other formats** (e.g., DOCX).
*   **Chunking**: Documents are split into manageable chunks using `RecursiveCharacterTextSplitter`:
    *   **Chunk Size**: 1000 characters.
    *   **Overlap**: 200 characters to maintain context across boundaries.
*   **Embeddings**: Text chunks are converted into vector representations using `OpenAIEmbeddings` (model: `text-embedding-3-small`).
*   **Storage**: Vectors are stored in a local **FAISS** index for efficient similarity search.

### 2. Retrieval & Generation (RAG)
The core logic for answering questions involves retrieving relevant context and generating a response.

*   **Retrieval**: Given a user query, the system retrieves the top **4** most similar document chunks from the FAISS index.
*   **Prompting**: A `ChatPromptTemplate` instructs the LLM to act as an expert legal assistant.
*   **Generation**: The `ChatOpenAI` model (gpt-4o-mini) generates an answer based on the retrieved context.
*   **Citations**: The system tracks source metadata (filename, page number) and appends it to the final response.

### 3. API Layer (Microservice)
The project includes an auto-generated `server.py` that exposes the RAG chain as a REST API.

*   **Framework**: Built with **FastAPI**.
*   **Integration**: Uses **LangServe** (`add_routes`) to create standard endpoints.
*   **Endpoints**:
    *   `/contract-assistant/invoke`: Execute the chain.
    *   `/contract-assistant/batch`: Batch processing.
    *   `/contract-assistant/stream`: Streaming responses.
    *   `/contract-assistant/playground`: Interactive playground UI.

### 4. Frontend (Gradio)
A user-friendly web interface created with **Gradio**.

*   **Ingestion Tab**: Upload files and trigger the ingestion pipeline.
*   **Chat Tab**: conversational interface for querying the documents.
*   **Local API Tab**: Quick reference for running the backend server.

## Data Flow

1.  **User Upload**: User uploads documents -> Ingestion Pipeline processes them -> Vector Store updated.
2.  **User Query**: User asks a question -> Query embedded -> Vector Store searched -> Context retrieved.
3.  **LLM Processing**: Context + Query sent to LLM -> Answer generated -> Response returned with sources.

## Technologies Used

*   **LangChain**: Orchestrator for LLM chains and tools.
*   **OpenAI**: Embeddings and Language Models.
*   **FAISS**: Vector Database.
*   **FastAPI**: Backend Web Framework.
*   **Gradio**: Frontend UI Library.
