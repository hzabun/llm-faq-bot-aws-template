import logging
from pathlib import Path
from typing import List

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader, UnstructuredMarkdownLoader
from langchain_huggingface import HuggingFaceEmbeddings

logging.basicConfig(level=logging.INFO)


def load_documents_from_directory(directory_path: str) -> List[Document]:
    """Load all PDF and Markdown files from a directory."""
    directory = Path(directory_path)
    all_docs = []

    # Find all supported files
    for pattern in ["*.pdf", "*.md", "*.markdown"]:
        for file_path in directory.glob(pattern):
            try:
                if file_path.suffix.lower() == ".pdf":
                    loader = PyPDFLoader(str(file_path))
                else:
                    loader = UnstructuredMarkdownLoader(str(file_path), mode="elements")

                docs = loader.load()
                all_docs.extend(docs)
                logging.info(f"Loaded {len(docs)} documents from {file_path.name}")
            except Exception as e:
                logging.error(f"Error loading {file_path}: {e}")

    return all_docs


def initialize_vector_store(directory_path: str = "../documents/") -> Chroma:
    """Initialize vector store from all documents in directory."""
    # Load all documents
    docs = load_documents_from_directory(directory_path)

    if not docs:
        logging.error("No documents found")
        return None

    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
    )
    chunks = text_splitter.split_documents(docs)

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory="./chromadb_client",
    )

    logging.info(
        f"Vector store created with {len(chunks)} chunks from {len(docs)} documents"
    )
    return vectorstore
