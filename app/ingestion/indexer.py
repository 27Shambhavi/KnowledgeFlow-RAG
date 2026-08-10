from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.config import (
    GOOGLE_API_KEY,
    VECTORSTORE_DIR,
)


# ============================================================
# EMBEDDINGS
# ============================================================

def get_embeddings():
    """
    Create the Google Gemini embedding model.
    """

    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY,
    )


# ============================================================
# VECTOR STORE
# ============================================================

def get_vectorstore():
    """
    Connect to the existing Chroma vector database.
    """

    embeddings = get_embeddings()

    vectorstore = Chroma(
        collection_name="rag_documents",
        embedding_function=embeddings,
        persist_directory=VECTORSTORE_DIR,
    )

    return vectorstore


# ============================================================
# ADD DOCUMENTS
# ============================================================

def add_documents(chunks):
    """
    Add new document chunks to the existing
    Chroma vector database.

    Existing documents are NOT deleted.
    """

    vectorstore = get_vectorstore()

    if not chunks:
        return vectorstore

    vectorstore.add_documents(
        chunks
    )

    return vectorstore


# ============================================================
# DELETE DOCUMENT
# ============================================================

def delete_document(document_id):
    """
    Delete all chunks belonging to a specific
    document from Chroma.

    Each chunk must contain:

        metadata["document_id"]
    """

    vectorstore = get_vectorstore()

    collection = vectorstore._collection

    collection.delete(
        where={
            "document_id": document_id
        }
    )

    return vectorstore


# ============================================================
# UPDATE DOCUMENT
# ============================================================

def update_document(
    document_id,
    chunks,
):
    """
    Replace an existing document in Chroma.

    Process:

        Old chunks
             ↓
        Delete them
             ↓
        New chunks
             ↓
        Add them
    """

    vectorstore = get_vectorstore()

    # --------------------------------------------------------
    # Remove old chunks
    # --------------------------------------------------------

    collection = vectorstore._collection

    collection.delete(
        where={
            "document_id": document_id
        }
    )

    # --------------------------------------------------------
    # Add new chunks
    # --------------------------------------------------------

    if chunks:

        vectorstore.add_documents(
            chunks
        )

    return vectorstore