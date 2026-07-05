import os
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
# from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
# 1. Initialize the Embedding Model (Free/Local)
# This will download the model (~80MB) on the first run
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 2. Setup Vector Database (Local Persistence)
DB_DIR = "./data/chroma_db"
vector_db = Chroma(
    persist_directory=DB_DIR, 
    embedding_function=embeddings,
    collection_name="support_collection"
)

# 3. Initialize the LLM (OpenAI)
if not api_key:
    print("❌ ERROR: OPENAI_API_KEY not found in environment!")
else:
    print(f"✅ OpenAI Key detected: {api_key[:8]}***")

llm = ChatOpenAI(
    model="gpt-4o-mini", 
    temperature=0.3,
    api_key=api_key  # Passing it explicitly
)
# 4. Define the RAG Prompt
template = """
You are a helpful support bot. Use the following context to answer the user's question.
If the answer is not in the context, say "I'm sorry, I don't have that information in my records."
Do not make up answers.

Context:
{context}

Question: 
{question}
"""
prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# 5. The RAG Chain
rag_chain = (
    {"context": vector_db.as_retriever() | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

def get_answer(query: str):
    """Function to be called by the FastAPI endpoint"""
    return rag_chain.invoke(query)