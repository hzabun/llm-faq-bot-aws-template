from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai
from pydantic import BaseModel, Field
from vector_store import initialize_vector_store, query_vector_store

# Load environment variables from .env file (for Gemini API key)
load_dotenv("../secrets.env")

# Initialize Gemini client
client = genai.Client()


class QueryRequest(BaseModel):
    """Request model for /ask endpoint."""

    prompt: str = Field(..., min_length=1, description="The prompt to send to Gemini")


class QueryResponse(BaseModel):
    """Response model for /ask endpoint."""

    response: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler to initialize resources at startup."""
    initialize_vector_store()  # Initialize vector store at startup
    yield


# Create FastAPI app with lifespan handler
app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"Hello": "World"}


@app.post("/ask", response_model=QueryResponse)
def ask_gemini(query: QueryRequest):
    """
    Endpoint to send a prompt to Gemini using context from the vector store.

    Args:
        query: QueryRequest containing the user's prompt

    Returns:
        QueryResponse with the generated response from Gemini

    Raises:
        HTTPException: 500 if there's an error processing the request
    """
    try:
        # Retrieve relevant context chunks from the vector store
        context_chunks = query_vector_store(query.prompt, n_results=3)
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
