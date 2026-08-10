import os

from app.ingestion.document_loader import load_document
from app.ingestion.chunker import split_documents
from app.ingestion.indexer import (
    add_documents,
    delete_document,
)
from app.ingestion.document_registry import (
    calculate_file_hash,
    get_document,
    register_document,
)


def process_document(file_path):
    """
    Add or update a document in the knowledge base.

    Returns:
        {
            "status": "added" | "updated" | "unchanged",
            "filename": str,
            "chunks": int
        }
    """

    filename = os.path.basename(file_path)

    # --------------------------------------------------------
    # 1. Calculate current file hash
    # --------------------------------------------------------

    file_hash = calculate_file_hash(
        file_path
    )

    # --------------------------------------------------------
    # 2. Check registry
    # --------------------------------------------------------

    existing_document = get_document(
        filename
    )

    # --------------------------------------------------------
    # 3. DOCUMENT ALREADY EXISTS
    # --------------------------------------------------------

    if existing_document:

        old_hash = existing_document.get(
            "file_hash"
        )

        # Same content → nothing to do
        if old_hash == file_hash:

            return {
                "status": "unchanged",
                "filename": filename,
                "chunks": existing_document.get(
                    "chunk_count",
                    0
                ),
            }

        # ----------------------------------------------------
        # Content changed → update
        # ----------------------------------------------------

        old_document_id = old_hash

        # Remove old chunks from Chroma
        delete_document(
            old_document_id
        )

        document_id = file_hash

        # Load document
        documents = load_document(
            file_path
        )

        # Create chunks with NEW document ID
        chunks = split_documents(
            documents,
            document_id=document_id,
        )

        # Add new chunks
        add_documents(
            chunks
        )

        # Update registry
        register_document(
            filename=filename,
            file_hash=file_hash,
            chunk_count=len(chunks),
        )

        return {
            "status": "updated",
            "filename": filename,
            "chunks": len(chunks),
        }

    # --------------------------------------------------------
    # 4. NEW DOCUMENT
    # --------------------------------------------------------

    document_id = file_hash

    # Load document
    documents = load_document(
        file_path
    )

    # Chunk + attach document ID
    chunks = split_documents(
        documents,
        document_id=document_id,
    )

    # Add to existing Chroma
    add_documents(
        chunks
    )

    # Register document
    register_document(
        filename=filename,
        file_hash=file_hash,
        chunk_count=len(chunks),
    )

    return {
        "status": "added",
        "filename": filename,
        "chunks": len(chunks),
    }