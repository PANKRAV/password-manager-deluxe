"""
Contains any configuration for the project
"""

from collections import namedtuple
import logging
from threading import Lock

#MODULE INITIALIZER
def vars_init() :
    user_data_init()
    global_security_init()
    global_logging_init()
    users_to_reset_init()


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




#LOOPS/UTILITY
CHOICEFILTER = True
SELFLOOP = True
MAINLOOP = True
USERLOOP = True
Global_Lock = Lock()


#DATA
def user_data_init() :
    from .user import User
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


def global_logging_init() :
    global GLOBAL_LOGGING
    from dotenv import load_dotenv
    from os import getenv
    load_dotenv()
    GLOBAL_LOGGING = getenv("GLOBAL_LOGGING")

   
    if GLOBAL_LOGGING == "DEBUG" :
        GLOBAL_LOGGING = logging.DEBUG
    elif GLOBAL_LOGGING == "INFO" :
        GLOBAL_LOGGING = logging.INFO
    elif GLOBAL_LOGGING == "WARNING" :
        GLOBAL_LOGGING = logging.WARNING
    elif GLOBAL_LOGGING == "ERROR" :
        GLOBAL_LOGGING = logging.ERROR
    elif GLOBAL_LOGGING == "CRITICAL" :
        GLOBAL_LOGGING = logging.CRITICAL
    else :
        raise BadEnvSetup

def users_to_reset_init() :
    global users_to_reset
    users_to_reset = []


#CONSTANSTS

