# Intelligent Resume Intelligence Platform

> **Assignment Title:** Intelligent Resume Intelligence Platform  
> **LLM Provider:** Groq (`ChatGroq`)  
> **Vector Store:** FAISS (`faiss-cpu`)  
> **Embeddings:** HuggingFace Embeddings (`sentence-transformers/all-MiniLM-L6-v2`)  

---

## 📌 Project Overview

The **Intelligent Resume Intelligence Platform** is an enterprise-grade backend application that automates candidate resume parsing, preprocessing, evaluation, scoring, and semantic retrieval against Job Descriptions (JDs).

Built strictly using modern **LangChain**, **Pydantic**, **Groq**, and **FAISS**, the platform provides transparent, explainable 0–100 job-matching scores, recruiter-facing analytical recommendations, and natural language candidate search without fabricating data or introducing demographic bias.

---

## 🛠️ Technology Stack & Versions

- **Python Version**: Python 3.9+
- **LangChain Version**: `langchain>=0.1.0`, `langchain-community`, `langchain-core`, `langchain-groq`
- **Data Validation & Schemas**: `pydantic>=2.0`
- **LLM Provider**: Groq API (`llama-3.3-70b-versatile` or configured model)
- **Embeddings Provider**: `sentence-transformers/all-MiniLM-L6-v2` via `HuggingFaceEmbeddings`
- **Vector Database**: FAISS (`faiss-cpu`)
- **PDF Loader**: `PyPDFLoader` (`pypdf`)
- **Environment Management**: `python-dotenv`

---

## 🧩 LangChain Concepts Used

1. **Document Loaders**: `PyPDFLoader` for multi-page resume loading and page metadata preservation.
2. **Prompt Engineering & Templates**: `PromptTemplate` with external prompt text files for 7 workflow stages.
3. **Structured Output Parsers**:
   - `PydanticOutputParser` for strict schema validation.
   - `JsonOutputParser` for flexible dictionary-based output extraction.
4. **Embeddings**: `HuggingFaceEmbeddings` for generating localized candidate vector representations.
5. **Vector Database & Storage**: `FAISS` vector store creation, local index persistence, and loading.
6. **Retrievers & Semantic Search**: `as_retriever` interface with distance threshold filtering.

---

## 📁 Required Project Structure

```text
Assignment2_Resume_Intelligence_YourName/
│
├── app.py                         # Main entry point & CLI controller
├── resume_loader.py               # PDF resume loading & error handling
├── preprocess.py                  # Text cleaning & artifact removal
│
├── chains/                        # LangChain workflow chains
│   ├── candidate_extraction.py   # Candidate contact & background info
│   ├── skills_extraction.py      # Technical skills categorization
│   ├── experience_classifier.py  # Experience level & duration classification
│   ├── jd_analysis.py            # Job Description requirement extraction
│   ├── job_match.py              # Candidate vs JD comparison
│   ├── scoring.py                # Explainable 0-100 scoring engine
│   └── recommendation.py         # Recruiter recommendation generator
│
├── parsers/                       # Output parsing & schema definitions
│   ├── pydantic_models.py        # Strict Pydantic data schemas
│   └── output_parsers.py         # Pydantic & JSON output parser implementations
│
├── vector_store.py                # Embedding creation & FAISS management
├── semantic_search.py             # Retriever interface & semantic search
│
├── prompts/                       # External prompt templates
│   ├── candidate_extraction_prompt.txt
│   ├── skills_extraction_prompt.txt
│   ├── experience_prompt.txt
│   ├── jd_analysis_prompt.txt
│   ├── job_match_prompt.txt
│   ├── scoring_prompt.txt
│   └── recommendation_prompt.txt
│
├── data/                          # Input data directory
│   ├── resumes/                  # Place candidate PDF resumes here
│   └── job_description/          # Place Job Description (.txt / .pdf) here
│
├── outputs/                       # Output directory
│   └── candidate_profiles.json   # Exported candidate JSON profiles
│
├── resume_intelligence_strategy.md # Complete strategy document
├── test_log.md                    # Evaluation test framework log
├── README.md                      # Application documentation
├── requirements.txt               # Dependencies file
└── .env.example                   # Environment variable template
```

---

## 🚀 Installation & Setup

### 1. Prerequisites
Ensure Python 3.9+ is installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy `.env.example` to `.env` and set your Groq API key:
```bash
cp .env.example .env
```
Inside `.env`:
```env
GROQ_API_KEY=your_actual_groq_api_key_here
GROQ_MODEL_NAME=llama-3.3-70b-versatile
```

---

## 📥 Adding Resumes and Job Description

1. **Add Resumes**: Place candidate PDF resumes inside `data/resumes/`
   Example: `data/resumes/John_Doe_Resume.pdf`, `data/resumes/Jane_Smith.pdf`
2. **Add Job Description**: Place the Job Description inside `data/job_description/`
   Supported formats: `.txt` or `.pdf` (e.g., `data/job_description/jd_backend_engineer.txt`)

---

## 💻 How to Run the Application

Run `app.py` from the root directory:

```bash
python app.py
```

### What happens when you run `app.py`:
1. Scans and loads PDF resumes from `data/resumes/`.
2. Preprocesses raw text (cleans whitespace, fixes line wraps, filters artifacts).
3. Reads and analyzes the Job Description from `data/job_description/`.
4. Executes multi-stage chain evaluation for each candidate.
5. Saves structured results to `outputs/candidate_profiles.json`.
6. Generates FAISS vector embeddings index in `outputs/faiss_index/`.
7. Launches interactive semantic candidate search CLI.

---

## 📊 How Scoring Works

The Explainable Scoring Engine computes a transparent `0.0 to 100.0` score based on five weighted categories:

1. **Skills Match (40%)**: Matched skills vs JD required/preferred skills.
2. **Relevant Experience (25%)**: Alignment of total/relevant experience with JD requirement.
3. **Projects Alignment (15%)**: Project experience relevance to JD responsibilities.
4. **Education (10%)**: Degree and field of study match.
5. **Additional Requirements (10%)**: Certifications, cloud/DevOps, and domain exposure.

$$\text{Overall Score} = \sum (\text{Category Score} \times \text{Weight})$$

---

## 🔍 How Semantic Search Works

- Candidate professional information (skills, experience, projects, certifications) is converted into 384-dimensional vector embeddings using `sentence-transformers/all-MiniLM-L6-v2`.
- Embeddings are indexed into a FAISS vector database.
- Queries are executed using LangChain Retriever with similarity distance thresholding (`threshold = 1.45`).
- If no candidate profile meets the similarity threshold, the search returns:
  `"No sufficiently relevant candidate profiles were found for this search."`

### Example Search Queries:
- `"Find candidates with LangChain + FastAPI experience."`
- `"Find candidates with Python backend development and MySQL skills."`
- `"Find candidates who have worked on RAG projects."`
- `"Find candidates with Java, Spring Boot, and microservices experience."`

---

## ⚠️ Known Limitations

1. **Scanned PDF Text**: PyPDFLoader extracts text-based PDFs. Image-only scanned PDFs require OCR preprocessing before extraction.
2. **API Rate Limits**: Large resume batches (50+ resumes) may hit Groq LLM rate limits if run concurrently; sequential processing with retry logic is implemented to mitigate this.
3. **Local Embedding Speed**: The initial run downloads the lightweight HuggingFace MiniLM model (~90MB) once for offline embedding generation.
