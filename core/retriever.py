import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

VECTORSTORE_PATH = Path(__file__).parent.parent / "vectorstore" / "faiss_index"
KNOWLEDGE_PATH = Path(__file__).parent.parent / "data" / "productivity_knowledge.txt"


def get_embeddings():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is missing in your .env file.")

    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key,
    )


def build_vectorstore():
    """Build and persist the FAISS vector store from knowledge base."""
    if not KNOWLEDGE_PATH.exists():
        raise FileNotFoundError(f"Knowledge file not found: {KNOWLEDGE_PATH}")

    with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
        raw_text = f.read().strip()

    if not raw_text:
        raise ValueError("Knowledge base file is empty.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " "],
    )

    chunks = splitter.split_text(raw_text)
    docs = [Document(page_content=chunk) for chunk in chunks]

    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)

    VECTORSTORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(VECTORSTORE_PATH))

    return vectorstore


def get_retriever(k: int = 4):
    """Load or build the retriever."""
    embeddings = get_embeddings()

    if VECTORSTORE_PATH.exists():
        vectorstore = FAISS.load_local(
            str(VECTORSTORE_PATH),
            embeddings,
            allow_dangerous_deserialization=True,
        )
    else:
        vectorstore = build_vectorstore()

    return vectorstore.as_retriever(search_kwargs={"k": k})


def retrieve_context(query: str, k: int = 4) -> str:
    """Retrieve relevant productivity knowledge for a query."""
    retriever = get_retriever(k=k)

    docs = retriever.invoke(query)

    if not docs:
        return "No relevant productivity context found."

    return "\n\n".join(doc.page_content for doc in docs)