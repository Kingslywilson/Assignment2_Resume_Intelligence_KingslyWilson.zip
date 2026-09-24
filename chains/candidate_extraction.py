"""
Chain 1: Candidate Information Extraction.
Extracts candidate contact details, education, job titles, companies, projects, and certifications.
Uses PydanticOutputParser for strict schema enforcement.
"""

import os
from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from parsers.pydantic_models import CandidateInfo
from parsers.output_parsers import get_pydantic_parser, parse_llm_output_with_retry


PROMPT_FILE = os.path.join(os.path.dirname(__file__), "..", "prompts", "candidate_extraction_prompt.txt")


def load_prompt() -> str:
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        return f.read()


def extract_candidate_info(resume_text: str, llm: ChatGroq = None) -> CandidateInfo:
    """
    Executes Candidate Extraction chain.
    """
    if llm is None:
        model_name = os.getenv("GROQ_MODEL") or os.getenv("GROQ_MODEL_NAME") or "llama-3.3-70b-versatile"
        llm = ChatGroq(model=model_name, temperature=0.0)

    parser = get_pydantic_parser(CandidateInfo)
    prompt_text = load_prompt()
    prompt = PromptTemplate(
        template=prompt_text,
        input_variables=["resume_text"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    formatted_prompt = prompt.format(resume_text=resume_text)
    
    try:
        response = llm.invoke(formatted_prompt)
        raw_text = response.content if hasattr(response, "content") else str(response)
        
        fallback_dict = {
            "candidate_name": "Not available",
            "total_experience": "Not available"
        }
        return parse_llm_output_with_retry(raw_text, CandidateInfo, fallback_dict)
    except Exception as e:
        print(f"Error in extract_candidate_info chain: {e}")
        return CandidateInfo()
