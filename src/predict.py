import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
classifier = joblib.load(os.path.join(BASE_DIR, '..', 'models', 'classifier.pkl'))
regressor  = joblib.load(os.path.join(BASE_DIR, '..', 'models', 'regressor.pkl'))

features = [
    "branch",
    "college_tier",
    "cgpa",
    "backlogs",
    "coding_skills",
    "dsa_score",
    "aptitude_score",
    "communication_skills",
    "ml_knowledge",
    "system_design",
    "internships",
    "projects_count",
    "certifications",
    "hackathons",
    "open_source_contributions",
    "extracurriculars"
]

student = {}
numerical = [
    "cgpa", "backlogs", "coding_skills", "dsa_score", "aptitude_score",
    "communication_skills", "ml_knowledge", "system_design", "internships",
    "projects_count", "certifications", "hackathons", "open_source_contributions",
    "extracurriculars"
]
categorical = ["branch", "college_tier"]

student = {}

for feature in features:
    val = input(f"Enter {feature}: ")
    student[feature] = val if feature in categorical else float(val)


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
    'extracurriculars': 2
}
  
data = pd.DataFrame([student])
pred = classifier.predict(data)
if (pred == 1):
    reg_pred = regressor.predict(data)
    print(f"Student will be placed | Predicted Salary Package: {reg_pred[0]:.2f} LPA")
else:
    print('Less probability of getting placed')
    weak_areas = []
for feature, threshold in thresholds.items():
    if feature == 'backlogs':
        if student[feature] > threshold:
            weak_areas.append(feature)
    else:
        if student[feature] < threshold:
            weak_areas.append(feature)

print(f"Weak areas to improve: {weak_areas}")
  
    
    
# encoder = classifier.named_steps['preprocessor'].named_transformers_['encoder']
# print(encoder.categories_)

