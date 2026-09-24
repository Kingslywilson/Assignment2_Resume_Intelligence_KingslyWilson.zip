"""
Chain 5: Candidate-to-JD Matching.
Compares candidate profile against Job Description requirements.
Demonstrates JsonOutputParser for flexible data structure extraction.
"""

import os
import json
from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from parsers.pydantic_models import (
    CandidateInfo, SkillsCategorized, ExperienceClassification,
    JobDescriptionAnalysis, JobMatchAnalysis
)
from parsers.output_parsers import get_json_parser, parse_json_output_with_retry


PROMPT_FILE = os.path.join(os.path.dirname(__file__), "..", "prompts", "job_match_prompt.txt")


def load_prompt() -> str:
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        return f.read()


def match_candidate_to_jd(
    candidate_info: CandidateInfo,
    skills: SkillsCategorized,
    experience: ExperienceClassification,
    jd_analysis: JobDescriptionAnalysis,
    llm: ChatGroq = None
) -> JobMatchAnalysis:
    """
    Executes Candidate-to-JD Matching chain.
    """
    if llm is None:
        model_name = os.getenv("GROQ_MODEL") or os.getenv("GROQ_MODEL_NAME") or "openai/gpt-oss-120b"
        llm = ChatGroq(model=model_name, temperature=0.0)

    json_parser = get_json_parser()
    prompt_text = load_prompt()

    schema_instructions = (
        "Return a JSON object with keys: "
        "'matched_skills' (list of strings), 'missing_skills' (list of strings), "
        "'additional_relevant_skills' (list of strings), 'relevant_experience_match' (string), "
        "'project_alignment' (string), 'qualification_alignment' (string), 'technology_alignment' (string)."
    )

    prompt = PromptTemplate(
        template=prompt_text,
        input_variables=["candidate_info", "candidate_skills", "candidate_experience", "jd_analysis"],
        partial_variables={"format_instructions": schema_instructions}
    )

    formatted_prompt = prompt.format(
        candidate_info=candidate_info.model_dump_json(),
        candidate_skills=skills.model_dump_json(),
        candidate_experience=experience.model_dump_json(),
        jd_analysis=jd_analysis.model_dump_json()
    )

    fallback_dict = {
        "matched_skills": [],
        "missing_skills": [],
        "additional_relevant_skills": [],
        "relevant_experience_match": "Unevaluated",
        "project_alignment": "Unevaluated",
        "qualification_alignment": "Unevaluated",
        "technology_alignment": "Unevaluated"
    }

    try:
        response = llm.invoke(formatted_prompt)
        raw_text = response.content if hasattr(response, "content") else str(response)
        
        parsed_json = parse_json_output_with_retry(raw_text, fallback_dict)
        return JobMatchAnalysis.model_validate(parsed_json)
    except Exception as e:
        print(f"Error in match_candidate_to_jd chain: {e}")
        return JobMatchAnalysis()
