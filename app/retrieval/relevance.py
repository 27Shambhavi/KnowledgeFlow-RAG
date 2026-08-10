from app.config import RELEVANCE_THRESHOLD


def filter_relevant_documents(results):
    """
    Keep only documents whose relevance score
    is above the configured threshold.
    """

    relevant_documents = []

    for document, score in results:

        if score >= RELEVANCE_THRESHOLD:
            relevant_documents.append(
                (document, score)
            )

    return relevant_documents