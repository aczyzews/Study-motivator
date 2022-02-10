import sklearn.pipeline as pipeline_sklearn
import joblib
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler

class PipelineLocal:
    def __init__(self):
        self.pipeline=pipeline_sklearn.Pipeline([
            ('imputer',SimpleImputer(strategy="median")),
            ('scaler',MinMaxScaler()),
        ])

import os
class MLPredictor:
    def __init__(self):
        self.sgdc_model = joblib.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'sgdc_model.pkl'))
        self.linreg_model=joblib.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),'linreg_model.pkl'))


    def predict(self,sex,age,address,studytime,freetime,goout,weekly_alcohol,weekend_alcohol,health,activity_type):

        if (studytime<2):
            studytime_class=1
        elif(studytime>=2 and studytime<5):
            studytime_class=2
        elif (studytime >= 5 and studytime < 10):
            studytime_class = 3
        else:
            studytime_class=4
        pipelined_data = PipelineLocal().pipeline.fit_transform([[sex, age, address, studytime_class, freetime, goout, weekly_alcohol, weekend_alcohol, health, activity_type]])
        score=self.linreg_model.predict([[studytime]])*0.55+self.sgdc_model.predict([[sex, age, address, studytime_class, freetime, goout, weekly_alcohol, weekend_alcohol, health, activity_type]])
        if(score>100):
            score=100
        if(score<0):
            score=0
        return int(score)


