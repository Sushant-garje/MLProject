import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join("artifacts","train.csv")
    test_data_path: str = os.path.join("artifacts","test.csv")
    raw_data_path: str = os.path.join("artifacts","raw.csv")

class DataIngestion:
    def __init__(self):
        self.config = DataIngestionConfig()

    def intiate_data_ingestion(self):
        logging.info("Entered in data ingestion component")

        try:
            df = pd.read_csv("/Users/sushant/Documents/PROJECTS/MLproject/notebook/data/stud.csv")
            logging.info("readed the dataset as dataframe")

            os.makedirs(os.path.dirname(self.config.train_data_path), exist_ok=True)

            df.to_csv(self.config.raw_data_path, index=False,header=True)

            logging.info("train test split initaiated")
            train, test = train_test_split(df, test_size=0.2, random_state=42)

            train.to_csv(self.config.train_data_path, index=False,header=True)
            test.to_csv(self.config.test_data_path, index=False,header=True)

            logging.info("train and test splitted successfully")

            logging.info("ingenstion of data completed")
        except Exception as e:
            raise CustomException(e,sys)

if __name__ == "__main__":
    obj = DataIngestion()
    obj.intiate_data_ingestion()