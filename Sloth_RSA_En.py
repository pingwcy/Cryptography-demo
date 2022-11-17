from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Signature import PKCS1_v1_5 as sign_PKCS
import base64
from Crypto.Hash import SHA3_512
def menu():
    print("1.Generate New key pair and save to file")
    print("2.Import myself key pair")
    print("3.Import another people's public key")
    print("4.Encrypt and sign message")
    print("5.Decrypt and verify message")
    print("0.Exit")
    choice = input("Choice:\n")
    return choice
def main():
    print("Welcome to sloth RSA encryption, please choose your function")
    while True:
        choice = menu()
        if choice == "1":
            Pri = input("Specific private key name to save, full name:\n")
            Pub = input("Specific public key name to save, full name:\n")
            if key_gen(Pri,Pub) == True:
                print("Key generated success")
                isimport = input("Do you want to import them now? Y/N:\n")
                if isimport == "Y":
                    pub_key,pri_key= importpair(Pri,Pub)
                    if len(str(pub_key)) > 1:
                        print("Import key pair success")
                    else:
                        print("Error to import")
            else:
                print("Error in generation")
        elif choice == "2":
            Pri = input("Specific private key name to read, full name:\n")
            Pub = input("Specific public key name to read, full name:\n")
            pub_key,pri_key= importpair(Pri,Pub)
            if len(str(pub_key)) > 1:
                print("Import key pair success")
            else:
                print("Error to import")
        elif choice == "3":
            Pub = input("Specific public key name to read, full name:\n")
            ano_pub_key = importpublic(Pub)
            if len(str(ano_pub_key)) > 1:
                print("Import public key success")
            else:
                print("Error to import")
        elif choice == "4":
            info = input("Input the message you want to encrypt:\n")
            which = input("Which Public key do you want to use? 1 for myself, 2 for another\n")
            if which == "1":
                key = pub_key
                encmsg = enc(info,key)
            else:
                key = ano_pub_key
                encmsg = enc(info,key)
            print("The encrypted message is: ")
            print(encmsg)
            save = input("Do you want to save it in a file? Y/N\n")
            if save == "Y":
                name = input("Input file name to store:\n")
                try:
                    with open(name,'w') as file:
                        file.write(encmsg)
                    print("Save success")
                except ZeroDivisionError:
                    print("Save fail")
            issign = input("Do you want to sign it? Y/N\n")
            if issign == "Y":
                singa = tosign(info,pri_key)
                print("The sigature is: ")
                print(singa)
            saves = input("Do you want to save it in a file? Y/N\n")
            if saves == "Y":
                name = input("Input file name to store:\n")
                try:
                    with open(name,'w') as file:
                        file.write(singa)
                    print("Save success")
                except:
                    print("Save fail")

        elif choice == "5":
            isfile = input("Do you want to input or by file? 1 for input, 2 for file \n")
            if isfile == "2":
                fnm = input("Input file name:\n")
                with open(fnm) as fb:
                    encmsg = fb.read()
            else:
                encmsg = input("What encrypted message you want to decrypt?\n")
            key = pri_key
            try:
                decmsg = dec(encmsg,key)
                print("This messgage is:")
                print(decmsg)
            except:
                print("Key or encmsg fail.")
            ischeck = input("Do you want to verify the singature?Y/N \n")
            if ischeck == "Y":
                who = input("Which Public key do you want to use?1 for myself, 2 for another \n")
                where = input("Read from file or input? 1 for file, 2 for input \n")
                if where == "1":
                    pass
                else:   
                    singa = input("Input sigature:\n")
                if who == "1":
                    result = check(pub_key,decmsg,singa)
                else:
                    result = check(ano_pub_key,decmsg,singa)
                print(result)
        elif choice == "0":
            break
        else:
            print("Unknown Choice")
def key_gen(Pri,Pub):
    try:
#生成密钥对
        rsa = RSA.generate(4096)
#将私钥和公钥赋值给变量
        private_key = rsa.exportKey()
        public_key = rsa.publickey().exportKey()
#写入文件
        with open(Pri, 'wb') as f:
            f.write(private_key)
        with open(Pub, 'wb') as f:
            f.write(public_key)
            return True
    except:
            return False

def importpair(Pri,Pub):
    try:
        with open(Pub) as publicobj:
            public_key = publicobj.read()
            pub_key = RSA.importKey(str(public_key))
        with open(Pri) as privateobj:
            private_key = privateobj.read()
            pri_key = RSA.importKey(private_key)
        return pub_key,pri_key
    except:
        return 0,0
def importpublic(Pub):
    try:
        with open(Pub) as publicobj:
            public_key = publicobj.read()
            ano_pub_key = RSA.importKey(public_key)
            return ano_pub_key
    except:
        return None
def enc(message,key):
# 使用公钥对内容进行rsa加密
    cipher = PKCS1_v1_5.new(key)#创建加密对象
    rsa_text = base64.b64encode(cipher.encrypt(bytes(message.encode("utf8"))))
    return rsa_text.decode('utf-8')
def dec(encmsg,key):
# 使用私钥对内容进行rsa解密
    cipher = PKCS1_v1_5.new(key)
    back_text = cipher.decrypt(base64.b64decode(encmsg), 0)
    return back_text.decode('utf-8')
def tosign(message,key):
    singobj = sign_PKCS.new(key)
    sha = SHA3_512.new()
    sha.update(message.encode())
    signa = base64.b64encode(singobj.sign(sha))
    return signa.decode('utf8')
def check(key,message,singa):
    checkobj = sign_PKCS.new(key)
    sha = SHA3_512.new()
    sha.update(message.encode())
    result = checkobj.verify(sha,base64.b64decode(singa))
    return result
main()
