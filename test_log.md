# Test Log — Intelligent Resume Intelligence Platform

## 1. Resume Processing

**Status:** Tested

The application successfully loaded the available PDF resumes from:

`data/resumes/`
## Test: Full Resume Processing + JD Matching

Input:
- Kingsly Resume.pdf
- Thirukarthikeyan resume.pdf
- job_description_1.txt — Python Backend Developer

Results:
- 2 PDF resumes loaded successfully.
- PDF text extraction completed successfully.
- Resume preprocessing completed.
- Candidate information extraction completed.
- Technical skills extraction completed.
- Experience classification completed.
- Job description analysis completed for Python Backend Developer.
- Candidate-to-JD matching completed.
- CAND001 score: 63.9/100
- CAND002 score: 13.7/100
- CAND001 recommendation: Needs Further Review
- CAND002 recommendation: Low Match
- candidate_profiles.json was successfully generated.
- FAISS vector search index was successfully generated.

Status:
PASS

Candidate profiles were generated and stored in:

`outputs/candidate_profiles.json`

---

## 2. FAISS Vector Store

**Status:** Passed

The existing FAISS vector store was successfully loaded using the application.

Output:

```text
Existing FAISS vector store loaded successfully.
```

The embedding model loaded successfully.

---

## 3. Semantic Search

### Test 1 — Query: `developer`

**Result:** 2 candidates found.

* CAND002 — THIRUKARTHIKEYAN G
* CAND001 — Kingsly Wilson K

**Status:** Passed

---

### Test 2 — Query: `Java developer with Spring Boot experience`

**Result:** 2 candidates found.

* CAND001 — Kingsly Wilson K
* CAND002 — THIRUKARTHIKEYAN G

CAND001 was returned first and has Java and Spring Boot skills.

**Status:** Passed

---

### Test 3 — Query: `Python backend developer`

**Result:** 2 candidates found.

* CAND001 — Kingsly Wilson K
* CAND002 — THIRUKARTHIKEYAN G

**Status:** Passed

---

### Test 4 — Query: `AI and machine learning candidate`

**Result:** 2 candidates found.

* CAND002 — THIRUKARTHIKEYAN G
* CAND001 — Kingsly Wilson K

CAND002 was returned first and has Data Science and Machine Learning skills.

**Status:** Passed

---

### Test 5 — Query: `candidate with React and Node.js experience`

**Result:** 2 candidates found.

* CAND001 — Kingsly Wilson K
* CAND002 — THIRUKARTHIKEYAN G

CAND001 was returned first and has React.js and Node.js skills.

**Status:** Passed

---

## 4. Semantic Search Summary

| Test | Query                                       | Result       | Status |
| ---- | ------------------------------------------- | ------------ | ------ |
| 1    | developer                                   | 2 candidates | Passed |
| 2    | Java developer with Spring Boot experience  | 2 candidates | Passed |
| 3    | Python backend developer                    | 2 candidates | Passed |
| 4    | AI and machine learning candidate           | 2 candidates | Passed |
| 5    | candidate with React and Node.js experience | 2 candidates | Passed |

## 5. Notes

The semantic search interface accepts natural-language queries and returns candidate profiles using the FAISS vector store and embedding-based retrieval.

The Hugging Face unauthenticated request message appeared during embedding model loading. It was a warning and did not prevent the application from completing the searches.

Further tests should be added after testing:

* Candidate information extraction
* Skills extraction
* Experience classification
* Job Description analysis
* Candidate-to-JD matching
* Explainable scoring
* Recruiter recommendation
* Invalid/incomplete resume handling
* Malformed PDF handling
* No-relevant-match semantic search

## 6. Candidate Information Extraction

### CAND001 — Kingsly Wilson K

**Status:** Passed

Extracted:

* Name: Kingsly Wilson K
* Email: [wilsonkingsly71@gmail.com](mailto:wilsonkingsly71@gmail.com)
* Phone: +91-7540050379
* Education: B.Tech — Information Technology
* Institution: Velammal Engineering College
* Graduation Year: 2026
* Certifications: Google AI Certification, C & C++ Programming Certification
* Job Title: Web Development Intern
* Companies: ennoViQ Educator, DLQ Technologies
* Projects: 2
* Total Experience: Oct 2023 - Dec 2024

### CAND002 — THIRUKARTHIKEYAN G

**Status:** Passed

Extracted:

* Name: THIRUKARTHIKEYAN G
* Phone: +91 6384160784
* Location: Tenkasi District
* Education: B.Tech — Information Technology, Pursuing
* Job Titles: Android App Development Intern; IoT with Embedded Systems In-Plant Trainee
* Projects: 3
* Total Experience: Not available

Missing values were represented as `null` or `Not available` rather than fabricated values.

---

## 7. Skills Extraction

**Status:** Passed

### CAND001

Programming Languages:

* Java
* Python
* JavaScript
* C++
* SQL

Frameworks:

* Spring Boot
* React.js
* Node.js

Databases:

* MongoDB
* MySQL

Other Technical Skills:

* Git
* Blockchain
* Smart Contracts

### CAND002

Programming Languages:

* Python
* C
* Java
* Kotlin

AI/ML:

* Data Science
* Machine Learning
* Data Visualization

Other Technical Skills:

* Android Studio
* Arduino
* IoT
* Embedded Systems
* Microcontroller programming
* Sensor interfacing
* Android app development

---

## 8. Experience Classification

**Status:** Passed

### CAND001

* Category: Internship experience
* Total professional experience: 0 years
* Internship duration: 14 months
* Relevant experience: Web Development Intern
* Relevant projects: Blockchain-Based Smart City Complaint System; URL Shortener with Analytics

### CAND002

* Category: Internship experience
* Total professional experience: 0 years
* Internship duration: Not available
* Relevant experience: 0 years
* Relevant projects: Breast Cancer Prediction; Tracking Phone Number; Car Parking System

---

## 9. Job Description Analysis

**Status:** Passed

Input:

* `job_description_1.txt`
* Role: Python Backend Developer

The application successfully analyzed the job description and used the resulting JD analysis during candidate matching and scoring.

---

## 10. Candidate-to-JD Matching

**Status:** Passed

### CAND001

Matched skills:

* Python
* REST API development
* Git
* Docker

Missing skills:

* FastAPI
* PostgreSQL
* LangChain
* RAG
* FAISS
* AWS
* Redis

The output also included relevant experience, project alignment, qualification alignment, and technology alignment.

### CAND002

Matched skills:

* Python

Missing skills:

* FastAPI
* REST API development
* PostgreSQL
* Git
* Docker
* LangChain
* RAG
* FAISS
* AWS
* Redis

The output included experience, project, qualification, and technology alignment analysis.

---

## 11. Explainable Scoring

**Status:** Passed

The application generated a 0–100 overall score together with category-level scores, weights, weighted scores, justifications, missing requirements, and a scoring summary.

### CAND001

Overall Score: **63.9/100**

Category weights:

* Skills Match: 40%
* Relevant Experience: 25%
* Projects: 15%
* Education: 10%
* Additional Requirements: 10%

### CAND002

Overall Score: **13.7/100**

Category weights:

* Skills Match: 40%
* Relevant Experience: 25%
* Projects: 15%
* Education: 10%
* Additional Requirements: 10%

Both candidates received explainable scoring information rather than only a single numerical score.

---

## 12. Recruiter Recommendation

**Status:** Passed

### CAND001

Recommendation category:

* Needs Further Review

The output included:

* Key strengths
* Relevant skills
* Relevant experience summary
* Missing requirements
* Areas requiring verification
* Overall JD alignment summary

### CAND002

Recommendation category:

* Low Match

The output included:

* Key strengths
* Relevant skills
* Relevant experience summary
* Missing requirements
* Areas requiring verification
* Overall JD alignment summary

The recommendation stage is presented as recruiter assistance rather than an autonomous hiring decision.

---

## 13. Structured JSON Output

**Status:** Passed

The application successfully generated:

`outputs/candidate_profiles.json`

The JSON contains structured candidate profiles including:

* Candidate information
* Categorized skills
* Experience classification
* Job match analysis
* Explainable scoring
* Recruiter recommendation

Two candidate profiles were successfully stored in the output file.

---

## 14. FAISS Semantic Search

**Status:** Passed

The candidate profiles were successfully converted into embeddings and stored in the FAISS vector index.

The application successfully loaded the embedding model and generated the FAISS index at:

`outputs/faiss_index`

Natural-language candidate searches were successfully performed using the stored candidate embeddings.

---

## 15. Overall Pipeline Test

**Status:** Passed

The complete pipeline successfully processed two resumes against a Python Backend Developer job description.

The workflow completed:

Resume Loading → Preprocessing → Candidate Information Extraction → Skills Extraction → Experience Classification → JD Analysis → Candidate-to-JD Matching → Explainable Scoring → Recruiter Recommendation → Structured JSON Output → FAISS Vector Store

No application crash occurred during the successful full-pipeline run.
