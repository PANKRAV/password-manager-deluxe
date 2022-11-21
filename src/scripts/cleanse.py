"""
A quality of life script, used for debugging to quickly delete all of the data files in the data directory
(except users.json which is just cleared)
"""
import sys
sys.path.insert(0, 'C:\\Users\\USERPC\\Desktop\\python\\ey\\double_deluxe\\src\\modules')
from helpers.scriptsutil import Dir_Reset
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
debug = os.getenv("DEBUG")



def main():
    abspath = Path(os.path.abspath(__file__))
    os.chdir(abspath.parent.parent.parent)

    if debug == "1":
        with Dir_Reset.from_string("data") as _cur :
            with Dir_Reset.from_string("encryption_data") as cur :
                for path in cur.pathlibdirs :
                    path : Path
                    path.unlink()
            
            with Dir_Reset.from_string("password_data") as cur :
                for path in cur.pathlibdirs :
                    path : Path
                    path.unlink()

            with Dir_Reset.from_string("user_data") as cur :
                for path in cur.pathlibdirs :
                    if path.stem == "users" :
                        with path.open("wt") as w_f :
                            w_f.write("{}")
                            continue

                    path : Path
                    path.unlink()

    elif debug == "0" :
        print("debug setting is turned off")

    else :
        print("bad .env configuration")

if __name__ == "__main__" :
        main()
        
    