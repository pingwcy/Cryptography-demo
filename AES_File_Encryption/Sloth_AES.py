from Crypto.Cipher import AES
import base64
import secrets
import os
import hashlib

def en_file(filename,salt,key):
    BUFFER_SIZE = 1024 * 1024  # The size in bytes that we read, encrypt and write to at once


    input_filename = filename  # Any file extension will work
    output_filename = input_filename + '.SafeSloth'  # You can name this anything, I'm just putting .encrypted on the end

# Open files
    file_in = open(input_filename, 'rb')  # rb = read bytes. Required to read non-text files
    file_out = open(output_filename, 'wb')  # wb = write bytes. Required to write the encrypted data
    file_out.write(salt)  # Write the salt to the top of the output file

    cipher = AES.new(key, AES.MODE_GCM)  # Create a cipher object to encrypt data
    file_out.write(cipher.nonce)  # Write out the nonce to the output file under the salt
    print("The nonce of AES-GCM is :",(cipher.nonce).hex())
    print("The key of AES-GCM is :",key.hex())
# Read, encrypt and write the data
    data = file_in.read(BUFFER_SIZE)  # Read in some of the file
    while len(data) != 0:  # Check if we need to encrypt anymore data
        encrypted_data = cipher.encrypt(data)  # Encrypt the data we read
        file_out.write(encrypted_data)  # Write the encrypted data to the output file
        data = file_in.read(BUFFER_SIZE)  # Read some more of the file to see if there is any more left

# Get and write the tag for decryption verification
    tag = cipher.digest()  # Signal to the cipher that we are done and get the tag
    file_out.write(tag)

# Close both files
    file_in.close()
    file_out.close()

def de_file(filename,key):
    BUFFER_SIZE = 1024 * 1024  # The size in bytes that we read, encrypt and write to at once


    input_filename = filename+'.SafeSloth'  # The encrypted file
    output_filename = filename  # The decrypted file

# Open files
    file_in = open(input_filename, 'rb')
    file_out = open(output_filename, 'wb')

# Read salt and generate key
    salt = file_in.read(32)  # Only to continue here, The salt we generated was 32 bits long

# Read nonce and create cipher
    nonce = file_in.read(16)  # The nonce is 16 bytes long
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

# Identify how many bytes of encrypted there is
# We know that the salt (32) + the nonce (16) + the data (?) + the tag (16) is in the file
# So some basic algebra can tell us how much data we need to read to decrypt
    file_in_size = os.path.getsize(input_filename)
    encrypted_data_size = file_in_size - 32 - 16 - 16  # Total - salt - nonce - tag = encrypted data

# Read, decrypt and write the data
    for _ in range(int(encrypted_data_size / BUFFER_SIZE)):  # Identify how many loops of full buffer reads we need to do
        data = file_in.read(BUFFER_SIZE)  # Read in some data from the encrypted file
        decrypted_data = cipher.decrypt(data)  # Decrypt the data
        file_out.write(decrypted_data)  # Write the decrypted data to the output file
    data = file_in.read(int(encrypted_data_size % BUFFER_SIZE))  # Read whatever we have calculated to be left of encrypted data
    decrypted_data = cipher.decrypt(data)  # Decrypt the data
    file_out.write(decrypted_data)  # Write the decrypted data to the output file

# Verify encrypted file was not tampered with
    tag = file_in.read(16)
    try:
        cipher.verify(tag)
    except ValueError as e:
        # If we get a ValueError, there was an error when decrypting so delete the file we created
        file_in.close()
        file_out.close()
        os.remove(output_filename)
        raise e

# If everything was ok, close the files
    file_in.close()
    file_out.close()

##消息加密模块
def msg_en(text,key,iv):
    private_key = bytes(key, 'utf-8')
    iv = bytes(iv, 'utf-8')
    cipher = AES.new(private_key, AES.MODE_CBC, iv)

    encrypted = cipher.encrypt(pad(text.encode("UTF-8"), AES.block_size))
    return iv,base64.b64encode(encrypted).decode('utf-8')

    

##消息解密模块
def de_msg(a,key,iv,text):
    if a == 0:
        key = input("请输入密钥：")
        iv= input("请输入初始向量：")
        text = input("请输入密文：")
    data = text.encode('utf8')
    encodebytes = base64.decodebytes(data)
    # 将加密数据转换位bytes类型数据
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, iv.encode('utf8'))
    text_decrypted = cipher.decrypt(encodebytes)
    # 去补位
    text_decrypted = unpad(text_decrypted,AES.block_size)
    text_decrypted = text_decrypted.decode('utf8')
    return text_decrypted
    
def check():
    StringForTest = str('T38O69Z5Z7,860p7..ZZ,_aZXen2eqG0Ja_4p4nNP,,nx94t62O6B8cv!67_jR!L!72M!cculVMuGF7WMG8_oTlpwQs813Iw4uUwGpD_.T!dj2y.AP42dpsA_jn07M4Z')
    FileForTest = open("SuperSloth.txt","a")
    FileContent = str('rv1N0_M4Hn_8!,k.05m6TNU8,rV.0p!!X58v2ap4,GbR6_czcQ_ww8qilvAxT2_1Nz,,Qk,zGRy6u,gA.505zGjcz__7!c7,7ghW_lC9T5d88JOA_,6f._Tm!2HTWaJ,7G,p75q0.,4!M_,,LMs6y1_MgJ!FR4Qb_qMKCs!PuWC3!t1G21mLq2I!._7,,,u_.!Oi5KiLH094_R9n_!uis7.G1u7k0D2KGOO4K._1ile_kKB1_!jNU1.l0_F4Vy44')
    FileForTest.write(str(FileContent))
    FileForTest.close()##creat test message and test file
    ##获取字符串MD5
    md5S0 = hashlib.md5()#获取一个MD5的加密算法对象
    md5S0.update(StringForTest.encode('utf-8')) #得到MD5消息摘要
    MD5OfString0 = md5S0.hexdigest()#以16进制返回消息摘要，32位
    ##获取文件MD5
    with open('SuperSloth.txt', 'rb') as fp:
        data = fp.read()
    MD5OfFile0 = hashlib.md5(data).hexdigest()
    #指定密钥
    key = secrets.token_hex(16)
    iv = ivgen()
    ##启动字符串加密
    ivv,StringEn = msg_en(StringForTest,key,iv)
    ##启动文件加密
    file_en('SuperSloth.txt',key,iv)
    ##删除原文件
    os.remove("SuperSloth.txt")
    ##解密字符串
    EndStr = de_msg(1,key,iv,StringEn)
    ##解密文件
    de_file(1,key,("SuperSloth.txt"+"."+iv))
    ##获取解密后字符串MD5
    md5S1 = hashlib.md5()#获取一个MD5的加密算法对象
    md5S1.update(EndStr.encode('utf-8')) #得到MD5消息摘要
    MD5OfString1 = md5S1.hexdigest()#以16进制返回消息摘要，32位
    ##获取解密后文件MD5
    with open('SuperSloth.txt', 'rb') as fps:
        datas = fps.read()
    MD5OfFile1 = hashlib.md5(datas).hexdigest()
    ##对比字符串MD5
    
    if MD5OfString1 == MD5OfString0:
        print("字符串测试通过！")
    else:
        print("字符串测试出错！可能是系统环境问题")
    ##对比文件MD5
    if MD5OfFile1 == MD5OfFile0:
        print("文件测试通过！")
    else:
        print("文件测试出错！无法加密文件")
    if MD5OfString1 == MD5OfString0 and MD5OfFile1 == MD5OfFile0: print("全部通过，可以处理重要文件")
    ##删除所有测试文件
    os.remove("SuperSloth.txt")
    rem = str("SuperSloth.txt"+"."+iv)
    os.remove(rem)
