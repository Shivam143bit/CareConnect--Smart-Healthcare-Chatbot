from langchain_community.vectorstores import FAISS
from .vectorstore import get_embeddings

def query_docs(question: str, k: int = 2):
    # Load existing FAISS index
    db = FAISS.load_local("data/faiss", get_embeddings(), allow_dangerous_deserialization=True)
    
    # Perform similarity search
    docs = db.similarity_search(question, k=k)
    return [d.page_content for d in docs]


if __name__ == "__main__":
    # Example usage
    q = "What is asthma?"
    results = query_docs(q)
    for r in results:
        print(r)
