# Student Placement Prediction System

A cascaded ML pipeline that predicts campus placement outcomes and estimates salary packages for placed students, with AI-powered improvement suggestions for students at risk.

> **Note:** Model `.pkl` files are not included in this repo due to size constraints. Train them locally by following the setup instructions below.

---

## Overview

Most placement prediction projects stop at a binary yes/no output. This project goes further — if a student is predicted as **placed**, it estimates their salary package. If **not placed**, it identifies their weak areas and generates personalized improvement suggestions using an LLM.

---

## Architecture

```
Student Profile (16 features)
        ↓
[Random Forest Classifier]
        ↓
   Placed?
   ↙        ↘
 YES          NO
  ↓            ↓
[Linear        Threshold-based
 Regression]   weak area detection
  ↓            ↓
Salary         Groq LLM
Prediction     Suggestions
```

---

## Models

| Model | Algorithm | Metric | Score |
|---|---|---|---|
| Classifier | Random Forest | Recall | 0.78 |
| Regressor | Linear Regression | R² | 0.74 |

Both models share a single `ColumnTransformer` preprocessor (StandardScaler + OneHotEncoder) baked into each pipeline.

---

## Tech Stack

| Layer | Technology |
|---|---|
| ML | Scikit-learn, XGBoost, Pandas, NumPy |
| API | FastAPI + Pydantic |
| Frontend | HTML5, Tailwind CSS, Vanilla JS, Chart.js |
| UI (alt) | Streamlit |
| AI Suggestions | Groq API (Llama 3.1) |
| Deployment | Render |

---

## Project Structure

```
student-placement-predictor/
├── data/
│   └── dataset.csv                    # download from Kaggle (see setup)
├── notebooks/
│   ├── eda.ipynb
│   ├── train_classifier.ipynb
│   └── train_regressor.ipynb
├── src/
│   ├── preprocessing.py               # shared ColumnTransformer
│   ├── predict.py                     # cascade logic (CLI testing)
│   └── api.py                         # FastAPI endpoints
├── models/                            # generated after training (not in repo)
│   ├── classifier.pkl
│   ├── regressor.pkl
│   └── preprocessor.pkl
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── streamlit_app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## API Endpoints

### `POST /predict`
Accepts student profile, returns placement status and salary or weak areas.

**Request:**
```json
{
  "branch": "CSE",
  "college_tier": "Tier-1",
  "cgpa": 8.5,
  "backlogs": 0,
  "coding_skills": 8,
  "dsa_score": 7,
  "aptitude_score": 75,
  "communication_skills": 8,
  "ml_knowledge": 7,
  "system_design": 6,
  "internships": 2,
  "projects_count": 5,
  "certifications": 3,
  "hackathons": 2,
  "open_source_contributions": 1,
  "extracurriculars": 2
}
```

**Response (Placed):**
```json
{
  "status": "Placed",
  "salary": "18.42 LPA"
}
```

**Response (Not Placed):**
```json
{
  "status": "Not Placed",
  "weak_areas": ["dsa_score", "projects_count", "internships"]
}
```

### `POST /suggestions`
Accepts weak areas list, returns AI-generated improvement suggestions.

**Request:**
```json
{
  "weak_areas": ["dsa_score", "projects_count", "internships"]
}
```

---

## Setup & Run

**1. Clone the repo**
```bash
git clone https://github.com/diweshsharma/student_placement_prediction
cd student_placement_prediction
```

**2. Create virtual environment**
```bash
python -m venv myenv
myenv\Scripts\activate  # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set environment variables**
```bash
cp .env.example .env
# Add your GROQ_API_KEY in .env
```

**5. Add dataset**

Download the dataset and place it at `data/dataset.csv`.

**6. Train models**

Run notebooks in order — this generates the `.pkl` files in `models/`:
- `notebooks/train_classifier.ipynb`
- `notebooks/train_regressor.ipynb`

**7. Start FastAPI**
```bash
uvicorn src.api:app --reload
```

**8. Open frontend**

Open `frontend/index.html` in a browser with FastAPI running on port 8000.

Or run Streamlit:
```bash
streamlit run streamlit_app.py
```

---

## Features

- Cascaded pipeline — regressor only runs when classifier predicts placement
- Shared preprocessor across both models — no data leakage
- Input validation via Pydantic with field-level constraints
- CORS enabled for browser-based frontend
- AI suggestions via Groq (Llama 3.1) — only triggered on not-placed result
- Interactive radar chart for skill visualization
- Skeleton loader and toast notifications in frontend

---

## Dataset

Synthetic dataset of 100,000 student records with 16 features covering academic performance, technical skills, and extracurricular activities. Generated for demonstrating the ML pipeline architecture.

---

## Author

**Diwesh Kumar**
B.Tech CSE (AI/ML) — Dronacharya College of Engineering, Gurugram
[GitHub](https://github.com/diweshsharma) · [LinkedIn](https://linkedin.com/in/diweshsharma)
