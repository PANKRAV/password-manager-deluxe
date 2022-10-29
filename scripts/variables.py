from collections import namedtuple




#SEQUENCES
CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
LOWER = "abcdefghijklmnopqrstuvwxyz"
UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBERS = "0123456789"
SYMBOLS = "!@#$%^&*()"
RAN_CHAR_SEQ = "hA#Fm&s%)0YanG$gQ3xylpvjB9f^M17S6eRCuqDZiwK*Ub!TLot4XV8@HONJ2rE5IcW(zdPk"



#PATHS




#EXCEPTIONS
class ReadOnly(Exception):
    ...

class BadValue(Exception):
    ...


class UserFileExists(Exception):
    ...


class BadUserSetup(Exception):
    ...


class BadEnvSetup(Exception):
    ...




#LOOPS
CHOICEFILTER = True
SELFLOOP = True
MAINLOOP = True
USERLOOP = True



#DATA
def user_data_init() :
    from user import User
    global user_data
    user_data = dict()
    user_data = User.users_gen()


def global_security_init() :
    global GLOBAL_SECURITY
    from dotenv import load_dotenv
    from os import getenv
    from math import log2
    load_dotenv()
    GLOBAL_SECURITY = getenv("GLOBAL_SECURITY")

    try :
        GLOBAL_SECURITY = int(GLOBAL_SECURITY)
    
    except :
        raise BadEnvSetup

    level = log2(GLOBAL_SECURITY)
    if level != int(level) :
        raise BadEnvSetup



