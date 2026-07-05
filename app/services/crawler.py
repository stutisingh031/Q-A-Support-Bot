from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.services.rag_engine import vector_db

def ingest_website(url: str):
    # Load website content
    loader = WebBaseLoader(url)
    docs = loader.load()
    
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=100
    )
    splits = text_splitter.split_documents(docs)
    
    # Add to Vector DB
    vector_db.add_documents(documents=splits)
    return len(splits)