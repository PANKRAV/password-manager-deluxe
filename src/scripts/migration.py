from scriptsutil import Dir_Reset
from pathlib import Path
import os
import sys
from typing import List
import json

def migrate(pwd, user, enc) :
    ...


def main(argsv : List):
    abspath = Path(os.path.abspath(__file__))
    os.chdir(abspath.parent)
    try :
        argsv[1]
    except IndexError :
        raise Exception("Security level command line argument required")
    except Exception as ex :
        raise ex("This wasn't supposed to happen")
    old_security = argsv[1]

    try :
        with Dir_Reset.from_string("migration/old") :
            with Dir_Reset.from_string("data") as cur :
                if len(argsv) == 3 :
                    user_name = argsv[2]
                    if user_name not in [_dir.stem for _dir in cur.pathlibdirs] :
                        raise Exception("User file does not exist")
                else :                  
                    user_name = cur.pathlibdirs.stem
                
                with Path(f"{user_name}.json").open("rt") as r_f :
                    pwd_json = json.load(r_f)
            
            with Path("users.json").open("rt") as r_f :
                user_json = json.load(r_f)
                user_data = user_json[user_name]
            
            with Dir_Reset.from_string("encryption_data") as cur :
                with Path(f"{user_name}.json").open("rt") as r_f :
                    enc_json = json.load(r_f)
                               

    
    except FileNotFoundError :
        raise FileNotFoundError("Migration directory does not exists or is either empty.")
    

    new_pwd, new_enc, new_user = migrate(pwd=pwd_json, user=user_data, enc=enc_json)

    with Dir_Reset.from_string("migration") as cur :
        if "NEW" not in cur.dirs :
            os.mkdir("NEW")
        
        with Dir_Reset.from_string("NEW") as _cur :
            
            os.mkdir("user_data")            
            os.mkdir("password_data")            
            os.mkdir("encryption_data")
            
            with Dir_Reset.from_string("user_data") :
                with Path(f"{user_name}.json").open("xt") as w_f :
                    txt = json.dumps(new_user, indent=4)
                    w_f.write(txt)
            
            with Dir_Reset.from_string("password_data") :
                with Path(f"{user_name}.json").open("xt") as w_f :
                    txt = json.dumps(new_pwd, indent=4)
                    w_f.write(txt)
            
            with Dir_Reset.from_string("encryption_data") :
                with Path(f"{user_name}.json").open("xt") as w_f :
                    txt = json.dumps(new_enc, indent=4)
                    w_f.write(txt)
    
    



if __name__ == "__main__" :
    main(sys.argv)