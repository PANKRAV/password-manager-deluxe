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
