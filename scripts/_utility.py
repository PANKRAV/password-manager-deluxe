#PYTHONMODULES
from ast import Tuple
import json
from pathlib import Path
import asyncio
import os
import sys
import time
from typing import List, Dict
import threading
import functools
import concurrent.futures
import logging
from msvcrt import getch, getche




#MYMODULES
from variables import ReadOnly, user_data_init, global_security_init, global_logging_init
import variables






format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.DEBUG,
                        datefmt="%H:%M:%S")




def _init() -> Dict:
    from user import User

    

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
        
    user_data_init()
    global_security_init()
    global_logging_init()

def _quit() -> None :
    sys.exit(0)



#To prevent hash timing attacks
def scheduled_return(_func = None,* ,interval : float = .5) :
    def inner(func) :

       
        mybarrier = threading.Barrier(2)
        myevent = threading.Event()

        def delay(interval) :
            while True :
                logging.debug("started sleeping")
                time.sleep(interval)
                logging.debug("checking for event")
                if myevent.is_set() :
                    try :
                        mybarrier.wait(timeout=100)
                        break

                    except TimeoutError :
                        logging.warning("delay timed out")
                        return False

                    except Exception as ex:
                        raise ex(f"An exception occurred{ex}")

            return


        class FuncData :
            def __init__(self, datafunc, _args, _kwargs) :
                self.datafunc : function = datafunc
                self.args : List = _args
                self.kwargs : Dict = _kwargs
        
        def new_func(data : FuncData) :
            global val
            func = data.datafunc
            args = data.args
            kwargs = data.kwargs
            start_time = time.time()
            logging.debug("starting")
            val = func(*args, **kwargs)
            myevent.set()
            mybarrier.wait()
            logging.debug(f"Finished process in {time.time() - start_time}")
            return val
            
        @functools.wraps(func)
        def wrapper(*args, **kwargs) :
            global mybarrier
            data = FuncData(func, args, kwargs)
            myevent.clear()
            mybarrier = threading.Barrier(2)
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                executor.map(new_func, (data, ))
                executor.map(delay, (interval, ))

            
            logging.debug("exited successfully")
            return val

        
        return wrapper

    if _func is None :  
        return inner
    else :
        return inner(_func)




def handle_file(path : Path, opt : str = "fetch", mode : str = "norm") -> dict :
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


class function :
        ...
class Arg_Save_Wrapper :
    

    def __init__(self, func : function) :
        self.func = func

    def logargs(self, *args, **kwargs) :

        self.func.args = f"*args = ({args}), *kwargs = ({kwargs})"
        self.func.__call__(*args, *kwargs)



def argssave(func : function) :
    return Arg_Save_Wrapper(func).logargs



def timeit(func : function, debug : bool = True, verbose : bool = False, *args : List[function], **kwargs : Dict[str, function]
            ) -> function | List[function] :

    error_count = 0
    errors = dict()
    start_time = time.time()
    try :
        val = func()

    except Exception as ex :        
        error_count += 1
        print(f"{ex} occurred in 1st process")
        errors[f"{error_count}.{val.__name__}()"] = ex

    if args != None or kwargs != None :
        val = list(val)

        for idx, _func in enumerate(args, start = 2) :
            _func : function
            try :
                val.append(_func())
            except Exception as ex:
                print(f"{ex} occured in No.{idx} process ({_func.__name__}())")
                errors[f"{error_count}.{_func.__name__}()"] = ex


        for idx, item in enumerate(kwargs.items(), start = 2 + len(args)) :
            key, _func = item
            try :
                val.append(_func().item())
                print(f"No.{idx} ({_func.__name__}()) {key} process executed successfully")
            except Exception as ex:
                print(f"{ex} occured in No.{idx} {key} process ({_func.__name__}())")
                errors[f"{error_count}.{_func.__name__}()"] = ex


    _time = time.time() - start_time
    if debug :
        print(f"{1 + len(args) + len(kwargs)} Prosseses were executed in {_time} with {error_count} error(s)")

    if verbose :
        for key, ex in errors :
            print(f"{ex} occured in {key} process")

    return val


def loop_switch() -> None :
    os.system("cls||clear")




class Dir_Reset :
    root = Path(__file__).parent.parent


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
        if not self.path == self.root :       
            os.chdir(self.path)
            return self



    def __exit__(self, exc_type, exc_val, exc_tb) :
        if not self.path == self.root :
            os.chdir(Dir_Reset.root)


    @classmethod
    def from_string(cls, _path : str) :
        _path = Path(_path)
        return cls(_path)


def get_dirs(path = os.getcwd()) -> Tuple :
    dirs = os.listdir(path)
    dirs = tuple(Path(dir) for dir in dirs)

    return dirs





class AsterisksOut :

    def __enter__(self) :
        ...

    def __exit__(self, exc_type, exc_val, exc_tb) :
        ...