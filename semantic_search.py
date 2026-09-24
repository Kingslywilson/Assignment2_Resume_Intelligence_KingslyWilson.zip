from typing import List, Dict, Any, Union
from langchain_community.vectorstores import FAISS
from vector_store import load_vector_store


SIMILARITY_DISTANCE_THRESHOLD = 1.05


def get_candidate_retriever(vector_store: FAISS = None, k: int = 3):
    if vector_store is None:
        vector_store = load_vector_store()

    if vector_store is None:
        return None

    return vector_store.as_retriever(search_kwargs={"k": k})


def search_candidates(
    query: str,
    vector_store: FAISS = None,
    top_k: int = 3,
    distance_threshold: float = SIMILARITY_DISTANCE_THRESHOLD
) -> Union[List[Dict[str, Any]], str]:
    if vector_store is None:
        vector_store = load_vector_store()

    if vector_store is None:
        return "No sufficiently relevant candidate profiles were found for this search."

    try:
        results_with_scores = vector_store.similarity_search_with_score(query, k=top_k)
    except Exception as e:
        print(f"Search execution error: {e}")
        return "No sufficiently relevant candidate profiles were found for this search."

    if not results_with_scores:
        return "No sufficiently relevant candidate profiles were found for this search."

    relevant_matches = []
    for doc, distance in results_with_scores:
        if distance <= distance_threshold:
            relevant_matches.append({
                "candidate_id": doc.metadata.get("candidate_id", "Unknown"),
                "candidate_name": doc.metadata.get("candidate_name", "Unknown"),
                "resume_filename": doc.metadata.get("resume_filename", "Unknown"),
                "experience_category": doc.metadata.get("experience_category", "Unknown"),
                "skills_summary": doc.metadata.get("skills_summary", ""),
                "similarity_score": round(float(distance), 4),
                "professional_context": doc.page_content
            })

    if not relevant_matches:
        return "No sufficiently relevant candidate profiles were found for this search."

    return relevant_matches
