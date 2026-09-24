"""
Chain 6: Explainable Candidate Scoring.
Computes a quantitative, transparent 0-100 job match score based on documented criteria:
- Skills Match (40%)
- Relevant Experience (25%)
- Projects (15%)
- Education (10%)
- Additional Requirements (10%)
Uses PydanticOutputParser for strict score validation.
"""

import os
from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from parsers.pydantic_models import (
    CandidateInfo, SkillsCategorized, ExperienceClassification,
    JobDescriptionAnalysis, JobMatchAnalysis, ExplainableScoring, CategoryScore
)
from parsers.output_parsers import get_pydantic_parser, parse_llm_output_with_retry


PROMPT_FILE = os.path.join(os.path.dirname(__file__), "..", "prompts", "scoring_prompt.txt")


def load_prompt() -> str:
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        return f.read()


def calculate_candidate_score(
    candidate_info: CandidateInfo,
    skills: SkillsCategorized,
    experience: ExperienceClassification,
    jd_analysis: JobDescriptionAnalysis,
    job_match: JobMatchAnalysis,
    llm: ChatGroq = None
) -> ExplainableScoring:
    """
    Executes Explainable Scoring chain.
    Ensures final overall_score is between 0.0 and 100.0.
    """
    if llm is None:
        model_name = os.getenv("GROQ_MODEL") or os.getenv("GROQ_MODEL_NAME") or "llama-3.3-70b-versatile"
        llm = ChatGroq(model=model_name, temperature=0.0)

    parser = get_pydantic_parser(ExplainableScoring)
    prompt_text = load_prompt()

    summary_payload = {
        "candidate_info": candidate_info.model_dump(),
        "skills": skills.model_dump(),
        "experience": experience.model_dump()
    }

    prompt = PromptTemplate(
        template=prompt_text,
        input_variables=["candidate_profile_summary", "jd_analysis", "job_match"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    formatted_prompt = prompt.format(
        candidate_profile_summary=str(summary_payload),
        jd_analysis=jd_analysis.model_dump_json(),
        job_match=job_match.model_dump_json()
    )

    fallback_scores = ExplainableScoring(
        overall_score=0.0,
        category_scores=[
            CategoryScore(category_name="Skills Match", score=0.0, weight_percent=40.0, weighted_score=0.0, justification="Could not parse LLM output"),
            CategoryScore(category_name="Relevant Experience", score=0.0, weight_percent=25.0, weighted_score=0.0, justification="Could not parse LLM output"),
            CategoryScore(category_name="Projects", score=0.0, weight_percent=15.0, weighted_score=0.0, justification="Could not parse LLM output"),
            CategoryScore(category_name="Education", score=0.0, weight_percent=10.0, weighted_score=0.0, justification="Could not parse LLM output"),
            CategoryScore(category_name="Additional Requirements", score=0.0, weight_percent=10.0, weighted_score=0.0, justification="Could not parse LLM output"),
        ],
        missing_requirements=["Evaluation unparsed"],
        scoring_breakdown_summary="Fallback score generated due to parsing error."
    )

    try:
        response = llm.invoke(formatted_prompt)
        raw_text = response.content if hasattr(response, "content") else str(response)
        
        result = parse_llm_output_with_retry(raw_text, ExplainableScoring, fallback_scores.model_dump())
        
        # Ensure bounds safety (0.0 to 100.0)
        result.overall_score = max(0.0, min(100.0, float(result.overall_score)))
        for cat in result.category_scores:
            cat.score = max(0.0, min(100.0, float(cat.score)))
            cat.weighted_score = max(0.0, min(100.0, float(cat.score) * float(cat.weight_percent) / 100.0))
            
        return result
    except Exception as e:
        print(f"Error in calculate_candidate_score chain: {e}")
        return fallback_scores
