import chromadb
import pymupdf  # imports the pymupdf library
import textwrap
import nltk

nltk.download("punkt_tab")
from nltk.tokenize import sent_tokenize

import logging

logging.basicConfig(level=logging.INFO)

# setup Chroma in-memory, for easy prototyping
client = chromadb.Client()

collection = client.create_collection("sample-collection")

chunk_size = 500  # number of characters per chunk


def semantic_chunk_text(text, max_tokens=500):
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


doc = pymupdf.open("documents/calypso_paper.pdf")
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

# query most similar results
results = collection.query(
    query_texts=["What prompt engineering methods are used in CALYPSO?"],
    n_results=3,
)

print(results)
