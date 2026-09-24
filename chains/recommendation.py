"""
Chain 7: Recruiter Recommendation.
Generates an analytical recommendation for recruiters (Strong Match, Potential Match, Needs Further Review, Low Match)
along with key strengths, missing requirements, and interview verification areas.
Uses PydanticOutputParser.
"""

import os
from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from parsers.pydantic_models import (
    JobDescriptionAnalysis, JobMatchAnalysis, ExplainableScoring, RecruiterRecommendation
)
from parsers.output_parsers import get_pydantic_parser, parse_llm_output_with_retry


PROMPT_FILE = os.path.join(os.path.dirname(__file__), "..", "prompts", "recommendation_prompt.txt")


def load_prompt() -> str:
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        return f.read()


def generate_recommendation(
    candidate_id: str,
    candidate_name: str,
    job_match: JobMatchAnalysis,
    scoring_results: ExplainableScoring,
    jd_analysis: JobDescriptionAnalysis,
    llm: ChatGroq = None
) -> RecruiterRecommendation:
    """
    Executes Recruiter Recommendation chain.
    """
    if llm is None:
        model_name = os.getenv("GROQ_MODEL") or os.getenv("GROQ_MODEL_NAME") or "llama-3.3-70b-versatile"
        llm = ChatGroq(model=model_name, temperature=0.0)

    parser = get_pydantic_parser(RecruiterRecommendation)
    prompt_text = load_prompt()

    prompt = PromptTemplate(
        template=prompt_text,
        input_variables=["candidate_id", "candidate_name", "job_match", "scoring_results", "jd_analysis"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    formatted_prompt = prompt.format(
        candidate_id=candidate_id,
        candidate_name=candidate_name,
        job_match=job_match.model_dump_json(),
        scoring_results=scoring_results.model_dump_json(),
        jd_analysis=jd_analysis.model_dump_json()
    )

    fallback_recommendation = RecruiterRecommendation(
        recommendation_category="Needs Further Review",
        key_strengths=[],
        relevant_skills=job_match.matched_skills,
        relevant_experience_summary="Unable to generate automated summary.",
        missing_requirements=job_match.missing_skills,
        areas_requiring_verification=["Verify candidate experience directly during interview."],
        overall_jd_alignment_summary="Recommendation generated via fallback logic due to parsing issue."
    )

    try:
        response = llm.invoke(formatted_prompt)
        raw_text = response.content if hasattr(response, "content") else str(response)
        
        return parse_llm_output_with_retry(raw_text, RecruiterRecommendation, fallback_recommendation.model_dump())
    except Exception as e:
        print(f"Error in generate_recommendation chain: {e}")
        return fallback_recommendation
