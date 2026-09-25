# Test Log — Intelligent Resume Intelligence Platform

## 1. Resume Processing

**Status:** Passed

### Test Input

* `Kingsly Resume.pdf`
* `Thirukarthikeyan resume.pdf`
* `job_description_1.txt` — Python Backend Developer

### Results

* 2 valid PDF resumes loaded successfully.
* PDF text extraction completed successfully.
* Resume preprocessing completed.
* Candidate information extraction completed.
* Technical skills extraction completed.
* Experience classification completed.
* Job description analysis completed.
* Candidate-to-JD matching completed.
* Explainable scoring completed.
* Recruiter recommendation completed.
* `candidate_profiles.json` generated successfully.
* FAISS vector index generated successfully.

### Candidate Scores

| Candidate                    |    Score | Recommendation       |
| ---------------------------- | -------: | -------------------- |
| CAND001 — Kingsly Wilson K   | 50.7/100 | Needs Further Review |
| CAND002 — THIRUKARTHIKEYAN G | 14.7/100 | Low Match            |

**Status:** PASS

---

## 2. Candidate Information Extraction

**Status:** Passed

### CAND001 — Kingsly Wilson K

* Name: Kingsly Wilson K

* Education: B.Tech — Information Technology
* Institution: Velammal Engineering College
* Graduation Year: 2026
* Certifications: Google AI Certification; C & C++ Programming Certification
* Job Title: Web Development Intern
* Companies: ennoViQ Educator; DLQ Technologies
* Projects: 2

### CAND002 — THIRUKARTHIKEYAN G

* Name: THIRUKARTHIKEYAN G
* Location: Tenkasi District
* Education: B.Tech — Information Technology, Pursuing
* Job Titles: Android App Development Intern; IoT with Embedded Systems In-Plant Trainee
* Projects: 3
* Total Experience: Not available

Missing information was represented using `null`, `Not available`, or empty values rather than fabricated information.

**Status:** PASS

---

## 3. Skills Extraction

**Status:** Passed

### CAND001

* Java
* Python
* JavaScript
* C++
* SQL
* Spring Boot
* React.js
* Node.js
* Spring Data JPA
* MongoDB
* MySQL
* Machine Learning
* AI
* GitHub Copilot
* REST APIs

### CAND002

* Python
* C
* Java
* Kotlin
* Machine Learning
* Data Science
* Data Visualization
* Android Studio
* IoT
* Embedded Systems
* Arduino
* Sensor interfacing
* Microcontroller programming

**Status:** PASS

---

## 4. Experience Classification

**Status:** Passed

### CAND001

* Category: Internship experience
* Total professional experience: 0 years
* Internship/relevant duration: 14 months
* Relevant experience: Web Development Intern

### CAND002

* Category: Internship experience
* Total professional experience: 0 years
* Relevant experience: 0 years
* Internship duration: Not available

**Status:** PASS

---

## 5. Job Description Analysis

**Status:** Passed

### Input

`job_description_1.txt`

### Role

Python Backend Developer

The application successfully analyzed the job description and used the resulting requirements during candidate matching and scoring.

**Status:** PASS

---

## 6. Candidate-to-JD Matching

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

### CAND002

Matched skill:

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

The matching output also included relevant experience, project alignment, qualification alignment, and technology alignment.

**Status:** PASS

---

## 7. Explainable Scoring

**Status:** Passed

The application generated an overall score on a 0–100 scale with category-level scoring and explanations.

### Scoring Weights

| Category                  | Weight |
| ------------------------- | -----: |
| Skills Match              |    40% |
| Relevant Experience       |    25% |
| Projects Alignment        |    15% |
| Education & Qualification |    10% |
| Additional Requirements   |    10% |

### Results

* CAND001: **50.7/100**
* CAND002: **14.7/100**

**Status:** PASS

---

## 8. Recruiter Recommendation

**Status:** Passed

### CAND001

Recommendation:

`Needs Further Review`

### CAND002

Recommendation:

`Low Match`

The recommendation output included strengths, relevant skills/experience, missing requirements, verification areas, and overall JD alignment.

The recommendation is used as recruiter decision support and not as an autonomous hiring decision.

**Status:** PASS

---

## 9. Structured JSON Output

**Status:** Passed

The application successfully generated:

`outputs/candidate_profiles.json`

The output contains structured candidate profiles including:

* Candidate information
* Categorized skills
* Experience classification
* Job match analysis
* Explainable scoring
* Recruiter recommendation

**Status:** PASS

---

## 10. FAISS Vector Store

**Status:** Passed

The application successfully generated the FAISS vector index at:

`outputs/faiss_index`

The embedding model:

`sentence-transformers/all-MiniLM-L6-v2`

loaded successfully.

The application successfully generated embeddings for the candidate profiles.

The existing FAISS index was also successfully loaded using application option `2`.

**Status:** PASS

---

## 11. Semantic Search

**Status:** Passed

### Test 1 — `developer`

Results:

1. CAND001 — Kingsly Wilson K
2. CAND002 — THIRUKARTHIKEYAN G

**Status:** PASS

### Test 2 — `Java developer with Spring Boot experience`

Result:

1. CAND001 — Kingsly Wilson K

Distance:

`1.0856`

CAND001 contains Java and Spring Boot experience.

**Status:** PASS

### Test 3 — `Python backend developer`

Results:

1. CAND001 — Kingsly Wilson K
2. CAND002 — THIRUKARTHIKEYAN G

**Status:** PASS

### Test 4 — `AI and machine learning candidate`

Results:

1. CAND002 — THIRUKARTHIKEYAN G
2. CAND001 — Kingsly Wilson K

CAND002 was returned first and contains Machine Learning and Data Science skills.

**Status:** PASS

### Test 5 — `candidate with React and Node.js experience`

Results:

1. CAND001 — Kingsly Wilson K
2. CAND002 — THIRUKARTHIKEYAN G

CAND001 contains React.js and Node.js.

**Status:** PASS

---

## 12. No Relevant Semantic Search

**Status:** Passed

### Test 1

Query:

`underwater welding specialist`

Result:

```text
No sufficiently relevant candidate profiles were found for this search.
```

**Status:** PASS

### Test 2

Query:

`nuclear reactor engineer`

The query was tested as an unrelated professional search.

The system rejected clearly irrelevant candidates using the semantic similarity threshold.

**Status:** PASS

---

## 13. Incomplete Resume Handling

**Status:** Passed

### Test Input

`incomplete_resume.pdf`

The incomplete resume contained limited information such as:

* Name
* Python
* Java
* B.Tech

### Results

The application handled the incomplete resume without crashing.

Missing candidate information was represented as `null`, `Not available`, or empty values.

The application continued processing the other valid resumes.

The candidate profile output and FAISS processing continued successfully.

**Status:** PASS

---

## 14. Malformed / Corrupted PDF Handling

**Status:** Passed

### Test Input

`malformed_resume.pdf`

The file was intentionally created as an invalid PDF for robustness testing.

### Results

* The application detected the invalid/malformed PDF during extraction.
* The extraction failure was handled without crashing the application.
* Valid resumes continued processing.
* Candidate processing and output generation continued successfully.
* The application remained operational after encountering the malformed file.

**Status:** PASS

---

## 15. Full Pipeline Test

**Status:** Passed

The complete workflow successfully executed:

```text
Resume Loading
    ↓
Text Preprocessing
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
Structured JSON Output
    ↓
FAISS Vector Store
    ↓
Semantic Candidate Search
```

The pipeline successfully handled valid, incomplete, and malformed resume inputs without an application crash.

**Status:** PASS

---

## 16. Notes

* The Hugging Face Hub unauthenticated-request message appeared while loading the embedding model.
* This was a warning and did not prevent embedding generation or FAISS indexing.
* The FAISS vector store was successfully created and loaded.
* Semantic search successfully handled relevant and unrelated queries.
* The relevance threshold successfully prevented clearly unrelated candidates from being returned.
* Incomplete resume handling was tested successfully.
* Malformed PDF handling was tested successfully.
* The test results recorded in this document reflect the application's testing workflow.
* No API keys or `.env` credentials are included in the test log.
