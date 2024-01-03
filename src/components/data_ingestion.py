import os
import sys
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifact', "train.csv")
    test_data_path: str = os.path.join('artifact', "test.csv")
    raw_data_path: str = os.path.join('artifact', "data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self, data_path):
        logging.info("Entered the data ingestion method or component")
        try:
            # Read the dataset as a dataframe
            df = pd.read_csv(data_path)
            logging.info("Read the dataset as a dataframe")

            # Create the necessary directories for storing the train and test data
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            
            logging.info("Initiate the split into train and test data")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # Save the train and test data to their respective files
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion of the dataset is completed")

            return self.ingestion_config.train_data_path, self.ingestion_config.test_data_path

        except Exception as e:
            logging.error("Encountered an error while ingesting the data", exc_info=True)
            raise CustomException(e, sys)

if __name__ == "__main__":
    data_path = "notebook/data/stud.csv"
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion(data_path)

    data_transformation = DataTransformation()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data, test_data)

    ModelTrainer=ModelTrainer()
    print(ModelTrainer.initiate_model_trainer(train_arr,test_arr))

