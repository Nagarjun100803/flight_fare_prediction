import sys



def get_error_message_detail(error, error_detail: sys) : 
    
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = f"""Error occured in python script name \n{file_name}\nin line number : {exc_tb.tb_lineno}\nerror message : {str(error)} """

    return error_message

class CustomException(Exception):
    def __init__(self, error, error_detail:sys):
        super().__init__(error, error_detail)
        self.error = get_error_message_detail(error, error_detail)

    def __str__(self):
        return self.error

if __name__ == '__main__':

    try : 
        res = 5/0
    except Exception as e:
        raise CustomException(e, sys)
    


