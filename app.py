import os
import json
import glob
from typing import List, Dict, Any

from dotenv import load_dotenv

load_dotenv()

from resume_loader import load_resumes_from_directory, load_single_resume
from preprocess import preprocess_resume_text

from parsers.pydantic_models import (
    CandidateProfile,
    CandidateInfo,
    SkillsCategorized,
    ExperienceClassification,
    JobDescriptionAnalysis,
    JobMatchAnalysis,
    ExplainableScoring,
    RecruiterRecommendation,
)

from chains.candidate_extraction import extract_candidate_info
from chains.skills_extraction import extract_skills
from chains.experience_classifier import classify_experience
from chains.jd_analysis import analyze_job_description
from chains.job_match import match_candidate_to_jd
from chains.scoring import calculate_candidate_score
from chains.recommendation import generate_recommendation
from vector_store import build_and_save_vector_store
from semantic_search import search_candidates, get_candidate_retriever


DATA_RESUMES_DIR = os.path.join(
    os.path.dirname(__file__),
    "data",
    "resumes",
)

DATA_JD_DIR = os.path.join(
    os.path.dirname(__file__),
    "data",
    "job_description",
)

OUTPUT_JSON_PATH = os.path.join(
    os.path.dirname(__file__),
    "outputs",
    "candidate_profiles.json",
)


def ensure_directories():
    """Ensure data and output directories exist."""
    os.makedirs(DATA_RESUMES_DIR, exist_ok=True)
    os.makedirs(DATA_JD_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(OUTPUT_JSON_PATH), exist_ok=True)


def load_job_description() -> str:
    ensure_directories()

    txt_files = sorted(
        glob.glob(os.path.join(DATA_JD_DIR, "*.txt"))
    )

    if txt_files:
        print(
            f"Loading Job Description from: "
            f"{os.path.basename(txt_files[0])}"
        )

        with open(txt_files[0], "r", encoding="utf-8") as f:
            return f.read().strip()

    pdf_files = sorted(
        glob.glob(os.path.join(DATA_JD_DIR, "*.pdf"))
    )

    if pdf_files:
        print(
            f"Loading Job Description from PDF: "
            f"{os.path.basename(pdf_files[0])}"
        )

        res_data = load_single_resume(
            pdf_files[0],
            "JD"
        )

        if res_data["success"]:
            return res_data["text"]

    print(
        "No Job Description file found in "
        "'data/job_description/'. "
        "Please add a .txt or .pdf file."
    )

    return ""


def process_single_candidate(
    resume_data: Dict[str, Any],
    jd_analysis: JobDescriptionAnalysis
) -> CandidateProfile:


    cand_id = resume_data["candidate_id"]
    filename = resume_data["filename"]
    raw_text = resume_data["text"]

    print("\n==================================================")
    print(f"Processing Candidate [{cand_id}]: {filename}")
    print("==================================================")

    cleaned_text = preprocess_resume_text(raw_text)

    print(
        f"  Stage 1: Preprocessed text "
        f"({len(cleaned_text)} chars)."
    )

    print("  Stage 2: Extracting Candidate Information...")

    cand_info = extract_candidate_info(cleaned_text)

    cand_name = (
        cand_info.candidate_name
        if cand_info.candidate_name
        and cand_info.candidate_name != "Not available"
        else filename
    )

    print("  Stage 3: Extracting Technical Skills...")
    skills = extract_skills(cleaned_text)

    print("  Stage 4: Classifying Experience Level...")

    experience = classify_experience(cleaned_text)

    print(
        "  Stage 5: Matching Candidate "
        "against Job Description..."
    )

    job_match = match_candidate_to_jd(
        cand_info,
        skills,
        experience,
        jd_analysis,
    )

    print("  Stage 6: Calculating Job Match Score...")

    scoring = calculate_candidate_score(
        cand_info,
        skills,
        experience,
        jd_analysis,
        job_match,
    )

    print(
        f"  -> Match Score: "
        f"{scoring.overall_score}/100"
    )

    print(
        "  Stage 7: Generating Recruiter Recommendation..."
    )

    recommendation = generate_recommendation(
        cand_id,
        cand_name,
        job_match,
        scoring,
        jd_analysis,
    )

    print(
        f"  -> Recommendation: "
        f"{recommendation.recommendation_category}"
    )

    profile = CandidateProfile(
        candidate_id=cand_id,
        candidate_name=cand_name,
        resume_filename=filename,
        candidate_info=cand_info,
        skills=skills,
        experience=experience,
        job_match=job_match,
        scoring=scoring,
        recommendation=recommendation,
    )

    return profile


def run_full_pipeline():

    ensure_directories()

    if not os.getenv("GROQ_API_KEY"):
        print(
            "\n[WARNING] GROQ_API_KEY environment "
            "variable is not set!"
        )

        print(
            "Please set your GROQ_API_KEY in the "
            "environment or create a .env file.\n"
        )

    loaded_resumes = load_resumes_from_directory(
        DATA_RESUMES_DIR
    )

    valid_resumes = [
        r for r in loaded_resumes
        if r["success"]
    ]

    if not valid_resumes:
        print(
            f"\nNo valid PDF resumes found to process "
            f"in '{DATA_RESUMES_DIR}'."
        )

        print(
            "Please place PDF resumes in the "
            "'data/resumes/' directory and run again."
        )

        return []

    jd_raw_text = load_job_description()

    if not jd_raw_text:
        print(
            "\nNo Job Description text available. "
            "Using generic baseline JD analysis for evaluation."
        )

        jd_analysis = JobDescriptionAnalysis(
            role_title="Software Development Engineer",
            required_skills=[
                "Python",
                "Software Engineering",
            ],
            required_experience="1+ years",
        )

    else:
        print(
            "\nAnalyzing Job Description with LLM..."
        )

        jd_analysis = analyze_job_description(
            jd_raw_text
        )

        print(
            f"JD Analysis Complete for role: "
            f"{jd_analysis.role_title}"
        )

    processed_profiles: List[CandidateProfile] = []

    for resume_data in valid_resumes:

        try:
            profile = process_single_candidate(
                resume_data,
                jd_analysis,
            )

            processed_profiles.append(profile)

        except Exception as e:

            print(
                f"[ERROR] Failed to process candidate "
                f"{resume_data['filename']}: {e}"
            )

    if processed_profiles:

        json_data = [
            p.model_dump()
            for p in processed_profiles
        ]

        with open(
            OUTPUT_JSON_PATH,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                json_data,
                f,
                indent=2,
            )

        print(
            f"\nSaved {len(processed_profiles)} "
            f"candidate profile(s) to "
            f"'{OUTPUT_JSON_PATH}'."
        )

        print(
            "\nBuilding FAISS vector search index..."
        )

        build_and_save_vector_store(
            processed_profiles
        )

    return processed_profiles


def interactive_search_mode():

    print("\n==================================================")
    print("Semantic Candidate Search Interface")
    print("==================================================")

    print(
        "Enter your natural language query "
        "(or type 'exit' / 'q' to quit)."
    )

    while True:

        try:

            query = input(
                "\nSearch Query > "
            ).strip()

            if not query or query.lower() in [
                "exit",
                "q",
                "quit",
            ]:

                print(
                    "Exiting search mode."
                )

                break

            results = search_candidates(query)

            if isinstance(results, str):

                print(
                    f"\nResult: {results}"
                )

            else:

                print(
                    f"\nFound {len(results)} "
                    f"matching candidate(s):"
                )

                for idx, res in enumerate(
                    results,
                    1,
                ):

                    print(
                        f"\n--- Result #{idx} ---"
                    )

                    print(
                        f"Candidate ID : "
                        f"{res.get('candidate_id', 'Not available')}"
                    )

                    print(
                        f"Candidate Name: "
                        f"{res.get('candidate_name', 'Not available')}"
                    )

                    print(
                        f"Resume File  : "
                        f"{res.get('resume_filename', 'Not available')}"
                    )

                    experience_category = res.get(
                        "experience_category",
                        "Not available",
                    )

                    total_experience = res.get(
                        "total_experience",
                        "Not available",
                    )

                    print(
                        f"Experience   : "
                        f"{experience_category} "
                        f"({total_experience})"
                    )

                    print(
                        f"Distance Score: "
                        f"{res.get('similarity_score', 'Not available')}"
                    )

                    print(
                        f"Skills       : "
                        f"{res.get('skills_summary', 'Not available')}"
                    )

        except (KeyboardInterrupt, EOFError):

            print(
                "\nExiting search mode."
            )

            break


def main():

    print(
        "=================================================="
    )

    print(
        " Intelligent Resume Intelligence Platform "
    )

    print(
        "=================================================="
    )

    profiles = run_full_pipeline()
    if profiles:

        print(
            "\nDo you want to perform natural "
            "language candidate search? (y/n)"
        )

        choice = input(
            "> "
        ).strip().lower()

        if choice in ["y", "yes"]:
            interactive_search_mode()
    else:

        print(
            "\nPipeline run finished. "
            "Add PDF resumes to data/resumes/ "
            "to process candidates."
        )

if __name__ == "__main__":
    main()