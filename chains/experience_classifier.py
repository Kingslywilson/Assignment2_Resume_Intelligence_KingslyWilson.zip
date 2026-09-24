"""
Chain 3: Experience Classification.
Classifies candidate experience level (Fresher, Internship, Entry-level, Experienced) and extracts relevant experience details.
Demonstrates JsonOutputParser usage.
"""

import os
import json
from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from parsers.pydantic_models import ExperienceClassification
from parsers.output_parsers import get_json_parser, parse_json_output_with_retry, parse_llm_output_with_retry


PROMPT_FILE = os.path.join(os.path.dirname(__file__), "..", "prompts", "experience_prompt.txt")


def load_prompt() -> str:
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        return f.read()


def classify_experience(resume_text: str, llm: ChatGroq = None) -> ExperienceClassification:
    """
    Executes Experience Classification chain using JsonOutputParser.
    """
    if llm is None:
        model_name = os.getenv("GROQ_MODEL") or os.getenv("GROQ_MODEL_NAME") or "llama-3.3-70b-versatile"
        llm = ChatGroq(model=model_name, temperature=0.0)

    json_parser = get_json_parser()
    prompt_text = load_prompt()
    
    schema_instructions = (
        "Return a JSON object with keys: "
        "'experience_category' (one of: 'Fresher', 'Internship experience', 'Entry-level', 'Experienced professional'), "
        "'total_professional_experience', 'relevant_experience', 'internship_duration', "
        "'relevant_projects' (list of strings), 'role_exposure' (list of strings)."
    )

    prompt = PromptTemplate(
        template=prompt_text,
        input_variables=["resume_text"],
        partial_variables={"format_instructions": schema_instructions}
    )

    formatted_prompt = prompt.format(resume_text=resume_text)

    fallback_dict = {
        "experience_category": "Fresher",
        "total_professional_experience": "Not available",
        "relevant_experience": "Not available",
        "internship_duration": "Not available",
        "relevant_projects": [],
        "role_exposure": []
    }

    try:
        response = llm.invoke(formatted_prompt)
        raw_text = response.content if hasattr(response, "content") else str(response)
        
        parsed_json = parse_json_output_with_retry(raw_text, fallback_dict)
        return ExperienceClassification.model_validate(parsed_json)
    except Exception as e:
        print(f"Error in classify_experience chain: {e}")
        return ExperienceClassification(experience_category="Fresher")
