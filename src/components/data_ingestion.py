import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from data_tranformation import DataTransformation
from model_trainer import ModelTrainer

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join("artifacts","train.csv")
    print(train_data_path)
    test_data_path: str = os.path.join("artifacts","test.csv")
    raw_data_path: str = os.path.join("artifacts","raw.csv")

class DataIngestion:
    def __init__(self):
        self.config = DataIngestionConfig()

    def intiate_data_ingestion(self):
        logging.info("Entered in data ingestion component")

        try:
            csv_path = os.path.join(os.path.dirname(__file__),"..","..","notebook","data","stud.csv")
            csv_path = os.path.abspath(csv_path)
            print(csv_path)


            df = pd.read_csv(csv_path)
            logging.info("readed the dataset as dataframe")

            os.makedirs(os.path.dirname(self.config.train_data_path), exist_ok=True)

            df.to_csv(self.config.raw_data_path, index=False,header=True)

            logging.info("train test split initaiated")
            train, test = train_test_split(df, test_size=0.2, random_state=42)

            train.to_csv(self.config.train_data_path, index=False,header=True)
            test.to_csv(self.config.test_data_path, index=False,header=True)

            logging.info("train and test splitted successfully")

            logging.info("ingenstion of data completed")

            return (
                self.config.train_data_path,
                self.config.test_data_path,
            )
        except Exception as e:
            raise CustomException(e,sys)

if __name__ == "__main__":
    obj = DataIngestion()
    train_data,test_data = obj.intiate_data_ingestion()

    # transformer = DataTransformation()
    # train_arr,test_arr,_ = transformer.initiate_data_transformation(train_data,test_data)
    #
    # model_training = ModelTrainer()
    # score = model_training.initiate_model_training(train_arr,test_arr)
    # print(score)