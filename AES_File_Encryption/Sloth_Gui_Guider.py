import secrets
import Sloth_PasswordGen
import Sloth_GetSalt
import Sloth_AES
import Sloth_ChaCha
from Crypto.Random import get_random_bytes

def Gui_Guider(algg,direction,upwd,name):
    if algg==1 or algg == "1":#aes
        if direction =="1" or direction==1:#en
            salt = get_random_bytes(32)
            key = Sloth_PasswordGen.helpkey(upwd,salt)
            Sloth_AES.en_file(name,salt,key)
        elif direction=="2" or direction==2:#de
            if algg==1 or algg == "1":
                name=name[:-10]
            else:
                name=name[:-14]
            salt = Sloth_GetSalt.getfilesalt(name)
            key = Sloth_PasswordGen.helpkey(upwd,salt)
            Sloth_AES.de_file(name,key)
    elif algg == 2 or algg =="2":#cha
        if direction =="1" or direction==1:#en
            salt = get_random_bytes(32)
            key = Sloth_PasswordGen.helpkey(upwd,salt)
            Sloth_ChaCha.en_file(name,salt,key)
        elif direction=="2" or direction==2:#de
            if algg==1 or algg == "1":
                name=name[:-10]
            else:
                name=name[:-14]
            salt = Sloth_GetSalt.getfilesalt(name)
            key = Sloth_PasswordGen.helpkey(upwd,salt)
            Sloth_ChaCha.de_file(name,key)
