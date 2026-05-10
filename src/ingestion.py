import os

from vector_store import DATA_PATH, ingest_documents

if __name__ == "__main__":
    # Ensure directory exists
    os.makedirs(DATA_PATH, exist_ok=True)
    
    # Create a dummy PDF if none exists (for testing)
    if not os.path.exists(DATA_PATH) or not os.listdir(DATA_PATH):
        print(f"No PDFs found in {DATA_PATH}. Please add files to enable RAG features.")
    else:
        ingest_documents()