##alg 1: aes 2: chacha
import time
import secrets
import Sloth_PasswordGen
import Sloth_GetSalt
import Sloth_AES
from Crypto.Random import get_random_bytes

def en_file_menu(alg):
    filename = input("Please Input file name in full form: \n")
    pwdtyp = input("Please enter 1 for chose your own 32-length key and 2 for using password to generate key: \n")
    if pwdtyp == "1":
        key = input("Enter your own 32 length key: \n")
        salt = get_random_bytes(32)  # Generate salt
        key = Sloth_PasswordGen.helpkey(userpwd,salt)
        if alg == "1":
            Sloth_AES.en_file(filename,salt,key)
        elif alg == "2":
            pass
    else:
        userpwd = input("Enter your password in any form: \n")
        salt = get_random_bytes(32)  # Generate salt
        t1 = time.perf_counter()
        key = Sloth_PasswordGen.helpkey(userpwd,salt)
        t2 = time.perf_counter()
        print("The key is:",key,"\nCost time",t2-t1)
        if alg == "1":
            t1 = time.perf_counter()
            Sloth_AES.en_file(filename,salt,key)
            t2 = time.perf_counter()
            print("Completed, cost time",t2-t1)
        elif alg == "2":
            pass
def en_msg_menu(alg):
    string = input("Please input your message: \n")
    
def de_file_menu(alg):
    filename = input("Please input file name without .SafeSloth: \n")
    salt = Sloth_GetSalt.getfilesalt(filename)
    pwdtyp = input("Please enter 1 to input 32-length key and 2 for inputting password: \n")
    if pwdtyp == "1":
        key = input("Enter your own 32 length key: \n")
        if alg == "1":
            key = Sloth_PasswordGen.helpkey(userpwd,salt)
            Sloth_AES.de_file(filename,key)
        elif alg == "2":
            pass
    else:
        userpwd = input("Enter your password: \n")
        key = Sloth_PasswordGen.helpkey(userpwd,salt)
        if alg == "1":
            key = Sloth_PasswordGen.helpkey(userpwd,salt)
            Sloth_AES.de_file(filename,key)
        elif alg == "2":
            pass
def de_msg_menu(alg):
    pass
