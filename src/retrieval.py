from vector_store import retrieve_documents

# --- Test Block ---
if __name__ == "__main__":
    # Test query
    test_query = "What is the impact of GenAI on productivity?"
    
    retrieved_docs = retrieve_documents(test_query)
    
    print(f"\n--- Top {len(retrieved_docs)} Results ---")
    for i, (doc, score) in enumerate(retrieved_docs):
        print(f"\n[Result {i+1}] (Score: {score:.4f})")
        print(f"Source: {doc.metadata.get('source', 'Unknown')}")
        print(f"Content Snippet: {doc.page_content[:200]}...")