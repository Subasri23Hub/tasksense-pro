"""
build_vectorstore.py — Run this once to build the FAISS vector store.
Usage: python build_vectorstore.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from core.retriever import build_vectorstore

if __name__ == "__main__":
    print("Building vector store from productivity knowledge base...")
    try:
        vs = build_vectorstore()
        print("✅ Vector store built and saved to /vectorstore/faiss_index")
    except Exception as e:
        print(f"❌ Failed: {e}")
        print("Make sure your GOOGLE_API_KEY is set in the .env file.")
