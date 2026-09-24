"""
Vector Store module.
Manages candidate embeddings generation and FAISS vector index building/persistence.
Uses HuggingFace Embeddings and FAISS for semantic candidate retrieval.
"""

import os
from typing import List, Dict, Any, Tuple
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from parsers.pydantic_models import CandidateProfile

VECTOR_DB_DIR = os.path.join(os.path.dirname(__file__), "outputs", "faiss_index")


def get_embedding_function():
    """
    Returns local HuggingFace embeddings model (sentence-transformers/all-MiniLM-L6-v2)
    with normalized embeddings for precise cosine similarity metric thresholding.
    """
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        encode_kwargs={"normalize_embeddings": True}
    )


def build_candidate_document(profile: CandidateProfile) -> Document:
    """
    Constructs a LangChain Document containing only professional skills, experience, projects,
    certifications, and technology history for vector embedding.
    EXCLUDES personal identifiable information (email, phone, address).
    """
    info = profile.candidate_info
    skills = profile.skills
    exp = profile.experience

    # Gather skills across categories
    all_skills_list = []
    for field_name, val in skills.model_dump().items():
        if isinstance(val, list):
            all_skills_list.extend(val)

    # Format project descriptions
    project_texts = []
    for p in info.projects:
        tech_str = f" (Tech: {', '.join(p.technologies)})" if p.technologies else ""
        desc_str = f": {p.description}" if p.description else ""
        project_texts.append(f"Project '{p.title}'{tech_str}{desc_str}")

    # Build concise professional text representation
    doc_content = (
        f"Candidate ID: {profile.candidate_id}\n"
        f"Name: {profile.candidate_name}\n"
        f"Experience Level: {exp.experience_category}\n"
        f"Total Experience: {exp.total_professional_experience}\n"
        f"Relevant Experience: {exp.relevant_experience}\n"
        f"Current/Previous Roles: {', '.join(info.job_titles) if info.job_titles else 'None'}\n"
        f"Companies: {', '.join(info.companies) if info.companies else 'None'}\n"
        f"Technical Skills: {', '.join(all_skills_list) if all_skills_list else 'None'}\n"
        f"Programming Languages: {', '.join(skills.programming_languages)}\n"
        f"Frameworks: {', '.join(skills.frameworks)}\n"
        f"Databases: {', '.join(skills.databases)}\n"
        f"Cloud & DevOps: {', '.join(skills.cloud_technologies + skills.devops)}\n"
        f"AI/ML & GenAI: {', '.join(skills.ai_ml + skills.generative_ai)}\n"
        f"Backend & Frontend: {', '.join(skills.backend_technologies + skills.frontend_technologies)}\n"
        f"Certifications: {', '.join(info.certifications) if info.certifications else 'None'}\n"
        f"Key Projects:\n" + "\n".join(project_texts)
    )

    metadata = {
        "candidate_id": profile.candidate_id,
        "candidate_name": profile.candidate_name,
        "resume_filename": profile.resume_filename,
        "skills_summary": ", ".join(all_skills_list[:15]),
        "experience_category": exp.experience_category,
        "total_experience": exp.total_professional_experience
    }

    return Document(page_content=doc_content, metadata=metadata)


def build_and_save_vector_store(profiles: List[CandidateProfile], db_dir: str = VECTOR_DB_DIR) -> FAISS:
    """
    Builds a FAISS vector database from a list of candidate profiles and saves it locally.
    """
    if not profiles:
        print("No candidate profiles provided to build vector store.")
        return None

    docs = [build_candidate_document(p) for p in profiles]
    embeddings = get_embedding_function()

    print(f"Generating embeddings for {len(docs)} candidate profile(s)...")
    vector_store = FAISS.from_documents(docs, embeddings)

    os.makedirs(db_dir, exist_ok=True)
    vector_store.save_local(db_dir)
    print(f"FAISS vector store successfully saved to '{db_dir}'.")
    return vector_store


def load_vector_store(db_dir: str = VECTOR_DB_DIR) -> FAISS:
    """
    Loads FAISS vector database from local directory.
    """
    if not os.path.exists(db_dir):
        return None

    embeddings = get_embedding_function()
    try:
        vector_store = FAISS.load_local(db_dir, embeddings, allow_dangerous_deserialization=True)
        return vector_store
    except Exception as e:
        print(f"Error loading FAISS vector store: {e}")
        return None
