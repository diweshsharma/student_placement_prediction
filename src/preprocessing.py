import pandas as pd
from sklearn.preprocessing import StandardScaler , OneHotEncoder
from sklearn.compose import ColumnTransformer

categorical =[
    'branch',
    'college_tier'
]

numerical =[
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

def preprocess():
    return ColumnTransformer(
        transformers=[(
            'encoder',
            OneHotEncoder(handle_unknown = 'ignore' ),
            categorical
            
        ),
        ('scaler',
         StandardScaler(),
         numerical
            
        )              
            
        ]
        
    )
    
    
