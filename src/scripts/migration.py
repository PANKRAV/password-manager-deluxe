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
REVERSE = False

class BadArguments(Exception) :
    def __init__(self, message) -> None:
        self.message = message
        self.message += "\nusage : python3 migarion.py [-v | --verbose] [-r | --reverse] <Security Level (power of 2)> <key (string)> <User Name (optional)>"
        super().__init__(self.message)

def migrate(*, name, pwd : Dict, user : Dict, enc : Dict, key : str, old_security : int, new_security : int = 2048) :
    new_enc = enc
    new_enc["security"] = new_security


    hashed_key = user["key"]
    salt = user["salt"]
    key_check = key + salt
    key_check = hash3(key_check)
    if not hashed_key == key_check  :
        raise Exception("Old key and new key don't match")
    else :
        user["name"] = name
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


    return new_user, new_enc, new_pwd
    
    

def reverse_migrate(*,name, pwd : Dict, user : Dict, enc : Dict, key : str, new_security : int = 2048) :
    new_user = dict()
    new_enc = dict()
    new_pwd = dict()

    hashed_key = user["key"]
    salt = user["salt"]
    key_check = key + salt
    key_check = hash3(key_check)
    if not hashed_key == key_check  :
        raise Exception("Old key and new key don't match")
    else :
        user.pop("name")
        new_user[name] = user
    

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
        new_enc_pwd = reverse_ceasar(dec_pwd, 6)
        new_enc_pwd = rsa.encrypt(new_enc_pwd.encode("latin-1"), pub_key=publicKey).decode("latin-1")
        new_pwd[acc_name]["pwd"] = new_enc_pwd
        

    
    return new_user, new_enc, new_pwd



def main(argsv : List):
    global VERBOSE
    opts = [arg for arg in argsv[1:] if arg.startswith("-")]
    args = [arg for arg in argsv[1:] if not arg.startswith("-")]


    if "-v" in opts or "--verbose" in opts :
        VERBOSE = True
    
    if "-r" in opts or "--revese" in opts :
        REVERSE = True

    abspath = Path(os.path.abspath(__file__))
    os.chdir(abspath.parent)
    try :
        args[0]
        _old_security = int(args[0])
        level = log2(_old_security)
        if level != int(level) :
            raise BadArguments("security level command line argument needs to be an integer power of 2")
    except IndexError :
        raise BadArguments("Security level command line argument required")
    except ValueError as val_ex:
        raise val_ex("security level command line argument needs to be an integer")
    except Exception as ex :
        raise ex("This wasn't supposed to happen")

   
    try :
        args[1]
    except IndexError :
        raise BadArguments("Key command line argument required")
    except Exception as ex :
        raise ex("This wasn't supposed to happen")
    _key = args[1]

    try :
        with Dir_Reset.from_string("MIGRATION/OLD") as _cur:
            with Dir_Reset.from_string("data", root = os.path.abspath(os.getcwd())) as cur :
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
                if not REVERSE :
                    user_data = user_json[user_name]
                else :
                    user_data = user_json
            with Dir_Reset.from_string("encryption_data") as cur :
                with Path(f"{user_name}.json").open("rt") as r_f :
                    enc_json = json.load(r_f)
                               

    
    except FileNotFoundError :
        raise FileNotFoundError("Migration directory does not exists or is either empty.")



    try :
        if not REVERSE :
            new_user, new_enc, new_pwd  = migrate(name=user_name, pwd=pwd_json, user=user_data, enc=enc_json, key=_key, old_security=_old_security)
        else : 
            new_user, new_enc, new_pwd  = reverse_migrate(name=user_name, pwd=pwd_json, user=user_data, enc=enc_json, key=_key)

    except KeyError as ex:
        print(f"An exception occured : {ex} (Probably bad json file structure)")



    with Dir_Reset.from_string("migration") as cur :
        if "NEW" not in cur.dirs :
            os.mkdir("NEW")
        
        with Dir_Reset.from_string("NEW") as _cur :
            
            if "user_data" not in _cur.dirs :
                os.mkdir("user_data") 
            if "password_data" not in _cur.dirs :           
                os.mkdir("password_data")
            if "encryption_data" not in _cur.dirs :          
                os.mkdir("encryption_data")
            
            with Dir_Reset.from_string("user_data", root = os.path.abspath(os.getcwd())) :
                with Path(f"{user_name}.json").open("wt") as w_f :
                    txt = json.dumps(new_user, indent=4)
                    w_f.write(txt)
            
            with Dir_Reset.from_string("password_data", root = os.path.abspath(os.getcwd())) :
                with Path(f"{user_name}.json").open("wt") as w_f :
                    txt = json.dumps(new_pwd, indent=4)
                    w_f.write(txt)
            
            with Dir_Reset.from_string("encryption_data", root = os.path.abspath(os.getcwd())) :
                with Path(f"{user_name}.json").open("wt") as w_f :
                    txt = json.dumps(new_enc, indent=4)
                    w_f.write(txt)
    
    



if __name__ == "__main__" :
    main(sys.argv)
    if VERBOSE :
        pass
    print("Executed succesfully")