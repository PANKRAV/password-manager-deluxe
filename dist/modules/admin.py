#MYMODULES
from .user import User
from ._utility import Dir_Reset

#PYTHONMODULES
from pathlib import Path
import json




class Admin :
    _instance = None
    def __new__(cls, *args, **kwargs) -> ...:
        if cls._instance is None :
            super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, user : User) -> None:
        self.user = user


    def valid_check(self) :
        with Dir_Reset.from_string("data/user_data") as cur :
            with Path("users.json").open("rt") as r_f :
                txt = r_f.read()
                self._json = json.loads(txt)

    @staticmethod
    def reset_admin() :
        with Dir_Reset.from_string("data/user_data") as cur :
            with Path("users.json").open("wt") as w_f :
                ...
