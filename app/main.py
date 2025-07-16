from contextlib import asynccontextmanager
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from google import genai
from langchain_chroma import Chroma
from langchain_integration import initialize_vector_store
from pydantic import BaseModel, Field

# Load environment variables for Gemini API key
load_dotenv("../secrets.env")

client = genai.Client()


class VectorStoreManager:
    """Manages the vector store instance."""

    def __init__(self):
        self._vectorstore: Chroma = None

    def initialize(self, directory_path: str = "../documents/"):
        self._vectorstore = initialize_vector_store(directory_path)
        if self._vectorstore is None:
            raise RuntimeError("Failed to initialize vector store")

    def get_vectorstore(self) -> Chroma:
        if self._vectorstore is None:
            raise RuntimeError("Vector store not initialized")
        return self._vectorstore

    def is_initialized(self) -> bool:
        return self._vectorstore is not None


vector_store_manager = VectorStoreManager()


class QueryRequest(BaseModel):
    """Request model for /ask endpoint."""

    prompt: str = Field(min_length=1, description="The prompt to send to Gemini")


class QueryResponse(BaseModel):
    """Response model for /ask endpoint."""

    response: str


# Dependency to get the vector store instance
def get_vector_store() -> Chroma:
    return vector_store_manager.get_vectorstore()


# Lifespan event handler to initialize resources at startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    vector_store_manager.initialize("../documents/")
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"Hello": "World"}


@app.post("/ask", response_model=QueryResponse)
def ask_gemini(
    query: QueryRequest, vectorstore: Annotated[Chroma, Depends(get_vector_store)]
):
    """
    Endpoint to send a prompt to Gemini using context from the vector store.

    Args:
        query: QueryRequest containing the user's prompt
        vectorstore: Vector store instance injected via dependency

    Returns:
        QueryResponse with the generated response from Gemini

    Raises:
        HTTPException: 500 if there's an error processing the request
    """
    try:
        # Retrieve relevant context chunks from the vector store
        results = vectorstore.similarity_search(query.prompt, k=3)

        # Extract content from the results
        context_chunks = [result.page_content for result in results]
        context = "\n".join(context_chunks)

        # Construct the full prompt for the Gemini model
        full_prompt = f"Context:\n{context}\n\nQuestion: {query.prompt}"

        # Generate response from Gemini model
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=full_prompt
        )
        return {"response": response.text}
    except Exception as e:
        # Log the error and return a 500 error response
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "vector_store_initialized": vector_store_manager.is_initialized(),
    }
