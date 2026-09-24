"""
Chain 2: Technical Skills Extraction.
Extracts and categorizes technical skills into programming languages, frameworks, databases, cloud, AI/ML, etc.
Uses PydanticOutputParser with strict anti-hallucination rules.
"""

import os
from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from parsers.pydantic_models import SkillsCategorized
from parsers.output_parsers import get_pydantic_parser, parse_llm_output_with_retry


PROMPT_FILE = os.path.join(os.path.dirname(__file__), "..", "prompts", "skills_extraction_prompt.txt")


def load_prompt() -> str:
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        return f.read()


def extract_skills(resume_text: str, llm: ChatGroq = None) -> SkillsCategorized:
    """
    Executes Technical Skills Extraction chain.
    """
    if llm is None:
        model_name = os.getenv("GROQ_MODEL") or os.getenv("GROQ_MODEL_NAME") or "llama-3.3-70b-versatile"
        llm = ChatGroq(model=model_name, temperature=0.0)

    parser = get_pydantic_parser(SkillsCategorized)
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
        
        fallback_dict = {}
        return parse_llm_output_with_retry(raw_text, SkillsCategorized, fallback_dict)
    except Exception as e:
        print(f"Error in extract_skills chain: {e}")
        return SkillsCategorized()
