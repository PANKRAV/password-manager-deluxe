#PYTHONMODULES
from typing import Tuple
from pathlib import Path
import os
from collections import deque
import logging


class ReadOnly(Exception):
    ...








class Dir_Reset :
    root = Path(__file__).parent.parent.parent
    stack = deque()
    stack.append(root)
    counter = 0


    def __init__(self, path : Path) -> None:
        self.path = path



    @property
    def dirs(self) :
        return os.listdir(os.getcwd())

    @dirs.setter
    def dirs(self, value) :
        raise ReadOnly("dirs attribute cannot be setted")


    @property
    def pathlibdirs(self) :
        return get_dirs(os.getcwd())

    @pathlibdirs.setter
    def pathlibdirs(self, value) :
        raise ReadOnly("pathlibdirs attribute cannot be setted")


    def __enter__(self) :
        if Dir_Reset.counter == 0 :
            Dir_Reset.stack.append(Dir_Reset.root)
        if not self.path == self.root :
            Dir_Reset.stack.append(os.getcwd())
            os.chdir(self.path)
            Dir_Reset.counter += 1
            return self



    def __exit__(self, exc_type, exc_val, exc_tb) :
        if not self.path == self.root :
            
            Dir_Reset.counter -= 1
            if Dir_Reset.counter < 0 :
                logging.debug("Wrong instance count")
                raise Exception("Wrong Dir_reset instance count")
            
            os.chdir(Dir_Reset.stack.pop())
            


    @classmethod
    def from_string(cls, _path : str) :
        _path = Path(_path)
        return cls(_path)


def get_dirs(path = os.getcwd()) -> Tuple :
    dirs = os.listdir(path)
    dirs = tuple(Path(dir) for dir in dirs)

    return dirs




