import yaml
from sensor.exception import SensorException
from sensor.logger import logging
import os,sys
import numpy as np
import dill




""" Reading the yaml_file"""
def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise SensorException(e, sys) from e

    
""" writing into the yaml_file and creating if we want the yaml_file if replace we keep to true"""

def write_yaml_file(file_path:str,content:object,replace:bool = False) ->None:
    try:

        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)   ## remove the previously created file
        
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as file:
            yaml.dump(content,file)   ## dumping the content into the yaml_file


    except Exception as e:
        raise SensorException(e,sys)



""" saving the numpy array data """

def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """

    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path,"wb") as numpy_file:
            np.save(numpy_file,array)

    except Exception as e:
        raise SensorException(e,sys) from e



""" loading the numpy array data """

def load_numpy_array_data(file_path:str)->np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """

    try:
        with open(file_path,"rb") as numpy_file:
            return np.load(numpy_file)
    except Exception as e:
        raise SensorException(e,sys) from e


""" using the dill to save the object file"""
def save_object(file_path:str,obj:object)->None:
    try:
        logging.info("Entered the save_object method of MainUtils class")

        os.makedirs(os.path.dirname(file_path),exist_ok=True) ## making the folder 
        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)

        logging.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        raise SensorException(e,sys) from e


""" loading the object file"""

def load_object(file_path:str)->object:
    try:
        if not os.path.exists(file_path):
            raise Exception (f"The file: {file_path} is not exists")
        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)
    
    except Exception as e:
        raise SensorException(e,sys) from e











