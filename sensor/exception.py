import os,sys


def error_message_details(error, error_detail:sys):
    exc_type, exc_obj, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occured at python script name [{0}] line_number[{1}] error message[{2}]".format(file_name,exc_tb.tb_lineno,str(error))
    return error_message



class SensorException(Exception):
    def __init__(self,error_message,error_detail:sys):
        self.error_message = error_message_details(error_message,error_detail)

    def __str__(self):
        self.error_message









