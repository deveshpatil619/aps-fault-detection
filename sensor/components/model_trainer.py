## Importing the important libraries
from sensor.utils.main_utils import load_numpy_array_data
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from sensor.entity.config_entity import ModelTrainerConfig
import os,sys
from xgboost import XGBClassifier
from sensor.ml.metric.classification_metric import get_classification_score
from sensor.ml.model.estimator import SensorModel
from sensor.utils.main_utils import save_object,load_object



class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,
        data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
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

            if classification_train_metric.f1_score <= self.model_trainer_config.expected_accuracy:
                raise Exception("Trained model is not good to provide the expected accuracy")

            classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)


            ## overfitting and the underfitting condition

            diff =abs( classification_train_metric.f1_score-classification_test_metric.f1_score ) ## here we are substracting the test_f1_score from train_f1_score
            
            ## comparing the diff with the set threshold value
            if diff > self.model_trainer_config.overfitting_underfitting_threshold:
                raise Exception ("Model is not good try to do more experimentation")

            ## loading the pickle file object
            preprocessor = load_object(file_path = self.data_transformation_artifact.transformed_object_file_path )

            ## making the folder 
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)

            sensor_model = SensorModel(preprocessor=preprocessor,model=model) ##
            
            save_object(file_path = self.model_trainer_config.trained_model_file_path,obj=sensor_model)  ## saving the object

            ## model_trainer_artifact

            model_trainer_artifact =ModelTrainerArtifact(trained_model_file_path= self.model_trainer_config.trained_model_file_path,
            train_metric_artifact = classification_train_metric,
            test_metric_artifact = classification_test_metric)

            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact


            
        except Exception as e:
            raise SensorException(e,sys)
            