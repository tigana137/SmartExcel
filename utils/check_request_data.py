
from x.functions import CustomError


def check_request_data(array_of_val: dict, request_data: dict):

    for val, val_type in array_of_val.items():
        if not val in request_data or val_type != type(request_data[val]):
            raise CustomError("")

    return
