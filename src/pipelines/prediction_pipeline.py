import os.path
import sys
import pandas as pd
import numpy as np
from src.logger import logging
from src.exception import CustomException

from sklearn.preprocessing import StandardScaler
from src.utils import load_obj

class PredictionPipeline():
    def __init__(self):
        pass

    def predict(self,features):

        try:
            model_path = os.path.join("src/components/artifacts", "model.pkl")
            preprocessor_path = os.path.join("src/components/artifacts", "preprocessor.pkl")

            model = load_obj(model_path)
            preprocessor = load_obj(preprocessor_path)

            scaled_data = preprocessor.transform(features)
            predict = model.predict(scaled_data)

            return predict
        except Exception as e:
            raise CustomException(e,sys)



class CustomData():
    def __init__(self,
                 gender: str,
                 race_ethnicity: str,
                 parental_level_of_education,
                 lunch: str,
                 test_preparation_course: str,
                 reading_score: int,
                 writing_score: int):

        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score

    def get_data_as_dataframe(self):

       try:
           custom_data_input_dict = {
               "gender": [self.gender],
               "race_ethnicity": [self.race_ethnicity],
               "parental_level_of_education": [self.parental_level_of_education],
               "lunch": [self.lunch],
               "test_preparation_course": [self.test_preparation_course],
               "reading_score": [self.reading_score],
               "writing_score": [self.writing_score]
           }

           dataframe = pd.DataFrame(custom_data_input_dict)

           return dataframe

       except Exception as e:
           raise CustomException(e,sys)
