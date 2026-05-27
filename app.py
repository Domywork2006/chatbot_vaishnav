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
# CUSTOM CSS
# =========================

st.markdown(
    """
    <style>

    /* Main App Background */
    .stApp {
        background-color: #050816;
        color: #E2E8F0;
    }

    /* Main Area */
    .main {
        background-color: #050816;
    }

    /* Title */
    h1 {
        color: #00FF9C;
        text-align: center;
        font-weight: 700;
        letter-spacing: 1px;
    }

    /* Caption */
    .stCaption {
        color: #7DD3FC;
        text-align: center;
    }

    /* Chat Messages */
    .stChatMessage {
        background-color: #0F172A;
        border: 1px solid #00FF9C;
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 12px;
        box-shadow: 0 0 12px rgba(0, 255, 156, 0.15);
    }

    /* User Icon */
    [data-testid="chatAvatarIcon-user"] {
        color: #00FF9C;
    }

    /* Assistant Icon */
    [data-testid="chatAvatarIcon-assistant"] {
        color: #38BDF8;
    }

    /* Chat Input */
    .stChatInput input {
        background-color: #0F172A !important;
        color: white !important;
        border: 1px solid #00FF9C !important;
        border-radius: 12px !important;
    }

    /* File Upload Box */
    section[data-testid="stFileUploader"] {
        background-color: #0F172A;
        border: 1px solid #38BDF8;
        border-radius: 12px;
        padding: 10px;
    }

    /* Expander */
    .streamlit-expanderHeader {
        color: #00FF9C !important;
        font-weight: bold;
    }

    /* Success Messages */
    .stAlert {
        background-color: #022C22;
        color: #00FF9C;
        border: 1px solid #00FF9C;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #020617;
    }

    ::-webkit-scrollbar-thumb {
        background: #00FF9C;
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# LOAD VECTOR DATABASE
# =========================

def load_vector_store():

    pages = []

    if os.path.exists(DOCS_PATH):

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


# =========================
# MAIN HEADER
# =========================

st.title("🤖 AI-Powered RAG Document Assistant")

st.caption(
    "Semantic Search + Groq AI + ChromaDB"
)


# =========================
# DOCUMENT UPLOAD
# =========================

st.markdown("### 📎 Add Documents")

uploaded_files = st.file_uploader(
    "",
    type=["pdf"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)


# =========================
# HANDLE PDF UPLOADS
# =========================

if uploaded_files:

    os.makedirs(DOCS_PATH, exist_ok=True)

    for uploaded_file in uploaded_files:

        save_path = os.path.join(
            DOCS_PATH,
            uploaded_file.name
        )

        with open(save_path, "wb") as f:

            f.write(uploaded_file.getbuffer())

    st.success(
        "PDF files uploaded successfully!"
    )


# =========================
# LOAD VECTOR STORE
# =========================

vector_store = load_vector_store()


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

    # Prompt
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

    # Generate Response
    with st.spinner("Thinking..."):

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

        # Source Chunks
        with st.expander("📄 Source Chunks"):

            for i, doc in enumerate(retrieved_docs):

                source_file = os.path.basename(
                    doc.metadata.get(
                        "source",
                        "Unknown"
                    )
                )

                page_number = doc.metadata.get(
                    "page",
                    "?"
                )

                st.markdown(
                    f"### 📄 {source_file} | Page {page_number}"
                )

                st.write(doc.page_content)

                st.markdown("---")