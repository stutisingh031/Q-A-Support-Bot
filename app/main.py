from fastapi import FastAPI
from pydantic import BaseModel
from app.services.rag_engine import get_answer, vector_db
from app.services.crawler import ingest_website
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

class IngestRequest(BaseModel):
    url: str

@app.post("/ingest")
async def ingest_site(request: IngestRequest):
    num_chunks = ingest_website(request.url)
    return {"message": f"Successfully ingested {num_chunks} chunks from {request.url}"}

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    retriever = vector_db.as_retriever()
    docs = retriever.invoke(request.question)
    answer = get_answer(request.question)
    return {
        "answer": answer,
        "raw_chunks": [
            {"content": doc.page_content, "metadata": doc.metadata} 
            for doc in docs
        ]
    }