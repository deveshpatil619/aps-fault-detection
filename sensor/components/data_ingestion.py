from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
import os,sys

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config





