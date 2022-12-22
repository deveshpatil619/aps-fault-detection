## importing the libraries

from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from sensor.entity.config_entity import DataValidationConfig
from sensor.exception import SensorException
from sensor.logger import logging
import os,sys
import pandas as pd


class DataValidation:

    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
    data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            



        except Exception as e:
            raise SensorException(e,sys)

    def validate_number_of_columns(self)-> bool:
        try:
            
        
        except Exception as e:
            raise SensorException(e,sys)

    def is_numerical_column_exist(self)-> bool:
        pass

    @staticmethod
    def read_data(file_path)-> pd.DataFrame:  ## output of the file_read should be in dataframe format
        try:
            return pd.read_csv(file_path)

        except Exception as e:
            raise  SensorException(e,sys)


    def detect_dataset_drift():
        pass

    def initiate_data_validation(self) -> DataIngestionArtifact :
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path ## we need to take the trained and test file paths from data_ingestion_artifacts
            test_file_path = self.data_ingestion_artifact.test_file_path  ## we need to take the trained and test file paths from data_ingestion_artifacts
            
            ## reading the data from the train and test files locations
            train_dataframe = DataValidation.read_data(train_file_path) ## calling the  @static_method read_data
            test_dataframe  = DataValidation.read_data(test_file_path) ##calling the  @static_method read_data


        except Exception as e:
            raise SensorException(e,sys)
