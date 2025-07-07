from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai
from pydantic import BaseModel, Field

app = FastAPI()

# Load gemini API key
load_dotenv("../secrets.env")

# Initialize Gemini client
client = genai.Client()


class QueryRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="The prompt to send to Gemini")


class QueryResponse(BaseModel):
    response: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


# Send prompt to query the model
@app.post("/ask", response_model=QueryResponse)
def ask_gemini(query: QueryRequest):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=query.prompt
        )
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
