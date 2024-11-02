import os
import streamlit as st
import pickle
import time
from langchain_core.documents import Document
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader


from langchain_groq.chat_models import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from dotenv import load_dotenv
load_dotenv()


def load_url_data(urls: list[str]) -> list[Document]:

    # Load data from a list of URLs using UnstructuredURLLoader.
    loader = UnstructuredURLLoader(urls=urls)
    documents = loader.load()

    return documents

def create_chunks(documents: list[Document]) -> list[Document]:
    # Split documents into smaller chunks for better retrieval
    text_splitter = RecursiveCharacterTextSplitter(separators=['\n\n', '\n', '.', ','],
                                                   chunk_size=1000, 
                                                   chunk_overlap=20)
    chunks = text_splitter.split_documents(documents)

    return chunks

def create_vectorstore(chunks: list[Document]) -> FAISS:

    # Define the Hugging Face Embeddings
    model_name = "BAAI/bge-small-en"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)

    # Create a FAISS vectorstore for efficient search
    vectorstore = FAISS.from_documents(documents=chunks, embedding=embeddings)

    return vectorstore

def save_vectorstore(vectorstore: FAISS, filepath: str) -> None:
    # Save the vectorstore to a pickle file
    with open(filepath, 'wb') as f:
        pickle.dump(vectorstore, f)
        
def load_vectorstore(filepath: str) -> FAISS:
    # Check if the vectorstore exists in the pickle file
    if os.path.exists(filepath):
        # Load the vectorstore from the pickle file
        with open(filepath, 'rb') as f:
            vectorstore = pickle.load(f)
        return vectorstore
    else:
        return None

def get_retrieval_chain(vectorstore_filepath: str) -> RetrievalQAWithSourcesChain:

    llm = ChatGroq(model="llama-3.1-70b-versatile",
                      stop_sequences="[end]")

    if os.path.exists(vectorstore_filepath):
        # Load the vectorstore from the pickle file
        with open(vectorstore_filepath, 'rb') as f:
            vectorstore = pickle.load(f)
            chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, 
                                                         retriever=vectorstore.as_retriever())
            return chain
    
    return None

def get_answer_and_source(question: str, chain: RetrievalQAWithSourcesChain) -> dict:
    # Get the answer using the retrieval chain
    result = chain.invoke({"question": question}, return_only_outputs=True)
    
    answer = result['answer']
    source = result.get("sources", "")

    output_dict = {'answer': answer,'source': source}

    # If no answer found, return a message
    if not answer:
        output_dict["answer"] = "No answer found. Please check the question and try again."

    return output_dict