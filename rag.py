from groq import Groq
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os

load_dotenv()

# Settings
GROQ_API_KEY  = os.getenv("GROQ_API_KEY")
PDF_PATH      = "docs/notes1.pdf"
CHUNK_SIZE    = 1000
CHUNK_OVERLAP = 50
TOP_K         = 5
MODEL         ="llama-3.1-8b-instant"


def load_pdf():
    loader = PyPDFLoader(PDF_PATH)
    pages  = loader.load()
    print(f"Pages loaded: {len(pages)}")
    return pages


def split_chunks(pages):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size    = CHUNK_SIZE,
        chunk_overlap = CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(pages)
    print(f"Chunks created: {len(chunks)}")
    return chunks


def build_vector_store(chunks):
    print("Loading embedding model...")
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    print("Storing in ChromaDB...")
    vector_store = Chroma.from_documents(
        documents         = chunks,
        embedding         = embedding_model,
        persist_directory = "chroma_db"
    )
    print(f"Done! {len(chunks)} chunks stored.")
    return vector_store

def retrieve_chunks(vector_store, question):
    results = vector_store.similarity_search(question, k=TOP_K)
    print("\nRetrieved chunks:")
    print("-" * 40)
    for i, doc in enumerate(results):
        print(f"Chunk {i+1} | Page {doc.metadata.get('page','?')}")
        print(doc.page_content)
        print("-" * 40)
    return results

def get_answer(question, results):
    client  = Groq(api_key=GROQ_API_KEY)
    context = "\n\n".join([doc.page_content for doc in results])
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Answer using ONLY the context provided. If the answer is not in the context say 'I could not find that in the document.'"
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}"
        }
    ]
    response = client.chat.completions.create(
        model       = MODEL,
        messages    = messages,
        temperature = 0.2,
        max_tokens  = 512
    )
    return response.choices[0].message.content


def main():
    print("=== RAG Chatbot ===\n")

    pages        = load_pdf()
    chunks       = split_chunks(pages)
    vector_store = build_vector_store(chunks)

    print("\nReady! Ask questions about your PDF.")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()

        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        results = retrieve_chunks(vector_store, question)
        answer  = get_answer(question, results)

        print(f"\nAnswer: {answer}\n")
        print("-" * 40)


main()