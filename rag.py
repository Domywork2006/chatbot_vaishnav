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
# LOAD PDF DOCUMENTS
# =========================

def load_pdfs():

    pages = []

    print("\n" + "=" * 60)
    print("LOADING PDF DOCUMENTS")
    print("=" * 60 + "\n")

    for file in os.listdir(DOCS_PATH):

        if file.endswith(".pdf"):

            print(f"[INFO] Loading PDF: {file}")

            loader = PyPDFLoader(f"{DOCS_PATH}/{file}")

            pages.extend(loader.load())

    print(f"\n[SUCCESS] Total pages loaded: {len(pages)}\n")

    return pages


# =========================
# SPLIT DOCUMENTS INTO CHUNKS
# =========================

def split_chunks(pages):

    print("=" * 60)
    print("SPLITTING DOCUMENTS INTO CHUNKS")
    print("=" * 60)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(pages)

    print(f"\n[SUCCESS] Created {len(chunks)} chunks\n")

    return chunks


# =========================
# BUILD VECTOR DATABASE
# =========================

def build_vector_store(chunks):

    print("=" * 60)
    print("CREATING VECTOR DATABASE")
    print("=" * 60)

    print("\n[INFO] Loading embedding model...")

    embedding_model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    print("[INFO] Creating ChromaDB vector store...")

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=CHROMA_DB_PATH
    )

    print(f"\n[SUCCESS] Stored {len(chunks)} chunks in ChromaDB\n")

    return vector_store


# =========================
# RETRIEVE RELEVANT CHUNKS
# =========================

def retrieve_chunks(vector_store, question):

    results = vector_store.similarity_search(
        question,
        k=TOP_K
    )

    print("\n" + "=" * 60)
    print("RETRIEVED SOURCE CHUNKS")
    print("=" * 60)

    for i, doc in enumerate(results):

        print(f"\n[Chunk {i + 1}] | Page: {doc.metadata.get('page', '?')}\n")

        print(doc.page_content)

        print("\n" + "-" * 60)

    return results


# =========================
# GENERATE FINAL ANSWER
# =========================

def get_answer(question, results, chat_history):

    client = Groq(api_key=GROQ_API_KEY)

    context = "\n\n".join(
        [doc.page_content for doc in results]
    )

    history_text = ""

    for chat in chat_history[-3:]:

        history_text += f"{chat['role']}: {chat['content']}\n"

    messages = [
        {
            "role": "system",
            "content": (
                "You are an intelligent AI assistant. "
                "Answer ONLY using the provided context. "
                "Use conversation history when necessary. "
                "Do not make up information. "
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
{question}

Answer:
"""
        }
    ]

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.2,
        max_tokens=512
    )

    return response.choices[0].message.content


# =========================
# MAIN APPLICATION
# =========================

def main():

    print("\n" + "=" * 60)
    print("AI POWERED RAG DOCUMENT ASSISTANT")
    print("=" * 60)

    pages = load_pdfs()

    chunks = split_chunks(pages)

    vector_store = build_vector_store(chunks)

    print("=" * 60)
    print("SYSTEM READY")
    print("=" * 60)

    print("\nAsk questions about your PDF documents.")
    print("Type 'exit' or 'quit' to stop.\n")

    chat_history = []

    while True:

        question = input("You: ").strip()

        if not question:
            continue

        if question.lower() in {"exit", "quit"}:

            print("\nGoodbye!\n")

            break

        results = retrieve_chunks(
            vector_store,
            question
        )

        answer = get_answer(
            question,
            results,
            chat_history
        )

        print("\n" + "=" * 60)
        print("FINAL ANSWER")
        print("=" * 60)

        print(f"\n{answer}\n")

        chat_history.append({
            "role": "user",
            "content": question
        })

        chat_history.append({
            "role": "assistant",
            "content": answer
        })


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":
    main()