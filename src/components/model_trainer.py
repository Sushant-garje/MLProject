import os
import numpy as np
import pandas as pd
import sys
from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor,GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from catboost import CatBoostRegressor
from xgboost import XGBRegressor
from src.utils import save_object,evaluate_models
from sklearn.metrics import r2_score


@dataclass
class ModelTrainerConfig:
    model_file_path = os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.config = ModelTrainerConfig()

    def initiate_model_training(self,train_arr,test_arr):

       try:
           X_train,y_train,X_test,y_test = (
               train_arr[:,:-1],
               train_arr[:,-1],
               test_arr[:,:-1],
               test_arr[:,-1]
           )


           models = {
               "DecisionTree": DecisionTreeRegressor(),
               "RandomForest": RandomForestRegressor(),
               "GradientBoosting": GradientBoostingRegressor(),
               "linear regrassion": LinearRegression(),
               "XGB": XGBRegressor(),
               "CatBoost": CatBoostRegressor(verbose=False),
               "AdaBoost": AdaBoostRegressor(),
           }

           params = {
               "Decision Tree": {
                   'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                   # 'splitter':['best','random'],
                   # 'max_features':['sqrt','log2'],
               },
               "Random Forest": {
                   # 'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],

                   # 'max_features':['sqrt','log2',None],
                   'n_estimators': [8, 16, 32, 64, 128, 256]
               },
               "Gradient Boosting": {
                   # 'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                   'learning_rate': [.1, .01, .05, .001],
                   'subsample': [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                   # 'criterion':['squared_error', 'friedman_mse'],
                   # 'max_features':['auto','sqrt','log2'],
                   'n_estimators': [8, 16, 32, 64, 128, 256]
               },
               "Linear Regression": {},
               "XGBRegressor": {
                   'learning_rate': [.1, .01, .05, .001],
                   'n_estimators': [8, 16, 32, 64, 128, 256]
               },
               "CatBoosting Regressor": {
                   'depth': [6, 8, 10],
                   'learning_rate': [0.01, 0.05, 0.1],
                   'iterations': [30, 50, 100]
               },
               "AdaBoost Regressor": {
                   'learning_rate': [.1, .01, 0.5, .001],
                   # 'loss':['linear','square','exponential'],
                   'n_estimators': [8, 16, 32, 64, 128, 256]
               }

           }

           model_report: dict = evaluate_models(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test,
                                                models=models, param=params)

           ## to get best model score from dictonary
           best_model_score  = max(sorted(model_report.values()))

           ## To get best model name from dict

           best_model_name = list(model_report.keys())[
               list(model_report.values()).index(best_model_score)
           ]

           best_model = models[best_model_name]

           if best_model_score <0.6:
               raise CustomException("NO best model found")

           logging.info(f"Best found model on both training and testing dataset")

           save_object(
               file_path=self.config.model_file_path,
               obj=best_model
           )


           predicted = best_model.predict(X_test)

           r2_square = r2_score(y_test, predicted)

           return r2_square


       except Exception as e:
           raise CustomException(e,sys)