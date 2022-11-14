"""
A module to help with the migration process 
It replaces the relative import 'from ..modules import user, encryption" which I couldn't get to work
"""


#THIRDPARTIES
import hashlib
import simplecrypt

#BUILTINS




#CONSTANTS
RAN_CHAR_SEQ = "hA#Fm&s%)0YanG$gQ3xylpvjB9f^M17S6eRCuqDZiwK*Ub!TLot4XV8@HONJ2rE5IcW(zdPk"






def hash3(ctx) -> str:
    byte_data = ctx.encode()
    return hashlib.sha3_512(byte_data).hexdigest()

def simple_crypt(passkey, ctx, mode : str = "enc") -> str:
    
    if mode == "enc":
        return simplecrypt.encrypt(passkey, ctx)

    elif mode == "dec":
        return simplecrypt.decrypt(passkey, ctx)

    else:
        return None

def ceasar(ctx, indent : int = 0) -> str:

    ctx = list(ctx)

    for idx, char in enumerate(ctx):

        char:str
        if not char.isspace():
            #ran_char_seq =  was assigned at line 22
            _index = RAN_CHAR_SEQ.index(char)
            try:
                new_char = RAN_CHAR_SEQ[_index + indent]
            
            except Exception:
                if _index + indent > 71:
                    new_char = RAN_CHAR_SEQ[indent - 71 - 1 + _index]
                
                elif _index + indent < 0:
                    new_char = RAN_CHAR_SEQ[71 - _index - indent]
            ctx[idx] = new_char

    return "".join(ctx)

def reverse_ceasar(ctx, indent : int = 0) -> str:

    return ceasar(ctx , -indent)
