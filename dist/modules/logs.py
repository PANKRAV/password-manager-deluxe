#PYTHONMODULES
from functools import wraps
import datetime

#MYMODULES
from ._utility import Dir_Reset

default_format = None
default_file = None



class Logger :

    def __init__(self) -> None:
        pass



    def log_func(self, func) :

        @wraps(func)
        def wrapper(*args, **kwargs) :
            return func(*args, **kwargs)
        
        return wrapper




class Config :
    _instance = None

    def __new__(cls, *args, **kwargs) -> ... :
        if cls._instance is None :
            super().__new__(cls, *args, **kwargs)
        return cls._instance

    
    def __init__(self, *, level : str, format = default_format, file = default_file) :
        self.level = level
        self._format = format
        self.file = file


    
    def decor(self, logger : Logger) :

        @wraps(logger)
        def cls_wrapper(*args, **kwargs) :
            logger(*args, **kwargs)


        return cls_wrapper





