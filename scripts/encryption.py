#PYTHONMODULES
from numpy import character, random as nprand
import numpy as np
import hashlib
from rsa import PrivateKey, PublicKey
import cryptography
from simplecrypt import encrypt, decrypt
from cryptography.fernet import Fernet
import pathlib


#MYMODULES
from variables import CHARS, LOWER, UPPER, NUMBERS, SYMBOLS



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
def hash2(ctx) -> str:
    byte_data = ctx.encode()
    return hashlib.sha512(byte_data).hexdigest()

def hash3(ctx) -> str:
    byte_data = ctx.encode()
    return hashlib.sha3_512(byte_data).hexdigest()

def salt(ctx : str) -> str:
    salt = random_password(5)
    return ctx + salt









class Password:
    ...