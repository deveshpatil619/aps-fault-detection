## importing the libraries

from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from sensor.entity.config_entity import DataValidationConfig
from sensor.utils.main_utils import read_yaml_file,write_yaml_file
from sensor.exception import SensorException
from sensor.logger import logging
import os,sys
import pandas as pd
from scipy.stats import ks_2samp



class DataValidation:

    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
        data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)  ## reading the schema file_path



        except Exception as e:
            raise SensorException(e,sys)

    def validate_number_of_columns(self,dataframe:pd.DataFrame)-> bool:
        try:
            
            number_of_columns = len(self._schema_config["columns"])  ## length of columns we will get from schema
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Data frame has columns: {len(dataframe.columns)}")
            if len(dataframe.columns)==number_of_columns:  ## comparing the dataframe columns and the number_of_columns
                return True
            else:
                return False
        except Exception as e:
            raise SensorException(e,sys)

    def is_numerical_column_exist(self,dataframe = pd.DataFrame)-> bool:
        try:

            numerical_columns = self._schema_config['numerical_columns'] ## length of numerical_columns we will get from schema
            dataframe_columns = dataframe.columns  ## columns from the 

            numerical_columns_present = True
            missing_numerical_columns = []
            for num_column in numerical_columns:
                if num_column not in dataframe_columns:
                    numerical_columns_present =False
                    missing_numerical_columns.append(num_column)

            logging.info(f"Missing numerical columns:[{missing_numerical_columns}]")
            return numerical_columns_present

        except Exception as e:
            raise  SensorException(e,sys)



    @staticmethod
    def read_data(file_path)-> pd.DataFrame:  ## output of the file_read should be in dataframe format
        try:
            return pd.read_csv(file_path)

        except Exception as e:
            raise  SensorException(e,sys)


    
    def detect_dataset_drift(self,base_df,current_df,threshold = 0.5)->bool: ## train_df, test_df and threshold
        try:
            status=True
            report = {}

            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1,d2)  ## calculating the drift

                if threshold<=is_same_dist.pvalue:  ## comparing our set threshold with the drift pvalue
                    is_found = False    ## returning false when drift is okay
                else:
                    is_found = True  ## returning true when the drift is greater then our threshold
                    status =False
                report.update({column:{
                                "p_value":float(is_same_dist.pvalue),
                                "drift_status":is_found
                                    }})

            

            drift_report_file_path =  self.data_validation_config.drift_report_file_path

            #Create directory for data_validation in artifacts
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report,)

            return status



        except Exception as e:
            raise SensorException(e,sys)


    def initiate_data_validation(self) -> DataIngestionArtifact :
        try:
            error_message =""
            train_file_path = self.data_ingestion_artifact.trained_file_path ## we need to take the trained and test file paths from data_ingestion_artifacts
            test_file_path = self.data_ingestion_artifact.test_file_path  ## we need to take the trained and test file paths from data_ingestion_artifacts
            
            ## reading the data from the train and test files locations
            train_dataframe = DataValidation.read_data(train_file_path) ## calling the  @static_method read_data
            test_dataframe  = DataValidation.read_data(test_file_path) ##calling the  @static_method read_data

            ## validate the number of columns
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"{error_message}Train dataframe does not contain all columns"
            
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"{error_message}Test dataframe doennot contain all columns"
            
            ## validate the numerical columns

            status = self.is_numerical_column_exist(dataframe=train_dataframe)
            if not status:
                error_message = f"{error_message}Train dataframe does not contain all numerical_columns"
            
            status = self.is_numerical_column_exist(dataframe=test_dataframe)
            if not status:
                error_message = f"{error_message}Test dataframe does not contain all numerical_columns"
            
            if len(error_message)>0:
                raise Exception(error_message)
            
            #Let's check data drift
            #Let check data drift
            status = self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)

            ## Creating the data_validation_artifact
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")

            return data_validation_artifact
        except Exception as e:
            raise SensorException(e,sys)
