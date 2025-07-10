import logging

import chromadb
import nltk
import pymupdf  # PDF processing library
from nltk.tokenize import sent_tokenize

# Download NLTK sentence tokenizer if not already present
nltk.download("punkt_tab")

logging.basicConfig(level=logging.INFO)

# Setup Chroma persistent client for vector storage
client = chromadb.PersistentClient(path="./chromadb_client")
collection = client.get_or_create_collection("sample-collection")
chunk_size = 500  # Number of characters per chunk


def semantic_chunk_text(text, max_tokens=500):
    """
    Split text into chunks of approximately max_tokens characters,
    using sentence boundaries for better semantic coherence.
    """
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_tokens:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


def initialize_vector_store(pdf_path="../documents/calypso_paper.pdf"):
    """
    Initialize the vector store by loading and chunking a given PDF document.
    Skips initialization if already populated.
    """
    if collection.count() > 0:
        logging.info("Vector store already initialized.")
        return

    doc = pymupdf.open(pdf_path)
    chunk_id = 1
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        chunks = semantic_chunk_text(text, chunk_size)
        for chunk in chunks:
            clean_chunk = chunk.replace("\n", " ").strip()
            collection.add(
                documents=[clean_chunk],
                ids=[f"id{chunk_id}"],
                metadatas=[{"page": page_num}],
            )
            logging.info(f"Added chunk {chunk_id} from page {page_num}")
            chunk_id += 1
    logging.info("Vector store initialized.")


def query_vector_store(query, n_results=3):
    """
    Query the vector store for the most semantically similar document chunks.

    Args:
        query (str): The search query text
        n_results (int): Number of results to return (default: 3)

    Returns:
        list[str]: List of document chunks most similar to the query
    """
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
    )
    return results["documents"][0] if results and "documents" in results else []
