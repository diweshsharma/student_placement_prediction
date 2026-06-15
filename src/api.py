import joblib
import os
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel , Field
from typing import Literal
from groq import Groq
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
classifier = joblib.load(os.path.join(BASE_DIR, '..', 'models', 'classifier.pkl'))
regressor  = joblib.load(os.path.join(BASE_DIR, '..', 'models', 'regressor.pkl'))

class predict(BaseModel):
    branch : Literal['CE', 'CSE', 'Chemical', 'ECE', 'EE', 'IT', 'ME']
    college_tier : Literal['Tier-1', 'Tier-2', 'Tier-3']
    cgpa: float = Field(...,gt = 0, le = 10.0, description="CGPA On The Scale of 10")
    backlogs: int = Field(...,le = 10)
    coding_skills: int = Field(...,ge =1,le = 10 ,description = 'Scale Your Skills On The Scale Of 10')
    dsa_score : float = Field(...,le = 10.0)
    aptitude_score : float = Field(...,lt=100.0)
    communication_skills: float = Field(...,le = 10.0 , description = 'Rate your communication skills on the scale of 10') 
    ml_knowledge :float = Field(...,le = 10.0 , description = 'Rate your ML Knowledge on the scale of 10') 
    system_design :float = Field(...,le = 10.0 , description = 'Rate your System Desigh on the scale of 10') 
    internships : int 
    projects_count : int
    certifications : int
    hackathons : int
    open_source_contributions : int
    extracurriculars : int = Field(...,ge =0, le=3)
    

@app.get("/")
def root():
    return {"message": "Student Placement Prediction API is running"}
@app.post('/predict')
def prediction(stud:predict):
    student =stud.model_dump()
    data = pd.DataFrame([student])
    
    thresholds = {
    'cgpa': 6.5,
    'backlogs': 3,          
    'coding_skills': 5,
    'dsa_score': 5,
    'aptitude_score': 50,
    'communication_skills': 5,
    'ml_knowledge': 4,
    'system_design': 4,
    'internships': 1,
    'projects_count': 3,
    'certifications': 2,
    'hackathons': 1,
    'open_source_contributions': 1,
    'extracurriculars': 1
    
}
    pred = classifier.predict(data)[0]
    if (pred == 1):
        reg_pred = regressor.predict(data)[0]
        return {'status': "Placed", 'salary': f"{round(float(reg_pred),2)} lpa"}
    else:
        weak_areas = []
        for feature, threshold in thresholds.items():
            if feature == 'backlogs':
                if student[feature] > threshold:
                    weak_areas.append(feature)
            else:
                if student[feature] < threshold:
                    weak_areas.append(feature)
                  
                    
        return {"status": "Not Placed", "weak_areas": weak_areas}
    
class WeakAreas(BaseModel):
    weak_areas: list[str]


@app.post('/suggestions')
def get_suggestions(data: WeakAreas):
    load_dotenv()
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": f"""
            A student is not getting placed in campus recruitment.
            Their weak areas are: {', '.join(data.weak_areas)}
            
            Give specific, actionable suggestions to improve each weak area.
            Keep it concise - 2 to 3 lines per weak area.
            Format as bullet points.
            """
        }]
    )
    
    return {"suggestions": response.choices[0].message.content}