from typing import List, Dict, Any, Union

from langchain_community.vectorstores import FAISS

from vector_store import load_vector_store


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
        return "No sufficiently relevant candidate profiles were found for this search."

    try:
        retriever = get_candidate_retriever(
            vector_store=vector_store,
            k=top_k
        )

        if retriever is None:
            return "No sufficiently relevant candidate profiles were found for this search."

        documents = retriever.invoke(query)

    except Exception as e:
        print(f"Search execution error: {e}")
        return "No sufficiently relevant candidate profiles were found for this search."

    if not documents:
        return "No sufficiently relevant candidate profiles were found for this search."

    relevant_matches = []

    for doc in documents:
        relevant_matches.append({
            "candidate_id": doc.metadata.get("candidate_id", "Unknown"),
            "candidate_name": doc.metadata.get("candidate_name", "Unknown"),
            "resume_filename": doc.metadata.get("resume_filename", "Unknown"),
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
            "similarity_score": "Semantic match",
            "professional_context": doc.page_content
        })

    return relevant_matches