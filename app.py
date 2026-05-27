import streamlit as st
from groq import Groq
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

import os


# =========================
# LOAD ENVIRONMENT VARIABLES
# =========================

load_dotenv()


# =========================
# CONFIGURATION
# =========================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

DOCS_PATH = "docs"

CHROMA_DB_PATH = "chroma_db"

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 50

TOP_K = 5

MODEL_NAME = "llama-3.1-8b-instant"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# =========================
# PAGE CONFIGURATION
# =========================

st.set_page_config(
    page_title="AI RAG Assistant",
    page_icon="🤖",
    layout="wide"
)


# =========================
# LOAD VECTOR DATABASE
# =========================

@st.cache_resource
def load_vector_store():

    pages = []

    for file in os.listdir(DOCS_PATH):

        if file.endswith(".pdf"):

            loader = PyPDFLoader(
                f"{DOCS_PATH}/{file}"
            )

            pages.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(pages)

    embedding_model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=CHROMA_DB_PATH
    )

    return vector_store


vector_store = load_vector_store()


# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.title("🤖 AI RAG Assistant")

    st.markdown("---")

    st.markdown("### Features")

    st.markdown("""
    - Multi PDF Support
    - Semantic Search
    - ChromaDB Vector Store
    - Conversational Memory
    - Groq LLM Integration
    - Source Chunk Retrieval
    """)

    st.markdown("---")

    st.markdown("### Model")

    st.code(MODEL_NAME)


# =========================
# MAIN TITLE
# =========================

st.title("🤖 AI-Powered RAG Document Assistant")

st.caption(
    "Ask questions from your PDF documents using semantic search and Groq AI."
)


# =========================
# SESSION MEMORY
# =========================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =========================
# DISPLAY CHAT HISTORY
# =========================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# =========================
# CHAT INPUT
# =========================

prompt = st.chat_input(
    "Ask a question about your documents..."
)


# =========================
# PROCESS USER INPUT
# =========================

if prompt:

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Display user message
    with st.chat_message("user"):

        st.markdown(prompt)

    # Retrieve relevant chunks
    retrieved_docs = vector_store.similarity_search(
        prompt,
        k=TOP_K
    )

    # Build context
    context = "\n\n".join(
        [doc.page_content for doc in retrieved_docs]
    )

    # Build conversation history
    history_text = ""

    for msg in st.session_state.messages[-6:]:

        history_text += (
            f"{msg['role']}: {msg['content']}\n"
        )

    # Create Groq client
    client = Groq(
        api_key=GROQ_API_KEY
    )

    # Prompt messages
    messages = [
        {
            "role": "system",
            "content": (
                "You are an intelligent AI assistant. "
                "Answer ONLY using the provided context. "
                "Use conversation history when necessary. "
                "If the answer is not found in the context, "
                "say: 'I could not find that in the document.'"
            )
        },
        {
            "role": "user",
            "content": f"""
Conversation History:
{history_text}

Context:
{context}

Question:
{prompt}

Answer:
"""
        }
    ]

    # Generate response
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.2,
        max_tokens=512
    )

    answer = response.choices[0].message.content

    # Store assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    # Display assistant response
    with st.chat_message("assistant"):

        st.markdown(answer)

        # Show source chunks
        with st.expander("📄 Source Chunks"):

            for i, doc in enumerate(retrieved_docs):

                st.markdown(
                    f"### Chunk {i + 1}"
                )

                st.write(doc.page_content)

                st.markdown("---")
