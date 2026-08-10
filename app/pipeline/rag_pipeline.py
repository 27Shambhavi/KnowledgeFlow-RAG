from app.retrieval.retriever import retrieve_documents
from app.retrieval.relevance import filter_relevant_documents
from app.generation.llm import generate_answer
from app.generation.prompt import build_prompt


def run_rag(question: str):
    """
    Complete RAG pipeline:

    Question
        ↓
    Retrieval
        ↓
    Relevance filtering
        ↓
    Context creation
        ↓
    LLM
        ↓
    Answer
    """

    # Step 1: Retrieve
    results = retrieve_documents(question)

    # Step 2: Check relevance
    relevant_results = filter_relevant_documents(results)

    if not relevant_results:
        return {
            "answer": "Information not found in the uploaded documents.",
            "sources": [],
        }

    # Step 3: Build context
    context_parts = []

    sources = []

    for document, score in relevant_results:

        context_parts.append(
            document.page_content
        )

        source = document.metadata.get("source", "Unknown")

        sources.append({
            "source": source,
            "score": score,
            "page": document.metadata.get("page"),
        })

    context = "\n\n---\n\n".join(context_parts)

    # Step 4: Build prompt
    prompt = build_prompt(
        question=question,
        context=context,
    )

    # Step 5: Generate answer
    answer = generate_answer(prompt)

    return {
        "answer": answer,
        "sources": sources,
    }