import os

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "raw_pdfs")
DB_PATH = os.path.join(PROJECT_ROOT, "data", "chroma_db")


def _get_embedding_model() -> OllamaEmbeddings:
    return OllamaEmbeddings(model="nomic-embed-text")


def ingest_documents() -> tuple[int, int]:
    print(f"Loading PDFs from {DATA_PATH}...")
    loader = PyPDFDirectoryLoader(DATA_PATH)
    raw_documents = loader.load()
    print(f"Loaded {len(raw_documents)} pages.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(raw_documents)
    print(f"Split into {len(chunks)} chunks.")

    embedding_model = _get_embedding_model()

    print("Initializing Vector Store (this may take a few minutes for large PDFs)...")
    vector_db = Chroma(embedding_function=embedding_model, persist_directory=DB_PATH)

    batch_size = 100
    total_chunks = len(chunks)
    for i in range(0, total_chunks, batch_size):
        batch = chunks[i : i + batch_size]
        print(
            f"   > Processing batch {i // batch_size + 1} "
            f"of {(total_chunks - 1) // batch_size + 1} ({len(batch)} chunks)..."
        )
        vector_db.add_documents(batch)

    print("Vector Store created successfully.")
    return len(raw_documents), len(chunks)


def retrieve_documents(query: str, k: int = 4, keyword_filter: bool = True):
    """
    Retrieve documents using vector similarity and an optional keyword boost.
    """
    embedding_model = _get_embedding_model()
    vector_store = Chroma(persist_directory=DB_PATH, embedding_function=embedding_model)

    print(f"Searching for: '{query}'...")
    results = vector_store.similarity_search_with_score(query, k=k + 2)

    if not keyword_filter:
        return results[:k]

    query_terms = set(query.lower().split())
    final_results = []
    for doc, score in results:
        content = doc.page_content.lower()
        term_matches = sum(1 for term in query_terms if term in content)
        boosted_score = score - (term_matches * 0.05)
        final_results.append((doc, boosted_score))

    final_results.sort(key=lambda x: x[1])
    return final_results[:k]
