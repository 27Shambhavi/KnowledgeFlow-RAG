import os

from app.ingestion.document_registry import (
    calculate_file_hash,
    register_document,
    get_document,
    list_documents,
)


def main():

    test_file = "data/test_registry.txt"

    # Create a temporary test document
    os.makedirs(
        "data",
        exist_ok=True
    )

    with open(
        test_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "This is a registry test document."
        )

    # Calculate hash
    file_hash = calculate_file_hash(
        test_file
    )

    print(
        "File hash:"
    )

    print(
        file_hash
    )

    # Register document
    register_document(
        filename="test_registry.txt",
        file_hash=file_hash,
        chunk_count=5,
    )

    # Retrieve document
    document = get_document(
        "test_registry.txt"
    )

    print(
        "\nRegistered document:"
    )

    print(
        document
    )

    # List documents
    documents = list_documents()

    print(
        "\nAll registered documents:"
    )

    for doc in documents:
        print(
            doc
        )

    # Cleanup test file
    os.remove(
        test_file
    )


if __name__ == "__main__":
    main()