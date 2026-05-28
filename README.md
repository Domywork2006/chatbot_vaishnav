# 🤖 AI Chatbot & RAG Document Assistant

This repository contains both:

* **Task 1 — Basic AI Chat System**
* **Task 2 — RAG AI Document Assistant**

Built using Groq, LangChain, ChromaDB, HuggingFace Embeddings, and Streamlit.

---

# 📂 Project Structure

```bash
chatbot_vaishnav/
│
├── docs/                     # PDF documents
├── screenshots/              # Project screenshots
├── presentation/             # Project presentation slides
├── logs/                     # Application logs
├── chroma_db/                # Persistent vector database
│
├── chat.py                   # Task 1 chatbot
├── rag.py                    # Task 2 terminal RAG chatbot
├── app.py                    # Streamlit UI for RAG system
│
├── requirements.txt
├── README.md
├── .env
├── .gitignore
```

---

# ✅ Task 1 — Basic AI Chat System

## Objective

Build a simple AI chatbot using the Groq API.

---

## Features Implemented

* Multi-turn chatbot
* Conversation memory
* Groq API integration
* System prompts
* Adjustable temperature and max tokens
* Terminal-based interaction

---

## Technologies Used

* Python
* Groq API

---

## Model Used

```python
llama3-8b-8192
```

---

## How Task 1 Works

1. User enters a message
2. Message is stored in conversation history
3. Full conversation history is sent to Groq API
4. Model generates contextual response
5. AI response is stored for future conversation memory

---

## Run Task 1

```bash
python chat.py
```

---

# ✅ Task 2 — RAG AI Document Assistant

## Objective

Enhance the chatbot using Retrieval-Augmented Generation (RAG) so it can answer questions from uploaded PDF documents instead of relying only on pretrained model knowledge.

---

# 🚀 Task 2 Features

## Core RAG Features

* PDF document loading
* Semantic document retrieval
* Context-aware AI responses
* ChromaDB vector database integration
* HuggingFace embeddings
* Groq LLM integration
* Document chunking using LangChain
* Retrieval-Augmented Generation (RAG)

---

## Advanced Features Implemented

* ✅ Multi-PDF Support
* ✅ Conversational Chat Memory
* ✅ Streamlit Web Interface
* ✅ Frontend PDF Upload
* ✅ Source Chunk Display
* ✅ Source File Name + Page Number Tracking
* ✅ ChromaDB Local Persistence
* ✅ Logging System
* ✅ Dark Futuristic UI Theme
* ✅ With vs Without RAG Comparison
* ✅ Semantic Search-Based Retrieval

---

# 🛠 Technologies Used

| Technology  | Purpose                |
| ----------- | ---------------------- |
| Groq        | AI response generation |
| LangChain   | RAG workflow           |
| ChromaDB    | Vector database        |
| HuggingFace | Embedding generation   |
| Streamlit   | Web interface          |
| Python      | Backend development    |

---

## Models Used

### LLM

```python
llama-3.1-8b-instant
```

### Embedding Model

```python
all-MiniLM-L6-v2
```

---

# ⚙️ How Task 2 Works

## Step 1 — Upload or Load PDFs

The system loads PDF documents using LangChain's `PyPDFLoader`.

Users can:

* Upload PDFs directly from the Streamlit UI
* Store PDFs inside the `docs/` folder

---

## Step 2 — Split Documents into Chunks

Documents are divided into smaller chunks using:

```python
chunk_size = 500
chunk_overlap = 50
```

---

## Step 3 — Generate Embeddings

The embedding model:

```python
all-MiniLM-L6-v2
```

converts document chunks into vector embeddings.

---

## Step 4 — Store in ChromaDB

Embeddings and chunks are stored inside ChromaDB for semantic similarity search.

---

## Step 5 — Semantic Retrieval

When a user asks a question:

1. The question is converted into embeddings
2. ChromaDB retrieves the most relevant chunks
3. Top matching chunks are used as context

---

## Step 6 — Generate AI Response

The retrieved context and user question are sent to the Groq LLM.

The AI generates a document-aware response using the retrieved chunks.

---

# 🧠 Conversational Memory

The chatbot stores previous conversations during the session.

Example:

```text
User: What is deep learning?
User: Explain it simply.
User: Give an example.
```

---

# 🌐 Streamlit Web Interface

The project includes a Streamlit-based web UI with:

* PDF upload support
* Source chunk display
* Real-time AI responses
* Multi-document retrieval


---

# ▶️ Run Task 2

## Terminal-Based RAG Chatbot

```bash
python rag.py
```

---

## Streamlit Web Interface

```bash
streamlit run app.py
```

---

# 📊 Comparison — With vs Without RAG

## Without RAG (`chat.py`)

The chatbot answers using only pretrained model knowledge.

Responses are:

* General
* Non-document-specific
* Possible hallucinations

---

## With RAG (`rag.py` / `app.py`)

The chatbot retrieves relevant chunks from uploaded PDF documents before generating answers.

Responses become:

* More accurate
* Context-aware
* Document-specific
* Better grounded in source material

---

# 📝 Logging System

Logs are stored inside:

```bash
logs/rag.log
```

Logs include:

* User questions
* Retrieved chunks
* AI responses
* Errors

---


* Streamlit homepage
* PDF upload interface
* AI-generated responses
* Source chunk display
* Multi-document retrieval
* Conversational memory demo
* Dark futuristic UI

---

# ⚠️ Challenges Faced

* Choosing optimal chunk size
* Managing retrieval relevance
* Handling dynamic PDF uploads
* Preventing hallucinations
* Improving conversational context
* Balancing UI responsiveness and retrieval speed

---

# 🔮 Possible Improvements

* Hybrid Retrieval (Semantic + Lexical Search)
* Better caching system
* Incremental vector indexing
* Streaming AI responses
* Support for DOCX/Text files
* Voice input integration
* Cloud deployment
