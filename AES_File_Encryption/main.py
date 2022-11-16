#this is main program, only for menu and interactive at beginning
import Sloth_Guider
import Sloth_Checker
def ini():
    print("Welcome to Sloth encrypt system, please select your algorithm first")
    print("In order to ensure the security, we only provide AES-GCM and ChaCha20_Poly1305, and only 256-bits key.")
    print("Additionally, we use scrypt as key generator")
    print("Please enter 1 for AES-GCM and 2 for ChaCha20_Poly1305, keep same choice when decryption")
    alg = input("Your choice: ")
    if alg == "1":
        return alg
    elif alg == "2":
        return alg
def menu():
    print("Chose function")
    print("1.encrypt file")
    print("2.encrypt message")
    print("3.decrypt file")
    print("4.decrypt message")
    print("5.Auto test to make sure environment is available")
    print("0.Exit")
    sel = input("Your choice：\n")
    return sel
def main():
    alg = ini()
    while True:
        sel = menu()
        if sel == "1":            
            Sloth_Guider.en_file_menu(alg)
        elif sel == "2":            
            Sloth_Guider.en_msg_menu(alg)
        elif sel == "3":            
            Sloth_Guider.de_file_menu(alg)
        elif sel == "4":            
            Sloth_Guider.de_msg_menu(alg)
        elif sel == "5":
            Sloth_Chcker.check()
        elif sel == "0":
            print("Exited")
            break
main()
