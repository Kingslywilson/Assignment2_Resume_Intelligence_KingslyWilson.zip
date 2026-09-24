"""
Chain 4: Job Description Analysis.
Analyzes job description text and extracts required skills, preferred skills, required experience, qualifications, and responsibilities.
Uses PydanticOutputParser.
"""

import os
from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from parsers.pydantic_models import JobDescriptionAnalysis
from parsers.output_parsers import get_pydantic_parser, parse_llm_output_with_retry


PROMPT_FILE = os.path.join(os.path.dirname(__file__), "..", "prompts", "jd_analysis_prompt.txt")


def load_prompt() -> str:
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        return f.read()


def analyze_job_description(job_description_text: str, llm: ChatGroq = None) -> JobDescriptionAnalysis:
    """
    Executes Job Description Analysis chain.
    """
    if llm is None:
        model_name = os.getenv("GROQ_MODEL") or os.getenv("GROQ_MODEL_NAME") or "llama-3.3-70b-versatile"
        llm = ChatGroq(model=model_name, temperature=0.0)

    parser = get_pydantic_parser(JobDescriptionAnalysis)
    prompt_text = load_prompt()
    prompt = PromptTemplate(
        template=prompt_text,
        input_variables=["job_description_text"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    formatted_prompt = prompt.format(job_description_text=job_description_text)

    try:
        response = llm.invoke(formatted_prompt)
        raw_text = response.content if hasattr(response, "content") else str(response)
        
        fallback_dict = {
            "role_title": "Position",
            "required_experience": "Not specified"
        }
        return parse_llm_output_with_retry(raw_text, JobDescriptionAnalysis, fallback_dict)
    except Exception as e:
        print(f"Error in analyze_job_description chain: {e}")
        return JobDescriptionAnalysis()
