import os
from Crypto.Hash import MD5

def get_file_checksum(filename):
    h = MD5.new()
    chunk_size = 8192
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if len(chunk) == 0:
                break
            h.update(chunk)
    print(h.hexdigest())
    return h.hexdigest()
filename = input("请输入文件名：")
get_file_checksum(filename)
check = input("回车退出")