import os, glob
from markdownify import markdownify as md
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from .vectorstore import get_embeddings

def ingest_docs(input_dir="data/medical_docs/", index_path="data/faiss"):
    os.makedirs(input_dir, exist_ok=True)
    files = glob.glob(os.path.join(input_dir, "**/*.*"), recursive=True)
    docs = []
    for f in files:
        try:
            if f.lower().endswith((".txt", ".md",)):
                text = open(f, "r", encoding="utf-8").read()
            else:
                # naive HTML to text fallback
                text = md(open(f, "r", encoding="utf-8", errors="ignore").read())
            if text.strip():  # ✅ avoid empty docs
                docs.append(text)
        except Exception as e:
                print(f"⚠️ Skipping {f}: {e}")
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    splits = []
    for d in docs:
        for chunk in splitter.split_text(d):
            splits.append(chunk)

        if not splits:
            print("⚠️ No text found in documents. Using placeholder.")
            splits = ["General health information placeholder."]
    embeddings = get_embeddings()
    vs = FAISS.from_texts(splits, embeddings)
    os.makedirs(index_path, exist_ok=True)
    vs.save_local(index_path)
    print(f"✅ Ingestion complete. {len(splits)} chunks saved in {index_path}")
    return len(splits)
    
if __name__ == "__main__":
    ingest_docs()
