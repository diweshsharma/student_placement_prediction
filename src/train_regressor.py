import pandas as pd
from sklearn.model_selection import train_test_split,KFold,cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score




data = pd.read_csv('dataset/student.csv')




from src.preprocessing import preprocess
preprocessor = preprocess()




placed_data = data[data['placement_status']== 1]
x = placed_data.drop(columns=['placement_status', 'salary_package_lpa'])
y= placed_data['salary_package_lpa']




x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2, random_state = 42)



candidates ={
    'Linear Regression' : LinearRegression(),
    'Random ForestRegressor': RandomForestRegressor(n_estimators=100,
        random_state=42,
        n_jobs=-1),
    'XGB Regressor' : XGBRegressor(n_estimators=100,
        learning_rate=0.1,
        max_depth=6,
        random_state=42,
        n_jobs=-1)
}





cv = KFold(shuffle = True, n_splits = 5, random_state = 42)
results =[]





for name,models in candidates.items():
    pipeline =Pipeline(steps=[('preprocessor' , preprocessor),('regressor',models)])
    r2 = cross_val_score(pipeline,x_train,y_train,cv =cv , scoring ='r2').mean()
    mae= cross_val_score(pipeline,x_train,y_train,cv =cv , scoring ='neg_mean_absolute_error').mean()
    rmse= cross_val_score(pipeline,x_train,y_train,cv =cv , scoring ='neg_root_mean_squared_error').mean()
    results.append({'model': name, 'r2': r2 , 'neg_mean_absolute_error' : mae, 'neg_root_mean_squared_error' : rmse , 'reg' : models})
    print(f"{name} {r2} {-1*mae} {-1*rmse}")




print(results[0])



best = max(results, key = lambda x: x['r2'])
best_pipeline_reg = Pipeline(steps=[('preprocessor' , preprocessor),
                                ('regressor' , best['reg'])])
best_pipeline_reg.fit(x_train,y_train)
y_pred = best_pipeline_reg.predict(x_test)
print('score' , r2_score(y_pred, y_test))


# In[26]:


import joblib
joblib.dump(best_pipeline_reg, 'models/regressor.pkl')


# In[ ]:




