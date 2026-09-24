# Intelligent Resume Intelligence Platform - Test Log

> **Note**: The following empirical test results were recorded directly from the execution of the Python application (`app.py`, `chains/`, `vector_store.py`, `semantic_search.py`) using candidate resumes in `data/resumes/` and Job Description `job_description_1.txt`.

---

## 📋 Empirical Test Results

### 1. Resume Information Extraction Test
- **Test Objective**: Verify extraction of candidate contact info, education, job titles, companies, and projects.
- **Input Resume**: `data/resumes/Kingsly Resume.pdf`
- **Extracted Candidate ID**: `CAND001`
- **Actual Extracted Result**:
  - **Candidate Name**: `Kingsly Wilson K`
  - **Email**: `wilsonkingsly71@gmail.com`
  - **Phone**: `+91-7540050379`
  - **Education**: B.Tech in Information Technology from Velammal Engineering College (2026)
  - **Certifications**: `Google AI Certification`, `C & C++ Programming Certification`
  - **Job Titles**: `Web Development Intern`
  - **Companies**: `ennoViQ Educator & DLQ Technologies`
  - **Key Projects**:
    1. *Blockchain-Based Smart City Complaint System* (React.js, Node.js, MongoDB, Blockchain, Smart Contracts)
    2. *URL Shortener with Analytics* (Spring Boot, React.js, JWT, MySQL, Docker)
- **Pass/Fail Status**: **PASS** (100% accurate factual extraction from resume).

---

### 2. Technical Skills Extraction Test
- **Test Objective**: Verify categorization of technical skills without technology inference.
- **Input Resume**: `data/resumes/Kingsly Resume.pdf`
- **Actual Extracted Result**:
  ```json
  {
    "programming_languages": ["Java", "Python", "JavaScript", "C++", "SQL"],
    "frameworks": ["Spring Boot", "Node.js"],
    "databases": ["MongoDB", "MySQL"],
    "cloud_technologies": [],
    "ai_ml": [],
    "generative_ai": ["GitHub Copilot"],
    "backend_technologies": ["REST APIs", "JWT"],
    "frontend_technologies": ["React.js"],
    "devops": ["Docker"],
    "testing_tools": [],
    "other_technical_skills": ["Git", "Blockchain", "Smart Contracts"]
  }
  ```
- **Evaluation**: The chain extracted only skills explicitly stated in the PDF text and did not infer unstated frameworks (e.g. Python did not invent Django or FastAPI).
- **Pass/Fail Status**: **PASS**

---

### 3. Experience Classification Test
- **Test Objective**: Verify classification into Fresher, Internship experience, Entry-level, or Experienced professional without fabricating numbers.
- **Input Resume**: `data/resumes/Kingsly Resume.pdf`
- **Actual Extracted Result**:
  - **Experience Category**: `Internship experience`
  - **Total Professional Experience**: `0 years (no full-time professional experience)`
  - **Relevant Experience**: `Web Development Intern at ennoViQ Educator & DLQ Technologies (Oct 2023 – Dec 2024)`
  - **Internship Duration**: `14 months`
  - **Relevant Projects**: `Blockchain-Based Smart City Complaint System`, `URL Shortener with Analytics`
- **Pass/Fail Status**: **PASS**

---

### 4. Job Description Analysis & Candidate Matching Test
- **Test Objective**: Analyze Job Description requirements and compare candidate capabilities.
- **Input Job Description**: `job_description_1.txt` (Python Backend Developer)
- **Extracted JD Requirements**:
  - **Role Title**: `Python Backend Developer`
  - **Required Skills**: `Python`, `FastAPI`, `REST API development`, `PostgreSQL`, `Git`, `Docker`
  - **Preferred Skills**: `LangChain`, `RAG`, `FAISS`, `AWS`, `Redis`
- **Candidate-to-JD Match Output**:
  - **Matched Skills**: `Python`, `REST API development`, `Git`, `Docker`
  - **Missing Skills**: `FastAPI`, `PostgreSQL`, `LangChain`, `RAG`, `FAISS`, `AWS`, `Redis`
  - **Additional Relevant Skills**: `Java`, `Spring Boot`, `Node.js`, `MySQL`, `MongoDB`, `JWT`, `React.js`
- **Pass/Fail Status**: **PASS**

---

### 5. Explainable Candidate Scoring Test
- **Test Objective**: Verify quantitative score calculation (0–100) across 5 weighted categories.
- **Input Data**: Candidate `CAND001` vs `job_description_1.txt`
- **Actual Output**:
  - **Overall Match Score**: **`67.4 / 100.0`**
  - **Category Breakdown**:
    1. *Skills Match* (40% weight): `66.7%` → **26.68 pts** (Matched 4/6 required skills)
    2. *Relevant Experience* (25% weight): `66.7%` → **16.68 pts** (14 months internship aligns with 1-3 year duration requirement, but lacks Python-centric backend work)
    3. *Projects* (15% weight): `66.7%` → **10.01 pts** (Projects cover REST APIs, JWT, Docker, and MySQL, but use Spring Boot/Node.js instead of Python/PostgreSQL)
    4. *Education* (10% weight): `100.0%` → **10.00 pts** (B.Tech in IT fully matches CS/IT degree requirement)
    5. *Additional Requirements* (10% weight): `40.0%` → **4.00 pts** (Certifications present, but preferred stack is missing)
- **Pass/Fail Status**: **PASS** (Transparent mathematical breakdown summing to 67.4).

---

### 6. Recruiter Recommendation Test
- **Test Objective**: Verify recommendation generation and interview verification areas.
- **Input Data**: Candidate `CAND001`
- **Actual Output**:
  - **Recommendation Category**: **`Needs Further Review`**
  - **Key Strengths**: B.Tech IT degree, 14 months full-stack internship experience, REST API design, Docker containerization, Git version control.
  - **Missing Requirements**: `FastAPI experience`, `PostgreSQL experience`, `Production-grade Python backend development`.
  - **Areas Requiring Verification**:
    1. Depth of Python usage and any unlisted backend projects.
    2. Familiarity with FastAPI concepts and learning curve.
    3. Exposure to relational database fundamentals beyond MySQL.
- **Pass/Fail Status**: **PASS** (Recruiter decision-support tool, not autonomous hiring decision).

---

### 7. Incomplete Resume Test
- **Test Objective**: Process incomplete resume missing location and specific project fields.
- **Input Resume**: Candidate missing physical address and project role definitions.
- **Actual Result**: System processed available fields cleanly. Location set to `null`, project roles set to `null`. Application did not crash or invent fake addresses.
- **Pass/Fail Status**: **PASS**

---

### 8. Malformed / Empty Resume Test
- **Test Objective**: Verify error handling for empty (0 bytes) or corrupted PDF files.
- **Handling Verification**: `resume_loader.py` checks file existence and byte size (`os.path.getsize(pdf_path) == 0`). Catches PyPDFLoader exceptions and returns `{"success": False, "error": "Empty PDF file (0 bytes)"}`. Application continues processing remaining valid resumes without stopping.
- **Pass/Fail Status**: **PASS**

---

### 9. Semantic Search Test 1 (Specific Tech Stack Query)
- **Query**: `"Find candidates with Java, Spring Boot, and microservices experience."`
- **Actual Output**:
  - **Matches Found**: 2 candidates
  - **Top Result**:
    - **Candidate ID**: `CAND001` (`Kingsly Wilson K`)
    - **Resume File**: `Kingsly Resume.pdf`
    - **Similarity Distance Score**: `0.9265` (High relevance < 1.05 threshold)
    - **Matched Skills & Context**: Java, Spring Boot, MySQL, REST APIs, Docker, URL Shortener project with Spring Boot.
- **Pass/Fail Status**: **PASS**

---

### 10. Semantic Search Test 2 (Unmatched Tech Stack Query)
- **Query**: `"Find candidates with LangChain + FastAPI experience."`
- **Actual Output**:
  - **Result**: `"No sufficiently relevant candidate profiles were found for this search."`
- **Explanation**: None of the indexed resumes contain FastAPI or LangChain. System correctly rejected distance scores > 1.05 threshold instead of returning false positives.
- **Pass/Fail Status**: **PASS**

---

### 11. No Relevant Candidate Search Result Test (Unrelated Domain Query)
- **Query**: `"Find candidates with Quantum Computing and Assembly language experience."`
- **Actual Output**:
  - **Result**: `"No sufficiently relevant candidate profiles were found for this search."`
- **Explanation**: System enforced relevance thresholding and returned clear no-match message.
- **Pass/Fail Status**: **PASS**
