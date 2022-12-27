## Importing the important libraries

from sensor.entity.config_entity import ModelTrainerConfig
from sensor.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from sensor.utils.main_utils import load_numpy_array_data
from sensor.exception import SensorException
from sensor.logger import logging
import os,sys
from xgboost import XGBClassifier
from sensor.ml.metric.classification_metric import get_classification_score



class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,
    data_transformation_artifact:DataTransformationArtifact) :

        try:
            self.model_trainer_config = model_trainer_config,
            self.data_transformation_artifact = data_transformation_artifact

        except Exception as e:
            raise SensorException(e,sys)


    def train_model(self,x_train,y_train): ## function to train the model
        try:
            xgb_clf = XGBClassifier()
            xgb_clf.fit(x_train,y_train)
            return xgb_clf

        except Exception as e:
            raise




    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path  ## file_paths from the data_transformation stage
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            ##loading the training array and testing array
            train_arr = load_numpy_array_data(train_file_path)  ## loading the training and testing array
            test_arr = load_numpy_array_data(test_file_path)


            x_train,y_train,x_test,y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]

            )
            model = self.train_model(x_train,y_train) ## training the model
            y_train_pred = model.predict(x_train)  ## predicted train values from model
            y_test_pred = model.predict(x_test)   ## predicted test values from model
            classification_train_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred)
            classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)


        except Exception as e:
            raise SensorException(e,sys)