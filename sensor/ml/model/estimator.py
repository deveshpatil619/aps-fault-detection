
from sensor.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
import os,sys


class TargetValueMapping:    ## for the target column values that we need to map neg to 0 and pos to 1
    def __init__(self) :
        self.neg : int = 0
        self.pos : int = 1

    def to_dict(self):
        return self.__dict__

    def reverse_mapping(self):
        mapping_response = self.to_dict()
        return dict(zip(mapping_response.values(),mapping_response.keys()))

## For training the model and checking the accuracy
class SensorModel:
    def __init__(self,preprocessor,model) :  ## we will pass the preprocessor(pickle) file that we created in the data_transformation stage and the model to train
        self.preprocessor = preprocessor
        self.model = model

    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise e

## This will give us the best model path
class ModelResolver:

    def __init__(self,model_dir = SAVED_MODEL_DIR):
        try:
            self.model_dir = model_dir

        except Exception as e:
            raise e

    def get_best_model_path(self,)->str:
        try:
            timestamps = list(map(int,os.listdir(self.model_dir))) ## coverting the string values to int via map function and then storing into the list
            latest_timestamp = max(timestamps)  ## taking the max from the list
            latest_model_path = os.path.join(self.model_dir,f"{latest_timestamp}",MODEL_FILE_NAME) 
            return latest_model_path
        except Exception as e:
            raise e

    def is_model_exist(self,)->str:
        try:
            if not os.path.exists(self.model_dir):  ## to check the directory to save model is available or not
                return False
            
            timestamps = os.listdir(self.model_dir) ##to check whether inside the directory files are present or not
            if len(timestamps) == 0:
                return False

            latest_model_path = self.get_best_model_path() ## we will call the best model to check the availability of the model.pkl file

            if not os.path.exists(latest_model_path):
                return False

            return True

        except Exception as e:
            raise e