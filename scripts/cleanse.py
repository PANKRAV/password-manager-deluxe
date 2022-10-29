from _utility import Dir_Reset
import os
from pathlib import Path



def main():
    abspath = Path(os.path.abspath(__file__))
    os.chdir(abspath.parent.parent)


    with Dir_Reset.from_string("data/encryption_data") as cur :
        for path in cur.pathlibdirs :
            path : Path
            path.unlink()

    with Dir_Reset.from_string("data/password_data") as cur :
        for path in cur.pathlibdirs :
            path : Path
            path.unlink()

    with Dir_Reset.from_string("data/user_data") as cur :
        for path in cur.pathlibdirs :
            if path.stem == "users" :
                continue

            path : Path
            path.unlink()



if __name__ == "__main__" :
    main()