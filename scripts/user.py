#MYMODULES
from _utility import Dir_Reset, _quit
from variables import MAINLOOP, USERLOOP, CHOICEFILTER, SELFLOOP, BadValue, ReadOnly
import encryption as enc
import json


#PYTHONMODULES
from pathlib import Path
from collections import namedtuple
from typing import List, NamedTuple


Passwords = List[enc.Password]

class User :
    user_count = 0
    user_data = namedtuple("user_data", ["name", "key", "passwords", "salt"])

    def __init__(self, name, key = None, salt = None, passwords = None | Passwords) -> None :
        self.name = name
        self.key = key
        self.passwords = passwords
        self.salt = salt
        self.ecnryption = None


        User.user_count += 1




    def __str__(self) :
        return self.name



    def __repr__(self) :
        return f"{self.__class__.__name__}(name={self.name}, key=\"Hidden\", passwords=\"Hidden\""




    @property
    def file(self) :
        return Path(f"{self.name}.json")


    @file.setter
    def file(self, value) :
        raise ReadOnly("file atributte cannot be setted")


    @property
    def data(self) :
        return {"name" : self.name, "key" : self.key, "pwd" : self.passwords, "salt" : self.salt}

    @data.setter
    def data(self, value) :
        raise ReadOnly("data atributte cannot be setted")



    @property
    def _json(self) :
        with Dir_Reset(Path("data/user_data")) :
            with self.file.open("r") as f_r :
                self._json_ = f_r.read()
            
            return self._json_


    @_json.setter
    def _json(self, value) :
        with Dir_Reset(Path("data/user_data")) :
            with self.file.open("w") as f_w :
                f_w.write(json.dumps(value, indent = 4))




    @property
    def enc_json(self) :
        with Dir_Reset(Path("data/encryption_data")) :
            with self.file.open("r") as f_r :
                self._enc_json = f_r.read()
            
            return self._enc_json


    @enc_json.setter
    def enc_json(self, value) :
        with Dir_Reset(Path("data/encryption_data")) :
            with self.file.open("w") as f_w :
                f_w.write(json.dumps(value, indent = 4))

    @staticmethod
    def users_gen() -> NamedTuple :
        ...



    @staticmethod
    def user_init(name, key = None):
        ...


    @classmethod
    def from_file(cls, path : str | Path) :

        if isinstance(path, str) :
            path = Path(path)
        elif isinstance(path, Path) :
            pass
        else :
            raise BadValue("path parametre needs to be either str or Pathlib.Path")


        with Dir_Reset(Path("data/user_data")) :
            with path.open("r") as f_r :
                ...


   


    def get_pwd(self) -> None :
        ...

    def add_pwd(self) -> None :
        ...

    def mod_pwd(self) -> None :
        ...

    def del_pwd(self) -> None :
        ...

    def list_pwds(self) -> str :
        ...

    def enc_copy(self) -> str :
        ...

    def dec_copy(self) -> str :
        ...




    


    def __call__(self) -> None:
        ...




    def acess(self, key) -> bool :
        
        while SELFLOOP :
            mode = input(
"""
MODE:
1.Acess password account
2.Add password account
3.Modify password account
4.Delete password account
5.List accounts
6.Get encrypted copy of data
7.Get decrypted copy of data
8.Back
9.Exit
Choice:"""
)

            while CHOICEFILTER :
                try:
                        mode = int(mode)               
                except ValueError:
                        mode = input("Input needs to be an integer\nNew choice:")
                        continue


                if mode not in (1, 2, 3, 5, 6, 7, 8, 9) :
                        mode = input("input needs to be an integer between 1 and 9\nNew choice:")
                        continue

                break




            if mode == 1 :
                self.get_pwd()

            
            elif mode == 2 :
                self.add_pwd()


            elif mode == 3 :
                self.mod_pwd()


            elif mode == 4 :
                self.del_pwd()


            elif mode == 5 :
                self.list_pwds()


            elif mode == 6 :
                self.dec_copy()


            elif mode == 7 :
                self.enc_copy() 

            
            elif mode == 8 :
                break

            else :
                _quit()