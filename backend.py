from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load env
load_dotenv()

# LangChain
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.documents import Document

# ---------------- INIT ----------------
app = FastAPI()

GROQ_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_KEY:
    raise ValueError("❌ GROQ_API_KEY not found!")

chat_model = ChatGroq(
    model_name="llama-3.1-8b-instant",
    groq_api_key=GROQ_KEY.strip(),
    temperature=0
)

embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

DB_PATH = "faiss_index_store"
PDF_DIR = "data"

# ---------------- CREATE / LOAD INDEX ----------------
def load_or_create_index():
    if os.path.exists(DB_PATH):
        print("✅ Loading existing FAISS index...")
        return FAISS.load_local(
            DB_PATH,
            embedder,
            allow_dangerous_deserialization=True
        )

    print("⚡ Creating FAISS index...")

    if not os.path.exists(PDF_DIR):
        os.makedirs(PDF_DIR)
        print("📂 'data' folder created. Add PDFs and restart.")
        exit()

    all_docs = []

    files = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]

    if not files:
        print("❌ No PDFs found in data folder.")
        exit()

    for file in files:
        reader = PdfReader(os.path.join(PDF_DIR, file))
        text = ""

        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150
        )

        chunks = splitter.split_text(text)

        for chunk in chunks:
            all_docs.append(Document(page_content=chunk))

    vectorstore = FAISS.from_documents(all_docs, embedder)
    vectorstore.save_local(DB_PATH)

    print("✅ FAISS index created!")

    return vectorstore

vectorstore = load_or_create_index()

# ---------------- REQUEST ----------------
class QueryRequest(BaseModel):
    query: str

# ---------------- ROUTES ----------------
@app.get("/")
def home():
    return {"message": "Backend running 🚀"}

@app.post("/ask")
def ask_question(request: QueryRequest):
    print("🔥 API HIT")

    query = request.query

    docs = vectorstore.similarity_search(query, k=5)
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
    SYSTEM: You are a cybersecurity expert.
    Answer ONLY from the context.

    CONTEXT:
    {context}

    QUESTION:
    {query}
    """

    try:
        response = chat_model.invoke(prompt)

        return {
            "answer": response.content
        }

    except Exception as e:
        return {
            "error": str(e)
        }