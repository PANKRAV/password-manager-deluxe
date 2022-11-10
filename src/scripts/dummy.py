"""
A script used for debugging to create three(3) dummy files in :
- data/encryption_data
- data/password_data
- data/user_data
"""
import sys
sys.path.insert(0, 'C:\\Users\\USERPC\\Desktop\\python\\ey\\double_deluxe\\src\\modules')
from pathlib import Path
from scriptsutil import Dir_Reset
import os
from dotenv import load_dotenv
import json

load_dotenv()
debug = os.getenv("DEBUG")


_json = {
    "enc_json" : {"publicKey": "sc\u0000\u0002\u00ea\u00cf\u00ffA\u00ddPknh\u00e8LK\u00b8\u001e\u00ec{\u00eb\u0099\u00ecf\u00a3!\u00a5\u001a|\u00e6\u00deJ\u00dd\u008e\u0080\u00aaD\u00cfI\u00dc\u00f9\u00f4\u00bc\u00e6+\u00c3\"\u00c6|\u00e0\u00ec\u0087\u00e1&\u00ce\t\u0091\u0014\u00ad\u00bc@\u008c\u0093>\u00ad>\u00f8k\u0096\u00e2<\u007f\u00cb\u00c6\u0095\u0082\u0096t\u00a4\u0089.\u00ee\u00fb3\u001f\u00daC5\u00bcNkC\u00f5\u0003\u00f0\u00e4\u00cel\u0018\u00f2&\u00fc\u0001.\u00d9\u00d4\u00d0\u0092\u009dQ\u00ff\u00de\u0005\u00dfe\u00c7\u0019\u00e5\u0003\f\u00fa\u001b\u0080\u00d7q\u008b\u0010\u00a5\u00e56\u00e3T\u00fa\u00b0\u000e\u00a8Er\u008fk\u00d6\u001c\u0002\u00a0\u00881\u0087\u00a8P\u0014s\u00ea\u00aa\\\u0007\u001a\u00a5\u001a\"\u0084>\u00a1\u00a2\u00ce\u000e5M\u00de^\u00adG\u009f\u001a\u0006\b7\u00ac@\u00e60\u0099\u0084\u00d2\u00cc\u00f9s\u000b\u00c1\u0006Zz??\u00f4&\u00bf\u008bzm\u00c6\u00e6I\u00f8c \u00f8+\u00f9\u000f\u00c3\u0013\u000e'[\u0016\u00b7m\u0010:\u0003\"\u0002\u00f0\u0083XB^\u00b0bF", "privateKey": "sc\u0000\u0002!(\u00dc\u0012\b\u00c8\u00f3\u00a2\u00d4\u00a7!\u0007\u001f#\u00dd\u00f7\u00c9\u00b7\u00c7\u00cd\u00dah\u00d3\u00b9v\u00f6\u00a9\u0080\u00fer\u00eb\u00e3\u00df\u00ac\u00c2H\u0006dSY\u00ae+\u00ff\u0086\u00a1\u00b4\u000f`q%\u00c0bm\u00dc*\u0010r\u00bbb\u0019\u00c0\u00ea\u0090\u00d3%\u0097\u00a0\u00d5\u00a4\u00b6\u0095\u00b6\u00a5\u00e9\u00cc\u00b0\u00c3\u0090\u00ac#\u0085PV9:y\u00fe\u00c0\u00bba4P\u00bbJzr\u00c9I\u00e50\u00ad\u009f\u00f9\u00fb57~.\u009f/\u00a5\u00df$:{\u0015\u001d{\u009d\u00cf`\u00f1\u0015{\u00c9I\u009a|\u00e8\u008ey\u0004I\u00e2{\u00e8\u0083\u00f74\u0014(\u007fG\u0019\u00c6<m\u00f4O\u00eb~\u00a7\u0001gg6H\u00acxDvp\u0087\u008e\u0096\u00dd\u00ca\u00c8\u0097\u00cd\u0096\fHw\u0003\u00efe\u00b4\u0092\u00fc?\u00fa\u00a3{WP(\u0005\u00cbZ\u00892C\u00ad\u00daG\u0000g\u00e8?\u00d0\u0006\u0017#\u0002\u00806\u00f8\u00f7A\u00b8\\w\u00baN\u00a7>>\u00c9\u00e3\u00c2\u0091iZ\u00f7\u001a0\"yCN\u00ac\u009d\u00a7\u00fak%\u00d00\u00a3\u008bL\u008a \u0092'4\u0014\u00c4\u0081\u009dc\u00fe\u00a8\u0007\\((%u\u00beV\u0085f\u00ac\u00b49\u00a4\ta\u00d2yM]\u00fe7\u00b0l\u007f\u00be p\\q\u008c{=\u0093\u00bd\u0080\u00eb\u00f92]\u00c2\u00e6s\u00a0\u0004\u00d9?y\u00cb\u0018\u00a6\u00be\u00c2\u009d\u00bb\u0092\u00de\u008f\u0096\u00a0\u00da\u00fe4@Z&\u0085\u00e8\u0091I0\u00b0U3M03\u00ed\u00da\u00a5\u00df\u0014x\u00b5\u00e3-j\r\u0003\u00c7\u0005\u0019>\u00e0\u00b6\u001c\u0083N\u00f92,x\u0092o&\u00c1\u00f4w\u00c0\u00ecF\u00ba\n\u00e8\u00e0\u0081\u00f9Mn]\u00d0\u00ca+J\u00a3b\u00e9\u00cc\u0099\u00cc\bI2\u00ba^\\~U\u00dbk\u00c1\u00eb\u00a4\u00fb\u00c3h\u00bf\u00e0wKqPGS\u00e8\u00c5^7\u00b7\t\f3.5\u00b8\u009a\u00daCd\u00ff\u00ed\u009d\u00a8\u00a97\u0005\u00eb\u00b2|\u00d5p\u00c9\"\u0002\u00fa\u00f5{\u00b3SX\u00ef\u00af\u0015o\u00e2E\u00dc\u00a8'<\u00c0\"\u00018\u00cf\u00b8\u00d3\u0017`K\u00b1\u00d106\u00a3f\u00c5\u00ff\u00abx\u00eb\u00f7e\u00f5z\u00f3\u0013\u0011?\u00a1\u0095\u00c9`\u00fe*+\u00e4q\u008b\u0004\u009ev,fc~E\u00c7\nO\u009e7Sp\u009e\u0081'\u00c5\u00f2\u0097g\u0005c>\u00acgc,\u00ce\u00e7\u000f\u00f7\u00dc\u0093\u00f5\u0004\u00bfr\u00921\u009e\n\u00d1\u001e\u008a\u0084E\u0084\u00b5\u00c2%\b+L\u008d\u00f0q9\u00f1.\u00adT7\u0095\u0084\u0001[", "security": 512
    },
    "pwd_json" : {
        "esy": {
        "username": "egw",
        "pwd": "&4\u00e4o5\u00f5\u0000\u0096\u00d9\u0081\u00ecx)\u00a1j\u00f0;\u0003\u00b1\u00f6uqS\u00ec\u00ac)\u00ae\u0000\u00b3\u00c2At\u0006d\u0019-\u00ef\u001f\u0013J\u0099\u001a(\u00ff\u00121\u0007a\u00ba\u0094bd\u00aaq}q\u00d2\b\u00f6L\u0002\u00d0\u0019Q",
        #esy password : eX2@W#7m#8F@hBf7C6x0U&@hY*b5!I
        "email": "aifjhaed"
        },
        "autos": {
        "username": "egw",
        "pwd": "g\u008dif7R\u00c5,M_\u009b\u00c0\u0085)\u00ca\u009cb\u0001j\u0096\u000e\u00cf\u00fc\u00c5\u0086U\u00bf\u00c0\u00de\u00cd\u0094[\u00a13\u0082\u00ddju\u00c2R\u00dd\u00f1\u00f5\u0013\u0088^x\u0087\u0094-s\u00f0\u0081\u00e7+\u008da\u00f0f\u00ce2V\u00fc\u0096",
        #autos password : $ro
        "email": "pankrav"
        }
    },
    "user_json" : {
        "name": "a",
        "key": "2eb6049dc429fe12af0a6f1315051c10d73b768d1a7a95582ec278d471042139171013c9b7364219598faef36c923095ae7244cd441a943c9e0b2131f08de24d",
        #user key : a
        "salt": "32Q0%"
    }
}

def main():
    abspath = Path(os.path.abspath(__file__))
    os.chdir(abspath.parent.parent.parent)

    if debug == "1":
        with Dir_Reset.from_string("data/encryption_data") as cur :
            if "dummy.json" in cur.dirs :
                print("Overwriting previous data/encryption_data json file")
            with Path("dummy.json").open("wt") as w_f :
                w_f.write(json.dumps(_json["enc_json"], indent=4))

        with Dir_Reset.from_string("data/password_data") as cur :
            if "dummy.json" in cur.dirs :
                print("Overwriting previous data/password_data json file")
            with Path("dummy.json").open("wt") as w_f :
                w_f.write(json.dumps(_json["pwd_json"], indent=4))

        with Dir_Reset.from_string("data/user_data") as cur :
            if "dummy.json" in cur.dirs :
                print("Overwriting previous data/user_data json file")
            with Path("dummy.json").open("wt") as w_f :
                w_f.write(json.dumps(_json["user_json"], indent=4))



    elif debug == "0" :
        print("debug setting is turned off")

    else :
        print("bad .env configuration")


if __name__ == "__main__" :
    main()