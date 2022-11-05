#PYTHONMODULES
from __future__ import annotations
from typing import TYPE_CHECKING
from numpy import character, random as nprand
import numpy as np
import hashlib
from rsa import PrivateKey, PublicKey
import cryptography
import simplecrypt
import rsa
from cryptography.fernet import Fernet
import pathlib
import json


#MYMODULES
from variables import CHARS, LOWER, UPPER, NUMBERS, SYMBOLS, RAN_CHAR_SEQ, BadUserSetup, GLOBAL_SECURITY
from _utility import scheduled_return


@scheduled_return
def random_password(length = 10):
    pr = []

    char_list = [char for char in CHARS]
    LOWER_list = [char for char in LOWER]
    UPPER_list = [char for char in UPPER]
    NUMBERS_list = [char for char in NUMBERS]
    SYMBOLS_list = [char for char in SYMBOLS]

    const = 1/len(char_list)

    for char in char_list:
        
        if char in LOWER_list:
            pr.append(0.2/len(LOWER_list))


        elif char in UPPER_list:
            pr.append(0.2/len(UPPER_list))


        elif char in NUMBERS_list:
            pr.append(0.3/len(NUMBERS_list)) 

        
        elif char in SYMBOLS_list:
            pr.append(0.3/len(SYMBOLS_list)) 

        
    password = nprand.choice(char_list, p = pr, size = length) 

    return "".join(password)




@scheduled_return
def random_password_new(length = 10):
    pr = []
    last = None
    password = []

    char_list = [char for char in CHARS]
    LOWER_list = [char for char in LOWER]
    UPPER_list = [char for char in UPPER]
    NUMBERS_list = [char for char in NUMBERS]
    SYMBOLS_list = [char for char in SYMBOLS]

    const = 1/len(char_list)

    for char in char_list:
        
        if char in LOWER_list:
            pr.append(0.2/len(LOWER_list))


        elif char in UPPER_list:
            pr.append(0.2/len(UPPER_list))


        elif char in NUMBERS_list:
            pr.append(0.3/len(NUMBERS_list)) 

        
        elif char in SYMBOLS_list:
            pr.append(0.3/len(SYMBOLS_list)) 

    for i in range(length):        
        char = nprand.choice(char_list, p = pr, size = 1) 

        if char in LOWER_list:
            if last == 1 and repeat == True:
                char = nprand.choice(char_list, p = pr, size = 1)
                repeat = False
                
            else:
                last = 1

        
        elif char in UPPER_list:
            if last == 2 and repeat == True:
                char = nprand.choice(char_list, p = pr, size = 1)
                repeat = False
                
            else:
                last = 2

        
        elif char in NUMBERS_list:
            if last == 3 and repeat == True:
                char = nprand.choice(char_list, p = pr, size = 1)
                repeat = False
                
            else:
                last = 3

        
        elif char in SYMBOLS_list:
            if last == 4 and repeat == True:
                char = nprand.choice(char_list, p = pr, size = 1)
                repeat = False
                
            else:
                last = 4
        
        password.append(char)
        repeat = True

    password = np.concatenate(password).ravel().tolist()
    return "".join(password)

#hash processes
@scheduled_return(interval=.4)
def hash2(ctx) -> str:
    byte_data = ctx.encode()
    return hashlib.sha512(byte_data).hexdigest()

@scheduled_return(interval=.4)
def hash3(ctx) -> str:
    byte_data = ctx.encode()
    return hashlib.sha3_512(byte_data).hexdigest()

def salt(ctx : str) -> str:
    salt = random_password(5)
    return ctx + salt, salt


@scheduled_return(interval=1)
def simple_crypt(passkey, ctx, mode : str = "enc") -> str:
    
    if mode == "enc":
        return simplecrypt.encrypt(passkey, ctx)

    elif mode == "dec":
        return simplecrypt.decrypt(passkey, ctx)

    else:
        return None




@scheduled_return(interval=.01)
def ceasar(ctx, indent : int = 0) -> str:
    ctx = list(ctx)

    for idx, char in enumerate(ctx):

        char:str
        if not char.isspace():
            #ran_char_seq =  was assigned at line 22
            _index = RAN_CHAR_SEQ.index(char)
            try:
                new_char = RAN_CHAR_SEQ[_index + indent]
            
            except IndexError:
                if _index + indent > 72:
                    new_char = RAN_CHAR_SEQ[indent]
                
                elif _index + indent < 0:
                    new_char = RAN_CHAR_SEQ[72 - indent]
            ctx[idx] = new_char

    return "".join(ctx)


@scheduled_return(interval=.01)
def reverse_ceasar(ctx, indent : int = 0) -> str:

    return ceasar(ctx , -indent)


class Encryption :
    

    @staticmethod
    class SinglePwd :
        if TYPE_CHECKING :
            from user import User
    

        def __init__(self, user : User, ctx : str) -> None:
            self.user = user
            self.key = self.user.key
            if not self.user.key_check :
                raise BadUserSetup("User object doesn't have an encryption key")

            else :
                self.enc_content = ctx.encode("latin-1")

                self.enc_json = json.loads(self.user.enc_json)
                self.publicKey = self.enc_json["publicKey"]
                self.publicKey = self.publicKey.encode("latin-1")
                self.publicKey = simple_crypt(self.key, self.publicKey, "dec")
                self.publicKey = PublicKey.load_pkcs1(self.publicKey)
                self.publicKey : PublicKey


                self.privateKey = self.enc_json["privateKey"]
                self.privateKey = self.privateKey.encode("latin-1")
                self.privateKey = simple_crypt(self.key, self.privateKey, "dec")
                self.privateKey = PrivateKey.load_pkcs1(self.privateKey)
                self.privateKey : PrivateKey

                self.dec_content = rsa.decrypt(self.enc_content, self.privateKey).decode()

        




        @classmethod
        def new_pwd(cls, user : User, ctx : str) :
            ...



    

    class UserEnc :
        if TYPE_CHECKING :
            from user import User

        
        def __init__(self, user : User) -> None:
            publicKey, privateKey = rsa.newkeys(GLOBAL_SECURITY)
            
            self.user = user
            self.key = self.user.key
            self.enc_json = json.loads(self.user.enc_json)


            self.publicKey = self.enc_json["publicKey"]
            self.publicKey = self.publicKey.encode("latin-1")
            self.publicKey = simple_crypt(self.key, self.publicKey, "dec")
            self.publicKey = PublicKey.load_pkcs1(self.publicKey)

            self.privateKey = self.enc_json["privateKey"]
            self.privateKey = self.privateKey.encode("latin-1")
            self.privateKey = simple_crypt(self.key, self.privateKey, "dec")
            self.privateKey = PrivateKey.load_pkcs1(self.privateKey)
            self.privateKey : PrivateKey





            del publicKey, privateKey




        def print_data(self) -> str:
            


            _json = json.loads(self.user.pwd_json)


            dec_json = _json.copy()

            for key, item in dec_json.items() :
                
                new_pwd = rsa.decrypt(dec_json[key]["pwd"].encode("latin-1"), self.privateKey)

                dec_json[key]["pwd"] = new_pwd.decode("latin-1")

            return json.dumps(dec_json)



        def reset(self) :
            ...


        
        @staticmethod
        def user_init(key : str) :
            publicKey, privateKey = rsa.newkeys(GLOBAL_SECURITY)


            publicKey = simple_crypt(key, publicKey.save_pkcs1())
            publicKey = publicKey.decode("latin-1")


            privateKey = simple_crypt(key, privateKey.save_pkcs1())
            privateKey = privateKey.decode("latin-1")

            return publicKey, privateKey, GLOBAL_SECURITY

    
        def encrypt(self, pwd : str) :
            return rsa.encrypt(pwd.encode("latin-1"),
                    self.publicKey).decode("latin-1")


        def decrypt(self, pwd : str) :
            return rsa.decrypt(pwd.encode("latin-1"), self.privateKey).decode("latin-1")
class Password :
    ...