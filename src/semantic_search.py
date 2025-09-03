"""
semantic_search.py
Semantic search using FAISS + SentenceTransformers.

Features:
- Build FAISS index from processed files
- Save index + metadata for reuse
- Load index instantly if already built
"""

import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Paths
PROCESSED_DIR = "processed"
INDEX_PATH = os.path.join(PROCESSED_DIR, "faiss_index.bin")
META_PATH = os.path.join(PROCESSED_DIR, "metadata.pkl")

# Load embedding model
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)


# --------- Build Index ---------
def build_faiss_index():
    """Build FAISS index from processed text files."""
    texts, metadata = [], []

    for fname in os.listdir(PROCESSED_DIR):
        if fname.endswith(".txt") and fname != "file_categories.txt":
            fpath = os.path.join(PROCESSED_DIR, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()

            # Split text into chunks for better retrieval
            chunks = [content[i : i + 500] for i in range(0, len(content), 500)]
            texts.extend(chunks)
            metadata.extend([(fname, i) for i in range(len(chunks))])

    print(f"✅ Loaded {len(texts)} chunks from {len(metadata)} documents.")

    # Encode chunks
    embeddings = model.encode(texts, convert_to_numpy=True)

    # Build FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Save index + metadata
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump((texts, metadata), f)

    print(f"✅ FAISS index built & saved: {INDEX_PATH}")
    return index, texts, metadata


# --------- Load or Build Index ---------
def load_or_build_index():
    """Load FAISS index if available, else build it."""
    if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
        print("📂 Loading existing FAISS index...")
        index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, "rb") as f:
            texts, metadata = pickle.load(f)
        return index, texts, metadata
    else:
        print("⚡ No index found, building a new one...")
        return build_faiss_index()


# --------- Semantic Search ---------
def semantic_search(query, top_k=5):
    index, texts, metadata = load_or_build_index()

    # Encode query
    query_vec = model.encode([query], convert_to_numpy=True)
    D, I = index.search(query_vec, top_k)

    results = []
    for idx, score in zip(I[0], D[0]):
        if idx < len(texts):
            fname, chunk_id = metadata[idx]
            snippet = texts[idx][:200].replace("\n", " ")
            results.append((fname, snippet, score))
    return results


# --------- CLI Run ---------
if __name__ == "__main__":
    while True:
        query = input("\nEnter your query (or 'exit'): ").strip()
        if query.lower() == "exit":
            break
        results = semantic_search(query)
        if not results:
            print("❌ No matches found.")
        else:
            print(f"\n🔍 Top results for '{query}':\n")
            for fname, snippet, score in results:
                print(f"📄 {fname}  (score: {score:.4f})\n   ↪ {snippet}...\n")
