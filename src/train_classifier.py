import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold,cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report , confusion_matrix , roc_curve, roc_auc_score




data = pd.read_csv('../dataset/student.csv')



from preprocessing import preprocess
preprocessor = preprocess()





X=data.drop(columns=['placement_status', 'salary_package_lpa'])
y = data['placement_status']





X_train,X_test,y_train,y_test= train_test_split(X,y,test_size = 0.2, random_state=42, stratify = y)




scale = 31525 / 68475
candidates = {
    'Logistic Regression' : LogisticRegression(C = 1.0, class_weight ='balanced', max_iter = 1000, random_state =42 ),
    'Random ForestClassifier' : RandomForestClassifier(n_estimators = 100, class_weight = 'balanced' , random_state = 42, n_jobs = -1),
    'XGboost': XGBClassifier(n_estimators = 100, learning_rate = 0.1,max_depth = 6, random_state = 42, n_jobs = -1, scale_pos_weight=scale)
}





cv =StratifiedKFold(n_splits= 5, shuffle = True, random_state = 42)
results = []




for name, model in candidates.items():
    pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', model)])
    roc_auc = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="roc_auc").mean()
    accur = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="accuracy").mean()
    prec = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="precision").mean()
    rec = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="recall").mean()
    results.append({"model": name, "roc_auc": roc_auc, "accuracy": accur,
                        "precision": prec, "recall": rec, "clf": model})
    print(f"{name:<22} {roc_auc:>8.4f} {accur:>8.4f} {prec:>9.4f} {rec:>8.4f}")




best = max(results, key = lambda x: x['recall'])
print(best['model'])





best_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', best['clf'])
])

best_pipeline.fit(X_train, y_train)




y_pred = best_pipeline.predict(X_test)
print(classification_report(y_test,y_pred))




import joblib
joblib.dump(best_pipeline, '../models/classifier.pkl')
print('Classifier model saved')

