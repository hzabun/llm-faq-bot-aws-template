from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai
from pydantic import BaseModel, Field
from vector_store import initialize_vector_store, query_vector_store

# Load gemini API key
load_dotenv("../secrets.env")

# Initialize Gemini client
client = genai.Client()


class QueryRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="The prompt to send to Gemini")


class QueryResponse(BaseModel):
    response: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_vector_store()  # Initialize vector store at startup
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}


# Send prompt to query the model
@app.post("/ask", response_model=QueryResponse)
def ask_gemini(query: QueryRequest):
    try:
        context_chunks = query_vector_store(query.prompt, n_results=3)
        context = "\n".join(context_chunks)

        full_prompt = f"Context:\n{context}\n\nQuestion: {query.prompt}"

        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=full_prompt
        )
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
