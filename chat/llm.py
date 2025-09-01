import os
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from .vectorstore import load_or_create_faiss

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
LLM_REPO_ID = os.getenv("LLM_REPO_ID", "mistralai/Mixtral-8x7B-Instruct-v0.1")

def get_llm():
    # Hosted inference endpoint
    return HuggingFaceEndpoint(
        repo_id=LLM_REPO_ID,
        task="text-generation",
        temperature=0.2,
        max_new_tokens=512,
        repetition_penalty=1.1,
        huggingfacehub_api_token=HF_API_TOKEN,
    )

DISCLAIMER = (
    "Important: I am an AI medical assistant providing general information. "
    "I do not provide diagnosis, prescriptions, or medical treatment. "
    "If this is an emergency, call local emergency services immediately."
)

SYSTEM_POLICY = (
    "You are a cautious medical information assistant. "
    "Scope: general health education, symptom understanding, lifestyle guidance, risk awareness. "
    "Avoid diagnosis, drug names, dosages, or treatment plans. Encourage seeking professional care. "
    "Be concise, empathetic, and evidence‑oriented. Use plain language."
)

def build_chain():
    db = load_or_create_faiss()
    retriever = db.as_retriever(search_kwargs={"k": 4})

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_POLICY + " " + DISCLAIMER + " Use retrieved context when relevant."),
        MessagesPlaceholder("history"),
        ("human", "{question}"),
        ("system", "Relevant context:\n{context}\nIf context is not helpful, say so briefly."),
    ])

    llm = get_llm()
    parser = StrOutputParser()

    retrieval = {"context": retriever, "question": RunnablePassthrough(), "history": RunnablePassthrough()}

    chain = RunnableParallel(**retrieval) | prompt | llm | parser
    return chain, retriever
