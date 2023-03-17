import sys

def error_message_detail(error,error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    error_file_name = exc_tb.tb_frame.f_code.co_filename
    error_line_number = exc_tb.tb_lineno
    error_msg = "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        error_file_name,error_line_number,str(error))

    return error_msg

class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        #super().__init__(error_message)
        self.error_message = error_message_detail(error = error_message,error_detail = error_detail)

    def __str__(self):
        return self.error_message
