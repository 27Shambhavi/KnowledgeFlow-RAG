from langchain_text_splitters import RecursiveCharacterTextSplitter


from app.config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)


def split_documents(
    documents,
    document_id=None,
):
    """
    Split loaded documents into smaller chunks.

    Each generated chunk can optionally receive
    a document_id in its metadata.

    The document_id allows us to identify and
    update/delete all chunks belonging to the
    same source document.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    chunks = splitter.split_documents(
        documents
    )

    # --------------------------------------------------------
    # ATTACH DOCUMENT ID
    # --------------------------------------------------------

    if document_id is not None:

        for chunk in chunks:

            if chunk.metadata is None:
                chunk.metadata = {}

            chunk.metadata[
                "document_id"
            ] = document_id

    return chunks