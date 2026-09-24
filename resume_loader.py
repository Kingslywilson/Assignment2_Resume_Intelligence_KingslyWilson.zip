"""
Resume Loader module.
Handles loading and extracting text from PDF resumes using PyPDFLoader with robust error handling.
"""

import os
import glob
from typing import List, Dict, Any, Tuple
from langchain_community.document_loaders import PyPDFLoader


def generate_candidate_id(index: int) -> str:
    """Generate candidate ID like CAND001, CAND002."""
    return f"CAND{index + 1:03d}"


def load_single_resume(pdf_path: str, candidate_id: str) -> Dict[str, Any]:
    """
    Loads and extracts text from a single PDF resume using PyPDFLoader.
    Preserves original filename, candidate ID, and page metadata.
    Returns a dictionary containing extracted text and metadata, or an error status.
    """
    filename = os.path.basename(pdf_path)
    result = {
        "candidate_id": candidate_id,
        "filename": filename,
        "filepath": pdf_path,
        "text": "",
        "pages": [],
        "page_count": 0,
        "success": False,
        "error": None
    }

    if not os.path.exists(pdf_path):
        result["error"] = f"File not found: {pdf_path}"
        return result

    if os.path.getsize(pdf_path) == 0:
        result["error"] = f"Empty PDF file (0 bytes): {filename}"
        return result

    try:
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        if not documents:
            result["error"] = f"No pages or text extracted from PDF: {filename}"
            return result

        extracted_text_pages = []
        page_metadata = []

        for idx, doc in enumerate(documents):
            page_text = doc.page_content if doc.page_content else ""
            extracted_text_pages.append(page_text)
            page_metadata.append({
                "page_number": idx + 1,
                "metadata": doc.metadata
            })

        full_text = "\n\n".join(extracted_text_pages).strip()

        if not full_text:
            result["error"] = f"PDF contains no extractable text (possibly scanned or empty): {filename}"
            return result

        result["text"] = full_text
        result["pages"] = page_metadata
        result["page_count"] = len(documents)
        result["success"] = True

    except Exception as e:
        result["error"] = f"Corrupted or invalid PDF format: {str(e)}"

    return result


def load_resumes_from_directory(resumes_dir: str) -> List[Dict[str, Any]]:
    """
    Loads all PDF resumes from the specified directory.
    Processes each resume independently so a failed file does not crash the app.
    """
    if not os.path.exists(resumes_dir):
        os.makedirs(resumes_dir, exist_ok=True)
        print(f"Created directory: {resumes_dir}")
        return []

    pdf_files = sorted(glob.glob(os.path.join(resumes_dir, "*.pdf")))
    
    if not pdf_files:
        print(f"No PDF resumes found in directory: {resumes_dir}")
        return []

    loaded_resumes = []
    print(f"Found {len(pdf_files)} PDF resume(s) in '{resumes_dir}'. Processing...")

    for idx, pdf_path in enumerate(pdf_files):
        cand_id = generate_candidate_id(idx)
        filename = os.path.basename(pdf_path)
        print(f"Loading [{cand_id}] {filename}...")
        
        resume_data = load_single_resume(pdf_path, cand_id)
        if not resume_data["success"]:
            print(f"  [ERROR] Failed to load {filename}: {resume_data['error']}")
        else:
            print(f"  [SUCCESS] Extracted {len(resume_data['text'])} chars across {resume_data['page_count']} page(s).")
            
        loaded_resumes.append(resume_data)

    return loaded_resumes
