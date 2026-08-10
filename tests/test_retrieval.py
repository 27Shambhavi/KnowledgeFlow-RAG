from app.retrieval.retriever import retrieve_documents
from app.retrieval.relevance import filter_relevant_documents


def main():

    query = input("\nAsk a question: ")

    print("\nSearching knowledge base...\n")

    # Retrieve chunks
    results = retrieve_documents(query)

    print(f"Retrieved chunks: {len(results)}")

    # Apply relevance threshold
    relevant_results = filter_relevant_documents(results)

    print(
        f"Relevant chunks: {len(relevant_results)}"
    )

    if not relevant_results:

        print(
            "\nInformation not found in the "
            "uploaded documents."
        )

        return

    print("\nRelevant information:\n")

    for i, (document, score) in enumerate(
        relevant_results,
        start=1
    ):

        print(f"--- Result {i} ---")
        print(f"Score: {score:.4f}")

        print(
            document.page_content[:1000]
        )

        print(
            f"Source: "
            f"{document.metadata.get('source')}"
        )

        print()


if __name__ == "__main__":
    main()