#MYMODULES
from _utility import _init
from variables import MAINLOOP, USERLOOP, CHOICEFILTER



#PYTHONMODULES
import atexit
from collections import namedtuple
import os
from getpass import getpass
from pwinput import pwinput
import sys








def main():

    from variables import user_data
    import encryption as enc
    from user import User
    from _utility import loop_switch, Dir_Reset, get_dirs, _quit

    while MAINLOOP:
        os.system("cls||clear")

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
        
        
        if mode == 1:

            with Dir_Reset.from_string("data/user_data") as cur:
        
                dirs = get_dirs()
                name = input("name:")
                while CHOICEFILTER:

                    if not name.isalpha():
                        name = input("Input needs to be a string\nNew name:")
                        continue

                    elif name in (names.stem for names in cur.pathlibdirs) :
                        name = input("Name already exists\nNew name:")
                        continue
                    
                    
                    break


            key = pwinput(prompt = "Password:")

            while CHOICEFILTER:

                if key == pwinput(prompt = "Confirm password:"):
                    loop_switch()
                    break

                else:
                    print("Confirmation failed")
                    key = pwinput(prompt = "New password:")

            user_data[name] = User.user_init(name, key)



        if mode == 2 :
            dirs = get_dirs("data/user_data")

            while USERLOOP :

                if len(dirs) == 1 :
                    print("they are no users yet\nmaybe create some")
                    input("continue :")
                    loop_switch()
                    break


                in_name = input("Give user name:\nor\n1.List Users\n2.Back\nChoice:")

                os.system("cls||clear")

                if in_name in (dir.stem for dir in dirs) :
                    _user : user.User = user_data[in_name]

                    in_key = pwinput(prompt = "Password:")

                    while CHOICEFILTER : #not exactly a CHOICEFILTER
                        if _user.check_key(in_key) :
                            loop_switch()
                            break

                        else :
                            print("Wrong key")
                            opt = input("1.Try again \n2.Exit:")


                            while CHOICEFILTER:

                                try:
                                    opt = int(opt)               
                                except ValueError:
                                    opt = input("Input needs to be an integer\nNew choice:")
                                    continue


                                if opt not in (1, 2) :
                                    opt = input("input needs to be an integer between 1 and 3\nNew choice:")
                                    continue

                                loop_switch()
                                break

                            if opt == 1 :
                                in_key = pwinput(prompt = "New password:")

                            else :
                                loop_switch()
                                break
                

                elif in_name == "1" :
                    os.system("cls||clear")
                    idx = []
                    users = []

                    print()

                    for index, user in enumerate(user_data, start = 1) :
                        print(f"{index}.{str(user)}")

                        users.append(user)
                        idx.append(index)

                    choice = input ("Choice:")

                    while CHOICEFILTER:

                        try:
                            choice = int(choice)               
                        except ValueError:
                            choice = input("Input needs to be an integer\nNew choice:")
                            continue


                        if choice not in idx :
                            choice = input(f"input needs to be an integer between {idx[0]} and {idx[:-1]}\nNew choice:")
                            continue

                        break

                    del idx
                    in_name = users[choice - 1]
                    _user : User = user_data[in_name]
                    del users

                    in_key = pwinput(prompt = "Password:")


                    while CHOICEFILTER : #not exactly a CHOICEFILTER
                        if _user.check_key(in_key) :
                            _user.acess()
                            break

                        else :
                            print("Wrong key")
                            opt = input("1.Try again \n2.Exit:")


                            while CHOICEFILTER:

                                try:
                                    opt = int(opt)               
                                except ValueError:
                                    opt = input("Input needs to be an integer\nNew choice:")
                                    continue


                                if opt not in (1, 2) :
                                    opt = input("input needs to be an integer between 1 and 3\nNew choice:")
                                    continue
                                break

                            if opt == 1 :
                                in_key = pwinput(prompt = "New password:")

                            else :
                                break


                elif in_name == "2" :
                    break

                else :
                    print("Account does not exist")



        if mode == 3 :
            _quit()





if __name__ == "__main__" :
    os.system("Title Password manager")
    _init()
    main()