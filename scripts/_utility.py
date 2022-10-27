from ast import Tuple
import json
from pathlib import Path
import asyncio
import os
import sys









def _init() -> None:
    abspath = Path(os.path.abspath(__file__))
    os.chdir(abspath.parent.parent)

    dirs = os.listdir()
    if "setup" not in dirs :
        with open("setup", "x"):
            pass

        try :
            with Path(".env").open(mode = "x"):
                pass
        except :
            print("password manager is not properly setted up")


        if "data" not in dirs:
            os.mkdir("data")


        with Dir_Reset.from_string("data") as cur :
            if "user_data" not in cur.dirs :
                os.mkdir("user_data")
            
            if "password_data" not in cur.dirs :
                os.mkdir("password_data")

            if "encryption_data" not in cur.dirs :
                os.mkdir("encryption_data")

            with Dir_Reset.from_string("user_data") as _cur :
                if "users.json" not in _cur.dirs :
                    with open("users.json", "x") :
                        pass


def _quit() -> None :
    sys.exit()



def handle_file(path : Path, opt : str = "fetch", mode : str = "norm") -> dict:
    if mode == "bytes" :
        mode = "b"
    else :
        mode = "t"


    if opt == "make" :
        with Dir_Reset(path) as cur :
            if path not in cur.dirs :
                with path.open(f"x{mode}") as f_w:
                    _json = {}
                    f_w.write(json.dumps(_json))
    
    if opt == "fetch" :
        with Dir_Reset(path) as cur :
            if path in cur.dirs :
                with path.open(f"r{mode}") as f_r:
                    _json = f_r.read()
                    _json = json.loads(_json)


    return _json


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
            self.dirs = os.listdir()
            return self



    def __exit__(self, exc_type, exc_val, exc_tb) :
        if not self.path == self.root :
            os.chdir(Dir_Reset.root)



def get_dirs(path = os.getcwd()) -> Tuple :
    dirs = os.listdir(path)
    dirs = tuple(Path(dir) for dir in dirs)

    return dirs