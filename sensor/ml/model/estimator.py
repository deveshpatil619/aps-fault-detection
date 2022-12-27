import os,sys
class TargetValueMapping:    ## for the target column values that we need to map
    def __init__(self) :
        self.neg : int = 0
        self.pos : int = 1

    def to_dict(self):
        return self.__dict__

    def reverse_mapping(self):
        mapping_response = self.to_dict()
        return dict(zip(mapping_response.values(),mapping_response.keys()))

