import os
import hashlib

def get_file_checksum(filename):
    chunk_size = 8096

    md5 = hashlib.md5()
    sha256 = hashlib.sha256()
    sha512 = hashlib.sha512()
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if len(chunk) == 0:
                break
            md5.update(chunk)
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if len(chunk) == 0:
                break
            sha256.update(chunk)
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if len(chunk) == 0:
                break
            sha512.update(chunk)
            
    return md5.hexdigest(),sha256.hexdigest(), sha512.hexdigest()
def get_str_checksum(string):
    md5 = hashlib.md5()#
    sha256 = hashlib.sha256()#
    sha512 = hashlib.sha512()#

    md5.update(string.encode('utf-8')) #得到MD5消息摘要
    MD5OfString = md5.hexdigest()#以16进制返回消息摘要，32位
    
    sha256.update(string.encode('utf-8')) #得到MD5消息摘要
    sha256OfString = sha256.hexdigest()#以16进制返回消息摘要，32位
    
    sha512.update(string.encode('utf-8')) #得到MD5消息摘要
    sha512OfString = sha512.hexdigest()#以16进制返回消息摘要，32位

    
    return MD5OfString,sha256OfString,sha512OfString

if __name__ == '__main__':
    typ = input("Please input 1 for file HASH, 2 for string HASH \n")
    if typ == "1":
        filename = input("Please input file name: ")
        filemd5,filesha256,filesha512 = get_file_checksum(filename)
        print("File MD5:",filemd5)
        print("File SHA-256:",filesha256)
        print("File SHA-512:",filesha512)
        check = input("Enter to exit")
    elif typ == "2":
        string = input("Please input target string: ")
        MD5OfString,sha256OfString,sha512OfString = get_str_checksum(string)
        print("string MD5:",MD5OfString)
        print("string SHA-256:",sha256OfString)
        print("string SHA-512:",sha512OfString)
        check = input("Enter to exit")
