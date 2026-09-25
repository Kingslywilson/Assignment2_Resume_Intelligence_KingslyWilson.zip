# Intelligent Resume Intelligence Platform

## Overview

A Python and LangChain based Resume Intelligence Platform that processes multiple PDF resumes, extracts candidate information and skills, analyzes experience, compares candidates with a Job Description, generates explainable scores and recruiter recommendations, and supports semantic candidate search.

## Features

* Multiple PDF resume processing
* Resume text extraction using PyPDF
* Resume text preprocessing
* Candidate information extraction
* Technical skill extraction and categorization
* Experience classification
* Job Description analysis
* Candidate-to-JD matching
* Explainable candidate scoring (0–100)
* Recruiter recommendation
* Structured Pydantic output
* JSON output generation
* Hugging Face embeddings
* FAISS vector database
* LangChain semantic candidate search
* Graceful handling of invalid resumes
* Hallucination prevention through document-grounded prompts

## Technologies

* Python
* LangChain
* LangChain Core
* LangChain Groq
* LangChain Hugging Face
* Pydantic
* PyPDF
* FAISS
* Sentence Transformers
* Groq LLM
* Hugging Face Embeddings

## Project Structure

```text
Assignment2_Resume_Intelligence_YourName/
│
├── app.py
├── resume_loader.py
├── preprocess.py
├── vector_store.py
├── semantic_search.py
│
├── chains/
│   ├── candidate_extraction.py
│   ├── skills_extraction.py
│   ├── experience_classifier.py
│   ├── jd_analysis.py
│   ├── job_match.py
│   ├── scoring.py
│   └── recommendation.py
│
├── parsers/
│   ├── pydantic_models.py
│   └── output_parsers.py
│
├── prompts/
│   ├── candidate_extraction_prompt.txt
│   ├── skills_extraction_prompt.txt
│   ├── experience_prompt.txt
│   ├── jd_analysis_prompt.txt
│   ├── job_match_prompt.txt
│   ├── scoring_prompt.txt
│   └── recommendation_prompt.txt
│
├── data/
│   ├── resumes/
│   └── job_description/
│
├── outputs/
│   └── candidate_profiles.json
│
├── resume_intelligence_strategy.md
├── test_log.md
├── requirements.txt
└── .env.example
```

## Installation

Create and activate a Python virtual environment, then install the dependencies:

```text
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file locally:

```text
GROQ_API_KEY=your_groq_api_key
```

Do not upload the `.env` file or expose the API key.

The project also includes `.env.example` as a template.

## Adding Resumes

Place PDF resumes inside:

```text
data/resumes/
```

Multiple resumes can be added.

The system assigns candidate IDs such as:

```text
CAND001
CAND002
CAND003
```

Invalid or unreadable resumes are handled without stopping the processing of valid resumes.

## Adding a Job Description

Place a `.txt` or `.pdf` Job Description inside:

```text
data/job_description/
```

The application analyzes the Job Description and extracts:

* Required skills
* Preferred skills
* Required experience
* Qualifications
* Responsibilities
* Additional requirements

## Processing Pipeline

The application follows a multi-stage workflow:

```text
PDF Resume
    ↓
Text Extraction
    ↓
Preprocessing
    ↓
Candidate Information
    ↓
Skills Extraction
    ↓
Experience Classification
    ↓
Job Description Analysis
    ↓
Candidate-to-JD Matching
    ↓
Explainable Scoring
    ↓
Recruiter Recommendation
    ↓
Structured Candidate Profile
    ↓
FAISS Vector Store
    ↓
Semantic Candidate Search
```

## Running the Application

Run:

```text
python app.py
```

The application provides three options:

```text
1. Process resumes and build/update FAISS
2. Load existing FAISS and perform semantic search
3. Exit
```

### Option 1

Use this when:

* Adding new resumes
* Changing resumes
* Changing the Job Description
* Rebuilding the FAISS index

This runs the complete LLM pipeline and creates:

```text
outputs/candidate_profiles.json
```

It also builds the FAISS vector store.

### Option 2

Use this when the FAISS index already exists and you only want to perform semantic searches.

Example queries:

```text
developer
```

```text
Java developer with Spring Boot experience
```

```text
Python backend developer
```

```text
AI and machine learning candidate
```

```text
candidate with React and Node.js experience
```

The search uses embeddings and FAISS semantic retrieval rather than exact keyword matching only.

## Structured Output

Pydantic models are used to validate candidate profiles and other structured results.

The project also demonstrates structured JSON parsing through the configured output parsers.

The final candidate information is stored in:

```text
outputs/candidate_profiles.json
```

## Explainable Scoring

Candidates receive an overall score from:

```text
0–100
```

The score is based on job-relevant evidence from the resume and Job Description.

The scoring includes areas such as:

* Skills
* Experience
* Projects
* Education
* Additional requirements

The system does not use unrelated personal characteristics for scoring.

## Recruiter Recommendation

The system generates a recruiter-support recommendation such as:

* Strong Match
* Potential Match
* Needs Further Review
* Low Match

The recommendation includes relevant strengths, missing requirements, and areas that may require verification.

The system is intended to assist recruiters and does not make the final hiring decision.

## Semantic Search

Professional information is converted into embeddings and stored in FAISS.

Search considers information such as:

* Skills
* Experience
* Projects
* Technologies
* Role history
* Certifications
* Relevant education

Example:

```text
Search Query > Java developer with Spring Boot experience
```

The system returns semantically relevant candidate profiles.

If no sufficiently relevant candidate is found, the application returns:

```text
No sufficiently relevant candidate profiles were found for this search.
```

## Hallucination Prevention

The prompts instruct the LLM to:

* Use only the supplied resume or Job Description information
* Never invent missing information
* Return `Not available` or `null` when information is missing
* Avoid unsupported assumptions
* Keep matching and scoring grounded in resume and JD evidence

## Privacy and Responsible Evaluation

Only job-relevant professional information is used for candidate evaluation.

The system does not intentionally use or infer:

* Gender
* Religion
* Caste
* Ethnicity
* Marital status
* Disability
* Photograph-based information
* Other protected personal characteristics

Use synthetic, sample, or authorized resumes for testing.

## Testing

Actual application tests and results are documented in:

```text
test_log.md
```

Testing includes resume processing, candidate extraction, Job Description analysis, matching, scoring, recommendation, invalid resume handling, and semantic search.

## Known Limitations

* LLM results depend on the configured Groq model and API limits.
* PDF quality can affect text extraction.
* Semantic search quality depends on the embedding model and indexed candidate information.
* API credentials are required for LLM-based processing.
* Recruiter recommendations are decision-support outputs and require human review.

## Requirements

Install all dependencies using:

```text
pip install -r requirements.txt
```

The exact package versions used for the project are documented in `requirements.txt`.
