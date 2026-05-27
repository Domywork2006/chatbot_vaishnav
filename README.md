# 🤖 AI-Powered RAG Document Assistant

An advanced Retrieval-Augmented Generation (RAG) based AI chatbot built using Groq, LangChain, ChromaDB, HuggingFace Embeddings, and Streamlit.

This system allows users to upload PDF documents and ask intelligent questions based on the uploaded content instead of relying only on the pretrained knowledge of the LLM.

---

# 🚀 Features

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

# 🛠 Tech Stack

## Backend

* Python
* LangChain
* ChromaDB
* Streamlit
* Groq API
* HuggingFace Embeddings

---

## Models Used

### LLM

`llama-3.1-8b-instant`

### Embedding Model

`all-MiniLM-L6-v2`

---

# 📂 Project Structure

```bash
chatbot_vaishnav/
│
├── docs/                     # PDF documents
├── screenshots/              # Project screenshots
├── logs/                     # Application logs
├── chroma_db/                # Persistent vector database
│
├── app.py                    # Streamlit RAG UI
├── rag.py                    # Terminal-based RAG chatbot
├── chat.py                   # Basic Groq chatbot
│
├── requirements.txt
├── README.md
├── .env
├── .gitignore
```

---

# ⚙️ How the RAG System Works

## Step 1 — Upload or Load PDFs

The system loads PDF documents using LangChain's `PyPDFLoader`.

Users can:

* Upload PDFs directly from the Streamlit UI
* Store PDFs inside the `docs/` folder

---

## Step 2 — Split Documents into Chunks

Documents are divided into smaller chunks using:

```python
chunk_size = 1000
chunk_overlap = 50
```

This improves retrieval quality and semantic matching.

---

## Step 3 — Generate Embeddings

The embedding model:

```python
all-MiniLM-L6-v2
```

converts document chunks into vector embeddings.

These embeddings capture semantic meaning.

---

## Step 4 — Store in ChromaDB

The embeddings and chunks are stored inside:

```python
ChromaDB
```

for fast semantic similarity search.

---

## Step 5 — Semantic Retrieval

When a user asks a question:

1. The question is converted into embeddings
2. ChromaDB retrieves the most relevant chunks
3. Top matching chunks are selected as context

---

## Step 6 — Generate AI Response

The retrieved chunks and user question are sent to the Groq LLM:

```python
llama-3.1-8b-instant
```

The AI generates a context-aware answer using only the retrieved document content.

---

# 🧠 Conversational Memory

The chatbot stores previous conversations during the session.

This allows:

* Follow-up questions
* Context-aware conversations
* Better user interaction

Example:

```text
User: What is deep learning?
User: Explain it simply.
User: Give an example.
```

---

# 🌐 Streamlit Web Interface

The project includes a modern Streamlit UI with:

git add README.md
* Frontend PDF upload support
* Source chunk display
* Real-time AI responses
* Multi-document retrieval

---

# ▶️ Installation Guide

## 1. Clone Repository

```bash
git clone https://github.com/Domywork2006/chatbot_vaishnav.git
cd chatbot_vaishnav
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Add Groq API Key

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

---

# ▶️ Running the Applications

## Run Terminal-Based RAG Chatbot

```bash
python rag.py
```

---

## Run Streamlit Web UI

```bash
streamlit run app.py
```

---

# 📄 Example Questions

* What is deep learning?
* Explain neural networks.
* Summarize the document.
* What topics are discussed?
* Explain the conclusion.
* What is semantic search?

---

# 📊 Comparison: With vs Without RAG

## Without RAG (`chat.py`)

The chatbot answers using only the pretrained knowledge of the LLM.

Responses are:

* General
* Non-document-specific
* Possible hallucinations

---

## With RAG (`rag.py` / `app.py`)

The system retrieves relevant chunks from uploaded PDF documents using semantic search.

Responses become:

* Context-aware
* More accurate
* Document-specific
* Better grounded in source material

---

## Example Observation

### Question

```text
What is deep learning?
```

### Without RAG

* General explanation from pretrained model knowledge.

### With RAG

* Answer generated using retrieved PDF content related to deep learning.

---

# 📝 Logging System

The application stores logs inside:

```bash
logs/rag.log
```

Logs include:

* User questions
* Retrieved chunks
* AI responses
* Errors



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
* Advanced reranking
* Support for DOCX/Text files
* Voice input integration
* Cloud deployment

---

# 📚 Learning Outcomes

This project helped in understanding:

* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Vector Databases
* Embeddings
* LangChain Pipelines
* Context-Aware AI Systems
* Streamlit Frontend Development
* Groq LLM Integration
* Multi-document Retrieval
* Conversational AI Systems

---

