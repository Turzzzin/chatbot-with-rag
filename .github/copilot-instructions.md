# AI Coding Agent Instructions for Chatbot with RAG Backend API

Welcome to the `Chatbot with RAG` backend API codebase! This document provides essential guidelines for AI coding agents to be productive and aligned with the project's architecture, workflows, and conventions.

## Project Overview

This project is a REST API designed to provide medication information using Retrieval-Augmented Generation (RAG). It consists of:

- **API Server**: Python with FastAPI, handling the RAG pipeline and API endpoints.
- **Database**: ChromaDB for storing vector embeddings of medication data.
- **External Integration**: Perplexity AI's `sonar-pro` language model for generating responses.

### Key Data Flow
1. **Data Ingestion**: Medication data from `DADOS_ABERTOS_MEDICAMENTOS.csv` is processed and stored as embeddings in ChromaDB.
2. **Query Handling**: User queries trigger retrieval of relevant data from ChromaDB.
3. **Response Generation**: Retrieved data and user queries are sent to the language model for generating answers.

## Codebase Structure

- `app/`
  - `main.py`: Entry point for the FastAPI application.
  - `data/vectorstores/`: Stores ChromaDB files.
  - `models/schemas.py`: Defines data models and schemas.
  - `routes/`
    - `api_router.py`: Main API router.
    - `endpoints/`: Contains route handlers (e.g., `chat.py`).
  - `services/rag_service.py`: Implements the RAG pipeline logic.
  - `utils/`
    - `config.py`: Configuration management.
    - `logger.py`: Logging utilities.
- `notebooks/`: Jupyter notebooks for data preprocessing.

## Developer Workflows

### Running the Application
1. Ensure dependencies are installed (see `pyproject.toml`).
2. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```
3. Access the API documentation at `http://127.0.0.1:8000/docs`.

### Testing
- Tests are not explicitly defined in the current structure. Add tests under a `tests/` directory following Python's `unittest` or `pytest` conventions.

### Debugging
- Use the `logger.py` utility for consistent logging.
- Debug FastAPI endpoints using tools like Postman or cURL.

## Project-Specific Conventions

- **Data Handling**: Always preprocess medication data using the provided Jupyter notebooks before updating the ChromaDB vectorstore.
- **API Design**: Follow FastAPI's dependency injection pattern for shared resources.
- **API Endpoints**: All endpoints are prefixed with `/api` and follow RESTful conventions.
- **CORS**: Configure CORS settings appropriately based on your frontend application's needs.

## External Dependencies

- **ChromaDB**: Used for vector similarity search.
- **Perplexity AI**: External language model for generating responses.
- **LangChain**: Framework for orchestrating the RAG pipeline.

## Examples of Common Patterns

### Adding a New Endpoint
1. Create a new file in `routes/endpoints/` (e.g., `example.py`).
2. Define the route using FastAPI decorators:
   ```python
   from fastapi import APIRouter

   router = APIRouter()

   @router.get("/example")
   async def example_endpoint():
       return {"message": "Hello, World!"}
   ```
3. Include the new router in `api_router.py`.

### Updating the RAG Pipeline
- Modify `services/rag_service.py` to adjust retrieval or generation logic.
- Ensure changes are tested with relevant queries.

## Limitations and Warnings
- The chatbot does not provide medical advice or make assumptions beyond its dataset.
- Always include disclaimers in generated responses.

For further details, refer to the `README.md` file.
