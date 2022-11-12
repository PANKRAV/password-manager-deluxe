"""
A module for the User class
"""

#MYMODULES
from ._utility import Dir_Reset, _quit, handle_file, loop_switch, Timeout
from .variables import users_to_reset, MAINLOOP, USERLOOP, CHOICEFILTER, SELFLOOP, BadValue, ReadOnly, UserFileExists, BadUserSetup
from .encryption import Encryption, Password, salt, hash3, hash2, random_password_new, ceasar, reverse_ceasar



#PYTHONMODULES
import json
from pathlib import Path
from collections import namedtuple
from typing import List, NamedTuple, Dict
import os
from pwinput import pwinput
import time


Passwords = List[Password]

class User :
    """
    A class used to implement Users

    ...

    Class Attributes :
    - user_count : Keep track of the user count


    Attributes :
    - name (str) : User's name

    - key (str) : * A User's key used for encryption processes 
                  * Is None on User initialization

    - password (int) : * User's password count
                       * Is None on User initialization
    
    - salt (str) : * User's salt used for encryption processes 
                   * Stored in data/user_data/{self.name}.json

    - encryption (encryption.Encryption) : User's own implemented encryption object to handle encryption processes

    - key_check (bool) : A switch to prevent acessing the User's methods without key validation


    Properties :
    - status : * A string representation of key_check
               * Can't be set

    - file : * A string representation of the file name where the User's data is stored
             * Can't be set

    - data : * A dict representation of the most useful User attributes
             * Can't be set

    - pwd_json : * A json string of password_data/{self.file}
                 * Writes json data on the same file when a dict is assigned to it

    - enc_json : * A json string of encryption_data/{self.file}
                 * Writes json data on the same file when a dict is assigned to it
    
    - user_json : * A json string of user_data/{self.file}
                 * Writes json data on the same file when a dict is assigned to it


    Class Methods :
    - from_file : Initializes a User object from a file name and the data stored on the file

    - user_init : * Initializes a new User object with no previous files
                 * Uses User.from_file internally
    

    Static Methods :
    - users_gen : Returns a dict of all the existing Users in the file structure

    - reset_encryption : Resets all User's rsa keys and encrypted data which have been accessed on runtime


    Methods :
    - __str__ : Returns the User's self.name

    - __repr__ : Representation of the User object

    - get_pwd : Prints a selected account from the User's password_data

    - add_pwd : Adds a certain account from the User's password_data

    - del_pwd : Deletes a selected account from the User's password_data

    - mod_pwd : Modifys a selected account from the User's password_data

    - list_pwds : Lists all of the User's account

    - enc_copy : Prints all the ecnrypted from the User's password_data

    - dec_copy : Prints all the decrypted from the User's password_data

    - acess : * Flow control for above methods
              * Only able to run if key_check == True

    - check_key : * Checks a User's stored hashed-salted key against a give one
                  * Toggles key_check attribute

    """

    user_count = 0
    user_data = namedtuple("user_data", ["name", "key", "passwords", "salt"])

    def __init__(self, name, key = None, salt = None, passwords = None | Passwords | int) -> None :
        self.name = name
        self.key = key
        self.passwords = passwords
        self.salt = salt
        self.ecnryption : Encryption = None
        self.key_check = False


        User.user_count += 1




    def __str__(self) :
        return self.name



    def __repr__(self) :
        return f"{self.__class__.__name__}(name={self.name}, key=\"Hidden\", passwords=\"Hidden\""



    #mostly for debugging purposes
    @property
    def status(self) :
        if self.check_key() :
            return "Unlocked"
        else :
            return "Locked"


    @status.setter
    def status(self, value) :
        raise ReadOnly("status atributte cannot be setted")



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
    def pwd_json(self) -> str :
        with Dir_Reset(Path("data/password_data")) :
            with self.file.open("r") as f_r :
                self._json_ = f_r.read()
            
            return self._json_


    @pwd_json.setter
    def pwd_json(self, value : Dict) -> None :
        with Dir_Reset(Path("data/password_data")) :
            with self.file.open("w") as f_w :
                f_w.write(json.dumps(value, indent = 4))




    @property
    def enc_json(self) -> str:
        with Dir_Reset(Path("data/encryption_data")) :
            with self.file.open("r") as f_r :
                self._enc_json = f_r.read()
            
            return self._enc_json


    @enc_json.setter
    def enc_json(self, value : Dict) -> None :
        with Dir_Reset(Path("data/encryption_data")) :
            with self.file.open("w") as f_w :
                f_w.write(json.dumps(value, indent = 4))



    @property
    def user_json(self) -> str :
        with Dir_Reset(Path("data/user_data")) :
            with self.file.open("r") as f_r :
                self._user_json = f_r.read()
            
            return self._user_json


    @user_json.setter
    def user_json(self, value : Dict) -> None :
        with Dir_Reset(Path("data/user_data")) :
            with self.file.open("w") as f_w :
                f_w.write(json.dumps(value, indent = 4))





    @classmethod
    def from_file(cls, path : str | Path) :

        if isinstance(path, str) :
            path = Path(path)
        elif isinstance(path, Path) :
            pass
        else :
            raise BadValue("path parameter needs to be either str or Pathlib.Path")


        with Dir_Reset(Path("data/user_data")) :
            with path.open("rt") as r_f :
                txt = r_f.read()
                _json = json.loads(txt)
                name : str = _json["name"]
                key : str = _json["key"] #hashed value
                salt : str = _json["salt"]

            return cls(name = name, key = key, salt = salt, passwords = len(_json))
        
        return




    @classmethod
    def user_init(cls, name, key = None):
        
        assert key != None
        original = str(key)#str so it is not just a reference
        key, _salt = salt(key)
        key = hash3(key)
        _file = f"{name}.json"
        
        with Dir_Reset.from_string("data/password_data") as cur :
            if _file in cur.dirs :
                raise UserFileExists("debug : data/password_data")

            with Path(_file).open("xt") as w_f :
                _json = json.dumps({})
                w_f.write(_json)


        with Dir_Reset.from_string("data/user_data") as cur :
            if _file in cur.dirs :
                raise UserFileExists("debug : data/user_data")

            with Path(_file).open("xt") as w_f :
                dct = {"name" : name, "key" : key, "salt" : _salt}
                _json = json.dumps(dct, indent=4)
                w_f.write(_json)



        publicKey, privateKey, security = Encryption.UserEnc.user_init(original)

        with Dir_Reset.from_string("data/encryption_data") as cur :
            if _file in cur.dirs :
                raise UserFileExists("debug : data/encryption_data")

            with Path(_file).open("xt") as w_f :
                _json = {"publicKey" : publicKey, "privateKey" : privateKey, "security" : security}
                _json = json.dumps(_json)
                w_f.write(_json)


        return cls.from_file(_file)



    @staticmethod
    def users_gen() -> NamedTuple :
        from .variables import user_data
        #user_data = dict()

        with Dir_Reset.from_string("data/user_data") as cur :
            users = (user for user in cur.pathlibdirs)
                
                
        for user in users :
            user : Path
            name = user.stem

            if name == "users" :
                continue

            with Dir_Reset.from_string("data/password_data") as cur :               

                try :
                    with user.open("rt") as r_f :
                        txt = r_f.read()
                        _json = json.loads(txt)
                        pwd_count = len(_json)

                except :
                    handle_file(user, opt = "make")
                    #log bug here

            
            with Dir_Reset.from_string("data/user_data") as cur :

                try :
                    with user.open("rt") as r_f:
                        txt = r_f.read()
                        _json = json.loads(txt)
                        _key = _json["key"]
                        _salt = _json["salt"]
                
                except :
                    handle_file(user, opt = "make")
                    #log bug here


            user_data[name] = User(name, passwords = pwd_count, key = _key, salt = _salt)


        
        return user_data


    def get_pwd(self) -> None :
        _json = self.pwd_json
        _json : Dict = json.loads(_json)
        if _json == {} :
            print("There are no accounts yet, maybe create some")
            input("Continue :")
            loop_switch()
            return

        acc_name = input("Account name :")
        while acc_name not in _json.keys() :
            acc_name = input("Account does not exist\nGive a new name :")
        
        for _idx, acc in enumerate(_json.keys()) :
            if acc == acc_name :
                idx = _idx

        tmp_t = Timeout(60)
        _json = _json[acc_name]
        username = _json["username"]
        email = _json["email"]
        enc_pwd = _json["pwd"]
        dec_pwd = self.ecnryption.decrypt(enc_pwd)
        dec_pwd = reverse_ceasar(dec_pwd, 6)
        print(f"""
Account : {acc_name}
Username : {username}
E-Mail : {email}
Password : {dec_pwd}""")

        tmp_t.run()
        loop_switch()
        return


    def add_pwd(self) -> None :
        _json = self.pwd_json
        _json : Dict = json.loads(_json)
        acc_name = input("Account name :")
        while acc_name in _json.keys() :
            acc_name = input("Account name is taken\nGive a new name :")

        username = input("Username :")
        while CHOICEFILTER :             
            email = input("E-Mail :")

            if email != email.rstrip():
                print("Email can't have a whitespace")
                continue
            break


        while True :
            mode = input("1.Choose a Password\n2.Random password\nChoice :")

            while CHOICEFILTER :
                try:
                    mode = int(mode)               
                except ValueError:
                    mode = input("Input needs to be an integer\nNew choice:")
                    continue


                if mode not in (1, 2) :
                    mode = input("input needs to be an integer between 1 and 2\nNew choice:")
                    continue

                break

            if mode == 1 :
                while CHOICEFILTER :
                    pwd = pwinput(prompt = "Password :")
                    check_pwd = pwinput(prompt = "Confirm Password :") 
                    if check_pwd != pwd :
                        print("Wrong confirmation\nTry again")
                        continue
                    break
                break
                 
                    
            
            else :#2
                while True:
                    try:
                        length = int(input("Password length :"))
                        break  

                    except ValueError:
                        length = input("choice needs to be an integer\nnew choice:")

                pwd = random_password_new(length)
                print(f"Your password is {pwd}")
                choice = input("For a different password input \"yes\" :")
                if not choice.upper() == "YES":
                    break

        
        ces_pwd = ceasar(pwd, self.passwords - 1)
        enc_pwd = self.ecnryption.encrypt(ces_pwd)
        _json[acc_name] = {"username" : username, "pwd" : enc_pwd, "email": email}
        self.pwd_json = _json
        print("Account configured")
        tmp_t = Timeout(60)
        print(f"""
Account : {acc_name}
Username : {username}
E-Mail : {email}
Password : {pwd}""")
        tmp_t.run()
        loop_switch()
        return



    def mod_pwd(self) -> None :
        _json = self.pwd_json
        _json : Dict = json.loads(_json)
        if _json == {} :
            print("There are no accounts yet, maybe create some")
            input("Continue :")
            loop_switch()
            return

        acc_name = input("Account name :")
        while acc_name not in _json.keys() :
            acc_name = input("Account does not exist\nGive a new name :")
        
        for _idx, acc in enumerate(_json.keys()) :
            if acc == acc_name :
                idx = _idx
        
        while USERLOOP :
            username = _json[acc_name]["username"]
            email = _json[acc_name]["email"]
            enc_pwd = _json[acc_name]["pwd"]
            dec_pwd = self.ecnryption.decrypt(enc_pwd)
            dec_pwd = reverse_ceasar(dec_pwd, 6)
            tmp_t = Timeout(60)

            print(f"""
Current :
Account : {acc_name}
Username : {username}
E-Mail : {email}
Password : {dec_pwd}""")
            tmp_t.run()
            loop_switch()

            print("What would you like to modify")
            mode = input(
"""
1.account name:
2.email
3.username
4.password
5.view current
6.Back
choice:"""
)   
            while CHOICEFILTER:               

                try:
                    mode = int(mode)               
                except ValueError:
                    mode = input("Input needs to be an integer\nNew choice:")
                    continue


                if mode not in (1, 2, 3, 4, 5, 6) :
                    mode = input("input needs to be an integer between 1 and 5\nNew choice:")
                    continue

                break


            
            if mode == 1 :
                while CHOICEFILTER :
                    change_text = input("New account name:")

                    if change_text in list(_json.keys()):

                        print("Account already exists")

                    else:
                        break

                _json[change_text] = _json.pop(acc_name)
                acc_name = change_text

            elif mode == 2 :
                while CHOICEFILTER :

                    change_text = input("New email:")

                    if change_text != change_text.rstrip():
                        print("Email can't have a whitespace")

                    else:
                        break




                _json[acc_name]["email"] = change_text
            
            elif mode == 3 :
                change_text = input("new username:")
                _json[acc_name]["username"] = change_text

            elif mode == 4 :
                while True :
                    _mode = input("1.Choose a new password\n2.Generate a new random password\nChoice :")

                    while CHOICEFILTER :
                        try:
                            _mode = int(_mode)               
                        except ValueError:
                            _mode = input("Input needs to be an integer\nNew choice:")
                            continue


                        if _mode not in (1, 2) :
                            _mode = input("input needs to be an integer between 1 and 2\nNew choice:")
                            continue

                        break

                    if _mode == 1 :
                        while CHOICEFILTER :
                            pwd = pwinput(prompt = "Password :")
                            check_pwd = pwinput(prompt = "Confirm Password :") 
                            if check_pwd != pwd :
                                print("Wrong confirmation\nTry again")
                                continue
                            break
                        break
                            
                            
                    
                    else :#2
                        while True:
                            try:
                                length = int(input("Password length :"))
                                break  

                            except ValueError:
                                length = input("choice needs to be an integer\nnew choice:")

                        pwd = random_password_new(length)
                        print(f"Your password is {pwd}")
                        choice = input("For a different password input \"yes\" :")
                        if not choice.upper() == "YES":
                            break
                            

                        
                    new_enc_pwd = self.ecnryption.encrypt(pwd)
                    _json[acc_name]["pwd"] = new_enc_pwd
            
            elif mode == 5 :
                #self.pwd_json = _json
                continue

            else :
                #self.pwd_json = _json
                break
            
            self.pwd_json = _json
            done = input("Are you done with the changes?\n1.Yes\n2.No\nChoice:")

            while CHOICEFILTER:
                try:
                    done = int(done)               
                except ValueError:
                    done = input("Input needs to be an integer\nNew choice:")
                    continue


                if done not in (1, 2) :
                    done = input("input needs to be an integer between 1 and 2\nNew choice:")
                    continue

                break

            
            if done == 1:
                loop_switch()
                return
            
            else :
                loop_switch()
                continue

    def del_pwd(self) -> None :
        _json = self.pwd_json
        _json : Dict = json.loads(_json)
        if _json == {} :
            print("There are no accounts yet, maybe create some")
            input("Continue :")
            loop_switch()
            return

        acc_name = input("Account name :")
        while acc_name not in _json.keys() :
            acc_name = input("Account does not exist\nGive a new name :")
        
        choice = input("Are you sure :\n1.Yes\n2.No\nChoise :")
        while True :
            try :
                choice = int(choice)
            except :
                choice = input("Your choice needs to be an integer")
                continue

            if choice not in (1, 2) :
                choice = input("Your choice needs to be an integer between 1 and 2")
                continue

            break

        if choice == 1 :
            _json.__delitem__(acc_name)
            self.pwd_json = _json
            input("Continue :")
            loop_switch()
            return
        
        else :
            return

    def list_pwds(self) -> str :
        _json = self.pwd_json
        _json : Dict = json.loads(_json)
        if _json == {} :
            print("There are no accounts yet, maybe create some")
            input("Continue :")
            loop_switch()
            return

        for idx , key in enumerate(_json.keys(), start=1) :
            print(f"{idx}.{key}")
        input("Continue :")
        loop_switch()
        return

    def enc_copy(self) -> str :
        _json = self.pwd_json
        _json = json.loads(_json)
        if _json == {} :
            print("There are no accounts yet, maybe create some")
            input("Continue :")
            loop_switch()
            return

        tmp_t = Timeout(60)
        print(_json)
        tmp_t.run()
        loop_switch()
        return

    def dec_copy(self) -> str :
        _json = self.pwd_json
        _json : Dict = json.loads(_json)
        if _json == {} :
            print("There are no accounts yet, maybe create some")
            input("Continue :")
            loop_switch()
            return

        for name, acc in _json.items() :
            enc_pwd = acc["pwd"]
            dec_pwd = self.ecnryption.decrypt(enc_pwd)
            dec_pwd = reverse_ceasar(dec_pwd, 6)
            _json[name]["pwd"] = dec_pwd
        
        tmp_t = Timeout(60)

        print(_json)
        
        tmp_t.run()
        loop_switch()
        return







    def __call__(self) -> None:
        ...



    def check_key(self, key : str = None, hash_type = 3) -> bool:
        #str(key) to avoid original being just a reference to the key variable
        original = str(key) 
        if not self.key_check :
            key += self.salt
            if hash_type == 3:
                key = hash3(key)
            elif hash_type == 2:
                key = hash2(key)

            if key == self.key:
                self.key = original
                del original
                self.key_check = True
                self.ecnryption = Encryption.UserEnc(self)
                time.sleep(.1)
                return True

            else:
                return False

        else :
            return True


    def access(self) -> None :
        if self not in users_to_reset :
            users_to_reset.append(self)

        if self.key_check and self.ecnryption is not None :    
            while SELFLOOP :
                mode = input(
    """
    MODE:
    1.Acess password account
    2.Add password account
    3.Modify password account
    4.Delete password account
    5.List accounts
    6.Get decrypted copy of data
    7.Get encrypted copy of data
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


                    if mode not in (1, 2, 3, 4, 5, 6, 7, 8, 9) :
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
                    self.key_check = False
                    self.key = json.loads(self.user_json)["key"]
                    break

                else :
                    _quit()


        else :
            raise BadUserSetup("User was setted up incorrectly")



    def reset(self) :
        _json = self.pwd_json
        _json : Dict = json.loads(_json)
        
        for name, acc in _json.items() :
            enc_pwd = acc["pwd"]
            dec_pwd = self.ecnryption.decrypt(enc_pwd)
            _json[name]["pwd"] = dec_pwd

        self.ecnryption.reset()
        
        for name, acc in _json.items() :
            dec_pwd = acc["pwd"]
            enc_pwd = self.ecnryption.encrypt(dec_pwd)
            _json[name]["pwd"] = enc_pwd

        self.pwd_json = _json






    @staticmethod
    def reset_encryption() :
        for user in users_to_reset :
            user : User
            user.reset()