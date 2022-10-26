from ast import Tuple
from pathlib import Path
import asyncio
import os









def _init() -> None:
    ...



def _quit() -> None :
    ...



def handle_file(path : Path) :
    ...



async def minimal_time(func, delay) :
    ...


def timeit(func) :
    ...



def loop_switch() -> None :
    os.system("cls||clear")


class Dir_Reset :
    root = Path(__file__).parent


    def __init__(self, path : Path) -> None:
        self.path = path


    @classmethod
    def from_string(cls, _path : str) :
        _path = Path(_path)
        return cls(_path)


    def __enter__(self) :
        if not self.path == self.root :       
            os.chdir(self.path)



    def __exit__(self, exc_type, exc_val, exc_tb) :
        if not self.path == self.root :
            os.chdir(Dir_Reset.root)



def get_dirs(path = os.getcwd()) -> Tuple :
    dirs = os.listdir(path)
    dirs = tuple(Path(dir) for dir in dirs)

    return dirs