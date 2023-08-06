import random
import globaldat
import classes
import standardformats
def typeManagment(data):
    dtype = type(data)
    if dtype == str:
        return(bytearray(data.encode(encoding='UTF-8', errors='strict')))
    elif dtype == bytes:
        return(data) 


