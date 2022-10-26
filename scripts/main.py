#MYMODULES
from _utility import loop_switch, Dir_Reset, get_dirs
import encryption as enc
import user
from variables import MAINLOOP, USERLOOP, CHOICEFILTER




#PYTHONMODULES
import atexit
from collections import namedtuple
import os
from getpass import getpass
import sys








def main():

    while MAINLOOP:

        mode = input("mode:\n1.new user\n2.user\n3.exit\nChoice:")

        while CHOICEFILTER:

            try:
                mode = int(mode)               
            except ValueError:
                mode = input("Input needs to be an integer\nNew choice:")
                continue


            if mode not in (1, 2, 3) :
                mode = input("input needs to be an integer between 1 and 3\nNew choice:")
                continue

            break



        
        
        os.system('cls||clear')
        print(os.getcwd())
        
        if mode == 1:

            with Dir_Reset.from_string("data/user_data") :
        
                dirs = get_dirs()
                name = input("name:")
                while CHOICEFILTER:

                    if not name.isalpha():
                        name = input("Input needs to be a string\nNew name:")
                        continue

                    elif name in (names.stem for names in dirs) :
                        name = input("Name already exists\nNew name:")
                        continue
                    
                    
                    break


            key = getpass()

            while CHOICEFILTER:

                if key == getpass("Confirm password:"):
                    break

                else:
                    print("confirmation failed")
                    key = getpass("Give new password:")

            #user.user_init(name, key)



        if mode == 2 :
            ...



        if mode == 3 :
            sys.exit()





if __name__ == "__main__" :
    os.system("Title Password manager")
    main()