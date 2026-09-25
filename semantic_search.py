from typing import List, Dict, Any, Union

from langchain_community.vectorstores import FAISS

from vector_store import load_vector_store


NO_MATCH_MESSAGE = "No sufficiently relevant candidate profiles were found for this search."


def get_candidate_retriever(vector_store: FAISS = None, k: int = 3):
    if vector_store is None:
        vector_store = load_vector_store()

    if vector_store is None:
        return None

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )


def search_candidates(
    query: str,
    vector_store: FAISS = None,
    top_k: int = 3
) -> Union[List[Dict[str, Any]], str]:

    if vector_store is None:
        vector_store = load_vector_store()

    if vector_store is None:
        return NO_MATCH_MESSAGE

    try:
        # Keep LangChain retriever usage for semantic search.
        retriever = get_candidate_retriever(
            vector_store=vector_store,
            k=top_k
        )

        if retriever is None:
            return NO_MATCH_MESSAGE

        documents = retriever.invoke(query)

        if not documents:
            return NO_MATCH_MESSAGE

        # Get similarity scores from FAISS.
        scored_documents = vector_store.similarity_search_with_score(
            query,
            k=top_k
        )

    except Exception as e:
        print(f"Search execution error: {e}")
        return NO_MATCH_MESSAGE

    if not scored_documents:
        return NO_MATCH_MESSAGE

    relevant_matches = []

    # FAISS distance:
    # lower distance = more similar
    #
    # With normalized embeddings, a conservative threshold
    # helps reject clearly unrelated queries.
    DISTANCE_THRESHOLD = 1.20

    for doc, distance in scored_documents:

        if distance > DISTANCE_THRESHOLD:
            continue

        relevant_matches.append({
            "candidate_id": doc.metadata.get(
                "candidate_id",
                "Unknown"
            ),
            "candidate_name": doc.metadata.get(
                "candidate_name",
                "Unknown"
            ),
            "resume_filename": doc.metadata.get(
                "resume_filename",
                "Unknown"
            ),
            "experience_category": doc.metadata.get(
                "experience_category",
                "Unknown"
            ),
            "total_experience": doc.metadata.get(
                "total_experience",
                "Not available"
            ),
            "skills_summary": doc.metadata.get(
                "skills_summary",
                ""
            ),
            "similarity_score": round(float(distance), 4),
            "professional_context": doc.page_content
        })

    if not relevant_matches:
        return NO_MATCH_MESSAGE

    return relevant_matches