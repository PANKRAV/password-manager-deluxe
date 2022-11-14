from pathlib import Path
import os
import sys
from typing import List, Dict
import json
from math import log2

import rsa

from helpers.scriptsutil import Dir_Reset
from helpers.migrationutil import ceasar, reverse_ceasar, hash3, simple_crypt


VERBOSE = False


def migrate(*, pwd : Dict, user : Dict, enc : Dict, key : str, old_security : int, new_security : int = 2048) :
    new_enc = enc
    new_enc["security"] = new_security


    hashed_key = user["key"]
    salt = user["salt"]
    key_check = key + salt
    key_check = hash3(key_check)
    if not hashed_key == key_check  :
        raise Exception("Old key and new key don't match")
    else :
        new_user = user


    publicKey = enc["publicKey"]
    publicKey = publicKey.encode("latin-1")
    publicKey = simple_crypt(key, publicKey, "dec")
    publicKey = rsa.PublicKey.load_pkcs1(publicKey)

    privateKey = enc["privateKey"]
    privateKey = privateKey.encode("latin-1")
    privateKey = simple_crypt(key, privateKey, "dec")
    privateKey = rsa.PrivateKey.load_pkcs1(privateKey)

    new_pwd = pwd
    for acc_name, acc in new_pwd.items() :
        enc_pwd = acc["pwd"]
        dec_pwd = rsa.decrypt(enc_pwd.encode("latin-1"), priv_key=privateKey).decode("latin-1")
        new_enc_pwd = ceasar(dec_pwd, 6)
        new_enc_pwd = rsa.encrypt(new_enc_pwd.encode("latin-1"), pub_key=publicKey).decode("latin-1")
        new_pwd[acc_name]["pwd"] = new_enc_pwd


    return new_user, new_enc, new_user
    
    




def main(argsv : List):
    opts = [arg for arg in argsv[1:] if arg.startswith("-")]
    args = [arg for arg in argsv[1:] if not arg.startswith("-")]


    if "-v" in opts :
        VERBOSE = True

    abspath = Path(os.path.abspath(__file__))
    os.chdir(abspath.parent)
    try :
        args[0]
        _old_security = int(args[0])
        level = log2(args[0])
        if level != int(level) :
            raise Exception("security level command line argument needs to be an integer power of 2")
    except IndexError :
        raise Exception("Security level command line argument required")
    except ValueError as val_ex:
        raise val_ex("security level command line argument needs to be an integer")
    except Exception as ex :
        raise ex("This wasn't supposed to happen")

   
    try :
        args[1]
    except IndexError :
        raise Exception("Key command line argument required")
    except Exception as ex :
        raise ex("This wasn't supposed to happen")
    _key = args[1]

    try :
        with Dir_Reset.from_string("MIGRATION/OLD") :
            with Dir_Reset.from_string("data") as cur :
                if len(args) == 3 :
                    user_name = args[2]
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



    try :
        new_user, new_enc, new_pwd  = migrate(pwd=pwd_json, user=user_data, enc=enc_json, key=_key, old_security=_old_security)
    except KeyError as ex:
        print(f"An exception occured : {ex} (Probably bad json file structure)")



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