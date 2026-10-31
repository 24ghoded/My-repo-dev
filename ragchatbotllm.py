import streamlit as st
import os 
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import ollama

import streamlit as st

st.set_page_config(page_title="C++ RAG Chatbot")
st.title("C++ RAG Chatbot")
st.success("Streamlit is working!")
st.write("Testing the application interface...")

#------------
# page config
#------------
st.title("C++ RAG Chatbot using ollama LLM")

#-----------
# load and process data
#-----------

def load_vectorstore():
    # Load Document
    loader = TextLoader("CPP.txt", encoding="utf-8")
    documents = loader.load()

    # Split Text
    textSplitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20
    )

    finalDocuments = textSplitter.split_documents(documents)

    # Embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    # Create FAISS vector database
    db = FAISS.from_documents(finalDocuments, embeddings)

    return db

db = load_vectorstore()

#load the LLM model
llm = ollama.Ollama(model="gemma2:2b")

#------------------
# chat interface
#------------------

user_question = st.text_input("Ask any questions related to C++ introduction")

if user_question:
    with st.spinner("Searching for relevant context..."):
        docs = db.similarity_search(user_question, k=3)
        context = "\n".join([doc.page_content for doc in docs])

        prompt = f"""
You are a helpful assistant that answers questions about C++ introduction. Use the following context to answer the question. If the answer is not in the context, say "I don't know".

context:
{context}

question: {user_question}

answer:


        """
        response = llm.invoke(prompt)
        st.subheader("Answer")
        st.write(response)