from app.pipeline.rag_pipeline import run_rag


def main():

    question = input("\nAsk a question: ")

    result = run_rag(question)

    print("\n" + "=" * 60)
    print("ANSWER")
    print("=" * 60)

    print(result["answer"])

    print("\n" + "=" * 60)
    print("SOURCES")
    print("=" * 60)

    for source in result["sources"]:
        print(
            f"Source: {source['source']}"
        )

        print(
            f"Score: {source['score']:.4f}"
        )

        print(
            f"Page: {source['page']}"
        )

        print()


if __name__ == "__main__":
    main()