# Test Log — Intelligent Resume Intelligence Platform

## 1. Resume Processing

**Status:** Tested

The application successfully loaded the available PDF resumes from:

`data/resumes/`

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
