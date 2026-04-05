import streamlit as st
import requests

st.set_page_config(page_title="Groq RAG Bot", page_icon="⚡")

st.title("⚡ Groq Cybersecurity RAG Bot")

API_URL = "http://127.0.0.1:8000/ask"

query = st.text_input("Ask a cybersecurity question:")

def ask_backend(query):
    try:
        response = requests.post(API_URL, json={"query": query})

        print("RAW RESPONSE:", response.text)

        if response.status_code == 200:
            data = response.json()
            return data.get("answer", "No answer found")
        else:
            return f"❌ Error: {response.status_code}"

    except Exception as e:
        return f"⚠️ Backend not running: {str(e)}"

if st.button("Generate"):
    if query:
        with st.spinner("Thinking..."):
            answer = ask_backend(query)

            st.subheader("💡 Answer")
            st.write(answer)