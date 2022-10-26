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