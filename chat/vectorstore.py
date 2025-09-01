import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

EMBEDDING_REPO_ID = os.getenv("EMBEDDING_REPO_ID", "sentence-transformers/all-MiniLM-L6-v2")

def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_REPO_ID)

def load_or_create_faiss(index_path="data/faiss"):
    embeddings = get_embeddings()
    if os.path.isdir(index_path):
        return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    else:
        os.makedirs(index_path, exist_ok=True)
        # start empty; ingest later
        return FAISS.from_texts(["This is a placeholder. Ingest medical documents."], embeddings)
