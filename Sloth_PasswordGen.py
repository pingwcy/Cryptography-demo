from Crypto.Protocol.KDF import scrypt
def helpkey(password,salt):
    key = scrypt(password, salt, key_len=32, N=2**20, r=8, p=1)  # Generate a key using the password and salt
    return key
