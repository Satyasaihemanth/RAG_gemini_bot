# 🤖 RAG Chatbot using LangChain

## 📌 Overview
This project implements a Retrieval-Augmented Generation (RAG) chatbot using LangChain and FAISS.

## 🚀 Features
- Document-based Q&A
- Semantic search using FAISS
- Context-aware responses

## 🛠 Tech Stack
- Python
- LangChain
- FAISS
- LLM API (OpenAI / Gemini)

## 📂 Project Structure
- backend.py → API logic
- chatbot.py → Chat interface
- data/ → Source documents

## ⚙️ How to Run

1. Install dependencies:
pip install -r requirements.txt

2. Add API key:
Create `.env` file:
API_KEY=your_key_here

3. Run chatbot:
python chatbot.py

## 📌 Note
FAISS index and embeddings are not included. Generate locally.
