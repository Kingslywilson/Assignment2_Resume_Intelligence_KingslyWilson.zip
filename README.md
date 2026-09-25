# Intelligent Resume Intelligence Platform

## Overview

This project is a Python and LangChain-based Resume Intelligence Platform for analyzing resumes against job descriptions.

The system supports:

* Multiple PDF resume uploads
* Resume text extraction and preprocessing
* Candidate information extraction
* Skills extraction
* Experience classification
* Job description analysis
* Candidate-to-JD matching
* Explainable candidate scoring
* Recruiter recommendations
* Structured JSON output
* FAISS-based semantic candidate search
* Incomplete and malformed PDF handling

The system is designed as a recruiter decision-support tool and does not make final hiring decisions.

---

## Technologies

* Python 3.11
* LangChain
* LangChain Groq
* LangChain HuggingFace
* Pydantic
* PyPDF
* FAISS
* Sentence Transformers
* Groq LLM
* Hugging Face Embeddings

---

## Project Structure

```text
Assignment2_Resume_Intelligence_YourName/
│
├── app.py
├── resume_loader.py
├── preprocess.py
├── vector_store.py
├── semantic_search.py
├── requirements.txt
├── .env.example
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
│   ├── candidate_profiles.json
│   └── faiss_index/
│
├── resume_intelligence_strategy.md
├── test_log.md
└── README.md
```

---

## Installation

Create and activate a virtual environment.

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file using `.env.example`.

```text
GROQ_API_KEY=your_groq_api_key_here
```

Do not commit the actual `.env` file or API keys.

---

## How to Run

Place resume PDF files inside:

```text
data/resumes/
```

Place the job description inside:

```text
data/job_description/
```

Run the application:

```bash
python app.py
```

The application provides options for:

1. Running the complete resume intelligence pipeline
2. Performing semantic candidate search

---

## Resume Processing Pipeline

The application processes resumes through multiple stages:

```text
PDF Resume
    ↓
Text Extraction
    ↓
Preprocessing
    ↓
Candidate Information Extraction
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
```

Each major stage uses separated prompt/chain logic.

---

## Structured Output

Candidate information is validated using Pydantic models.

The application generates:

```text
outputs/candidate_profiles.json
```

The structured profile contains candidate information, skills, experience, job matching, scoring, and recommendation information.

The project also demonstrates structured JSON parsing using LangChain output parsers.

---

## Candidate Scoring

Candidates receive an explainable score from **0–100**.

The scoring weights used are:

| Category                  | Weight |
| ------------------------- | -----: |
| Skills Match              |    40% |
| Relevant Experience       |    25% |
| Projects Alignment        |    15% |
| Education & Qualification |    10% |
| Additional Requirements   |    10% |

The score is based only on information available in the resume and job description.

---

## Recruiter Recommendation

The system generates one of the following categories:

* Strong Match
* Potential Match
* Needs Further Review
* Low Match

The recommendation provides supporting information such as:

* Strengths
* Relevant skills
* Relevant experience
* Missing requirements
* Verification areas
* Overall JD alignment

The recommendation is intended to support recruiters and is not an autonomous hiring decision.

---

## Semantic Candidate Search

Candidate professional information is converted into embeddings using:

```text
sentence-transformers/all-MiniLM-L6-v2
```

FAISS is used as the vector database.

Example searches:

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

The system also supports natural-language semantic queries rather than only exact keyword matching.

A relevance threshold is applied to FAISS similarity distance. Lower distance represents greater semantic similarity.

If no sufficiently relevant candidate is found, the system returns:

```text
No sufficiently relevant candidate profiles were found for this search.
```

---

## Error Handling

The application handles:

* Empty resumes
* Incomplete resumes
* Malformed/corrupted PDFs
* PDF extraction failures
* LLM/parser failures
* Missing candidate information
* No relevant semantic-search results

An invalid resume should not prevent valid resumes from being processed.

---

## Privacy and Responsible Use

The system uses only job-relevant professional information.

It should not infer or use protected or unrelated personal characteristics such as:

* Gender
* Religion
* Caste
* Ethnicity
* Disability
* Marital status
* Photograph-based characteristics

Only synthetic, sample, or authorized resumes should be used for testing.

API keys and unnecessary personal information should not be included in logs or submitted files.

---

## Testing

Testing is documented in:

```text
test_log.md
```

The test log covers:

* Resume processing
* Candidate extraction
* Skills extraction
* Experience classification
* JD analysis
* Candidate matching
* Explainable scoring
* Recruiter recommendation
* JSON output
* FAISS vector store
* Semantic search
* No-match search
* Incomplete resume handling
* Malformed PDF handling
* Full pipeline execution

---

## Documentation

Additional implementation strategy is available in:

```text
resume_intelligence_strategy.md
```

It describes the resume processing workflow, LangChain pipeline, prompts, structured outputs, scoring, embeddings, semantic search, and hallucination-control approach.

---

## Known Limitations

* LLM output depends on the quality and completeness of the input documents.
* Semantic search relevance depends on the embedding model and configured similarity threshold.
* Resume extraction quality depends on the PDF structure and readability.
* API rate limits may affect LLM processing.
* Recruiter recommendations require human review before making employment decisions.

---

## Conclusion

This project demonstrates a multi-stage Python and LangChain workflow for resume intelligence, including document processing, structured extraction, JD matching, explainable scoring, recruiter recommendations, embeddings, FAISS vector storage, and semantic candidate search.
