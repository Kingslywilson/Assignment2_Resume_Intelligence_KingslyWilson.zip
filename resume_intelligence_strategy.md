# Intelligent Resume Intelligence Platform - Strategy Document

## 1. Executive Overview

The **Intelligent Resume Intelligence Platform** is an enterprise-grade, multi-stage NLP and LLM pipeline built with **LangChain**, **Pydantic**, **FAISS**, and **Groq LLM**. It processes, parses, evaluates, scores, and indexes candidate resumes against Job Descriptions (JDs) with total transparency, zero hallucination, strict schema validation, and semantic search capability.

---

## 2. System Architecture & Workflow

The platform follows a modular 12-step architecture:

```text
Resume PDF
   ↓
PyPDFLoader (resume_loader.py)
   ↓
Text Preprocessing (preprocess.py)
   ↓
Candidate Information Extraction Chain (chains/candidate_extraction.py)
   ↓
Skills Extraction Chain (chains/skills_extraction.py)
   ↓
Experience Classification Chain (chains/experience_classifier.py)
   ↓
Job Description Analysis Chain (chains/jd_analysis.py)
   ↓
Candidate-to-JD Matching Chain (chains/job_match.py)
   ↓
Explainable Scoring Engine (chains/scoring.py)
   ↓
Recruiter Recommendation Chain (chains/recommendation.py)
   ↓
Structured Candidate Profile JSON (outputs/candidate_profiles.json)
   ↓
FAISS Vector Database Indexing (vector_store.py)
   ↓
LangChain Retriever & Semantic Candidate Search (semantic_search.py)
```

---

## 3. Resume Processing & Preprocessing Strategy

### 3.1 PDF Loading (`resume_loader.py`)
- **PyPDFLoader Integration**: Loads multi-page PDF documents page-by-page.
- **Candidate ID Generation**: Automatically assigns unique candidate identifiers (e.g. `CAND001`, `CAND002`).
- **Metadata Preservation**: Preserves original filename, full filepath, page numbers, and document metadata.
- **Fault Tolerance & Resilience**:
  - Handles zero-byte empty files, corrupted PDFs, unreadable formatted PDFs, scanned non-extractable PDFs.
  - Catches extraction errors per file and logs clear diagnostic failure messages.
  - Continues processing valid resumes without interrupting or crashing the complete application.

### 3.2 Preprocessing Pipeline (`preprocess.py`)
- **Artifact Cleanup**: Strips non-printable control characters, bullet symbols, and extraction glyphs while preserving code/math notation.
- **Hyphenation Repair**: Fixes words broken across line wraps (e.g., `devel-\nopment` → `development`).
- **Whitespace Normalization**: Collapses horizontal tabs/multiple spaces into single spaces and caps consecutive empty lines at 2.
- **Header/Footer & Duplicate Filtering**: Identifies and removes repeated page headers, footers (e.g., "Page 1 of 3"), and duplicate adjacent text.
- **Information Integrity**: Strictly retains all meaningful candidate content (work history, project details, skills).

---

## 4. Multi-Stage LangChain Workflow & Stage Data Flow

Each pipeline stage operates as a dedicated LangChain module with isolated prompts and output parsers:

| Stage | Module | Prompt File | Output Parser | Data Inputs | Data Outputs |
|---|---|---|---|---|---|
| **1. Candidate Extraction** | `candidate_extraction.py` | `candidate_extraction_prompt.txt` | `PydanticOutputParser` | Preprocessed Resume Text | `CandidateInfo` model |
| **2. Skills Extraction** | `skills_extraction.py` | `skills_extraction_prompt.txt` | `PydanticOutputParser` | Preprocessed Resume Text | `SkillsCategorized` model |
| **3. Experience Classification** | `experience_classifier.py` | `experience_prompt.txt` | `JsonOutputParser` | Preprocessed Resume Text | `ExperienceClassification` model |
| **4. JD Analysis** | `jd_analysis.py` | `jd_analysis_prompt.txt` | `PydanticOutputParser` | Raw Job Description Text | `JobDescriptionAnalysis` model |
| **5. Candidate Matching** | `job_match.py` | `job_match_prompt.txt` | `JsonOutputParser` | Candidate Profile + JD Analysis | `JobMatchAnalysis` model |
| **6. Explainable Scoring** | `scoring.py` | `scoring_prompt.txt` | `PydanticOutputParser` | Candidate Profile + Job Match | `ExplainableScoring` model |
| **7. Recommendation** | `recommendation.py` | `recommendation_prompt.txt` | `PydanticOutputParser` | Scoring + Job Match + JD Analysis | `RecruiterRecommendation` model |

---

## 5. Prompt Engineering & Hallucination Prevention

### 5.1 Design Principles
- **Explicit Role & Constraint Enforcement**: Every prompt in `prompts/` explicitly defines the agent's role, task, inputs, rules, constraints, and format instructions.
- **Anti-Hallucination Directives**: Prompts explicitly forbid inferring or fabricating unmentioned tools, degrees, years of experience, or projects.
- **Non-Inference Rule**: Mentioning a language (e.g., `Python`) strictly DOES NOT imply associated frameworks (e.g., `Django`, `Flask`, or `FastAPI`) unless explicitly written in the resume.
- **Missing Information Treatment**: Unstated fields are strictly populated as `null`, `"Not available"`, or empty lists `[]`.
- **Responsible Candidate Evaluation**: Strictly prevents bias or demographic inference. Excludes gender, age, religion, caste, ethnicity, marital status, photograph analysis, or name-based assumptions.

---

## 6. Structured Output & Parser Error Handling

### 6.1 Demonstration of Dual Output Parsers
- **`PydanticOutputParser`**: Used for strict schema validation across Candidate Info, Skills, JD Analysis, Scoring, and Recommendation stages.
- **`JsonOutputParser`**: Used for flexible structural extraction in Experience Classification and Candidate-to-JD Matching stages.

### 6.2 Parser Repair & Resilience (`parsers/output_parsers.py`)
- **Markdown Fence Stripping**: Automatically strips ```json ... ``` code blocks from raw LLM strings.
- **Multi-Level Retry Strategy**:
  1. LangChain parser parsing.
  2. Native `json.loads` parsing.
  3. Regex JSON block extraction (`\{[\s\S]*\}`).
  4. Safe fallback default instantiation.
- Prevents invalid JSON formatting from crashing the pipeline.

---

## 7. Explainable Scoring Framework

Scores are computed strictly on a `0.0 to 100.0` scale using five documented, job-relevant categories:

$$\text{Overall Match Score} = \sum_{i=1}^{5} \left( \text{Category Score}_i \times \text{Weight}_i \right)$$

### 7.1 Weight Allocation

| Category | Weight (%) | Criteria & Basis for Score |
|---|---|---|
| **Skills Match** | **40%** | Ratio of matched candidate technical skills to JD mandatory and preferred skills. |
| **Relevant Experience** | **25%** | Alignment of professional work duration and domain history with JD required experience. |
| **Projects Alignment** | **15%** | Relevance of candidate projects and applied technologies to JD role responsibilities. |
| **Education & Qualification** | **10%** | Degree, specialization, and qualification alignment with JD education criteria. |
| **Additional Requirements** | **10%** | Certifications, cloud/DevOps exposure, and secondary domain competencies. |

---

## 8. Recruiter Recommendation Categories

Candidates are categorized into four clear analytical categories:
- **Strong Match**: Meets or exceeds skills, experience, and educational requirements.
- **Potential Match**: Strong core skills with minor experience or non-critical skill gaps.
- **Needs Further Review**: Partial alignment requiring recruiter/interview verification.
- **Low Match**: Significant missing skills or experience mismatches.

*Note: All recommendations are analytical decision-support tools and do not represent automated hiring decisions.*

---

## 9. Vector Database & Semantic Candidate Search

### 9.1 Embeddings Provider & Model
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2` via `HuggingFaceEmbeddings`.
- **Privacy & Security**: Embedded text contains strictly professional skills, experience, projects, certifications, and role history. Excludes email, phone number, and physical address.

### 9.2 Vector Database
- **FAISS (`faiss-cpu`)**: Stores candidate vector representations locally in `outputs/faiss_index/`.
- **Metadata Included**: `candidate_id`, `candidate_name`, `resume_filename`, `skills_summary`, `experience_category`, `total_experience`.

### 9.3 Retriever & Semantic Candidate Search

- Uses LangChain's vector store retriever interface with FAISS.
- Uses similarity-based retrieval to find the top-k candidate profiles relevant to a natural-language query.
- The retriever is configured using LangChain's `as_retriever()` interface.
- Candidate results are ranked according to semantic similarity between the query and the professional candidate profile embeddings.
- The search focuses on professional information such as skills, experience, projects, technologies, certifications, and role history.
- Personal contact information such as email address, phone number, and physical address is not used as semantic search content.
- If the vector index is unavailable, empty, or the search produces no documents, the system returns:

  `"No sufficiently relevant candidate profiles were found for this search."`
