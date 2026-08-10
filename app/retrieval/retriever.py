from app.ingestion.indexer import get_vectorstore
from app.config import TOP_K


def retrieve_documents(query: str, k: int = TOP_K):
    """
    Retrieve the most relevant document chunks
    for a given user query.
    """

    vectorstore = get_vectorstore()

    results = vectorstore.similarity_search_with_relevance_scores(
        query,
        k=k
    )

    return results