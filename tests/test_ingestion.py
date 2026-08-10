from app.ingestion.document_loader import load_document
from app.ingestion.chunker import split_documents
from app.ingestion.indexer import add_documents


FILE_PATH = "data/uploads/Dummy-Bank-Statement.pdf"


def main():
    # 1. Load document
    documents = load_document(FILE_PATH)

    print(f"Loaded documents: {len(documents)}")

    # 2. Split into chunks
    chunks = split_documents(documents)

    print(f"Created chunks: {len(chunks)}")

    # 3. Add chunks to vector database
    vectorstore = add_documents(chunks)

    print("Documents successfully added to Chroma.")


if __name__ == "__main__":
    main()