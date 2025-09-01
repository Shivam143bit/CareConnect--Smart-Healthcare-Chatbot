# CareConnect – Smart Healthcare Chatbot

## Overview
CareConnect is an AI-powered medical chatbot designed to assist users with general healthcare queries in a safe, interactive, and user-friendly manner. The chatbot does not provide medical prescriptions but offers reliable health-related information by leveraging NLP, RAG (Retrieval-Augmented Generation), and secure web technologies.

## How It Works

### 1. Document Ingestion & Knowledge Base
All healthcare-related documents, guidelines, and medical knowledge sources are stored in a folder (medical_docs).

These documents are pre-processed and split into chunks using LangChain’s RecursiveCharacterTextSplitter.

Each chunk is converted into vector embeddings via OpenAI Embeddings.

The embeddings are indexed and stored in FAISS (Facebook AI Similarity Search) to enable fast semantic search.

### 2.User Interaction (Frontend)
The user interacts through a chat interface (chat.html).

Queries are sent securely via AJAX requests with CSRF protection (X-CSRFToken).

The frontend dynamically displays both user messages and chatbot responses.

### 3. Backend Processing (Django + REST Framework)
The query hits a Django REST API endpoint.

The backend fetches the most relevant information from FAISS using semantic similarity.

If required, the query is further passed to an LLM (OpenAI GPT) for generating a natural, conversational response.

The chatbot ensures contextual relevance by storing chat history (sessions & messages) in a database.

### 4. Response Delivery
The chatbot returns the answer to the frontend in JSON format.

The frontend updates the chat UI instantly, providing a smooth, human-like interaction.

## Technologies Used

### Backend: Python, Django, Django REST Framework
### Frontend: HTML, CSS, JavaScript (with CSRF-secure AJAX calls)
### AI & NLP: LangChain, OpenAI Embeddings, FAISS Vector Database
### Database: PostgreSQL (for chat sessions & messages)
### Security: CSRF protection, secure API endpoints
### Deployment Ready: AWS / Heroku with scalability in mind

## Key Features

### AI-Powered Responses – Provides health-related information using RAG (Retrieval-Augmented Generation) for accuracy.
### Document Knowledge Base – Uses medical text files converted into embeddings for domain-specific answers.
### Secure & Reliable – CSRF protection, structured APIs, and Django security features.
### Interactive Chat UI – Real-time chatbox with clean UI, mimicking human-like conversations.
### Context-Aware Sessions – Stores chat history per user session for better conversational flow.
### Scalable & Extensible – Can be expanded to integrate voice assistants, mobile apps, or telemedicine platforms.

## Impact

CareConnect demonstrates how AI and web technologies can combine to build intelligent healthcare assistants. It showcases real-time natural language processing, secure API design, and scalable backend development, making it a perfect blend of AI + Full-Stack + Cloud.
