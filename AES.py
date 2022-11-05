from Crypto.Cipher import AES
import base64
from Crypto.Util.Padding import pad, unpad
import secrets
import os
import hashlib
##加密参数制造模块
def ivgen():
    chose = ['0','1','2','3','4','5','6','7','8']
    iv = []
    i = 0
    while i<16:
        i+=1
        iv.append(secrets.choice(chose))
    return "".join(iv)
def keygen(bit):
    key = secrets.token_hex(bit)
    return key
##making end
##消息加密模块
def msg_en(text,key,iv):
    private_key = bytes(key, 'utf-8')
    iv = bytes(iv, 'utf-8')
    cipher = AES.new(private_key, AES.MODE_CBC, iv)

    encrypted = cipher.encrypt(pad(text.encode("UTF-8"), AES.block_size))
    return iv,base64.b64encode(encrypted).decode('utf-8')
##文件pad模块
def file_pad(text):
    while len(text) % 16 != 0:
        text += b'@'
    return text
##文件加密模块
def file_en(name,key,iv):
    ivname = iv
    private_key = bytes(key, 'utf-8')
    iv = bytes(iv, 'utf-8')
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    data = bytearray(os.path.getsize(name))    
    with open(name, 'rb') as f:        
        f.readinto(data)    
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    with open(name+"."+ivname, 'ba') as f:
        f.write(encrypted_data)

    

    return
##文件加密向导
def en_file_menu():
    print("1.指定密钥，或者自动生成密钥")
    keytype = input("输入16(32)由系统生成16(32)位密钥；或者手动输入指定的密钥，必须16或者32位。强烈推荐32位\n")
    if keytype == "16":
        key = keygen(8)
        print("您的密钥是",key)
    elif keytype == "32":
        key = keygen(16)
        print("您的密钥是",key)
    else:
        key = keytype
    print("2.初始向量生成中，本步骤无需您操作，虽然iv会附加在文件名，但还请记录生成的值，确保文件名更改后仍能解密。")
    iv = str(ivgen())
    print("IV生成结果",iv)
    name = input("3.输入您要加密的同目录文件名：\n")
    print("加密运行中...")
    file_en(name,key,iv)
    print("加密完成，加密后的文件保存在同目录下")
    return
##消息加密向导
def en_msg_menu():
    print("1.指定密钥，或者自动生成密钥")
    keytype = input("输入16(32)由系统生成16(32)位密钥；或者手动输入指定的密钥，必须16或者32位。强烈推荐32位\n")
    if keytype == "16":
        key = keygen(8)
        print("您的密钥是",key)
    elif keytype == "32":
        key = keygen(16)
        print("您的密钥是",key)
    else:
        key = keytype
    print("2.初始向量生成中，本步骤无需您操作，但请记录生成的值，这将用于解密。")
    iv = str(ivgen())
    print("IV生成结果",iv)
    text = input("3.输入您要加密的信息：\n")
    print("加密运行中...")
    iv,result = msg_en(text,key,iv)
    print("加密完成，结果如下")
    print(result)
    #print(iv)
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
    
##文件解密模块
def de_file(a,key,name):
    if a == 0:
        key = input("请输入密钥：")
        name = input("请输入完整文件名：")
    ivname = name[-17:]
    iv = name[-16:]
    private_key = bytes(key, 'utf-8')
    iv = bytes(iv, 'utf-8')
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    data = bytearray(os.path.getsize(name))    
    with open(name, 'rb') as f:        
        f.readinto(data)    
    encrypted_data = cipher.decrypt(data)
    #encrypted_data = cipher.decrypt(file_pad(data))如果出现问题恢复此句
    encrypted_data = unpad(encrypted_data,AES.block_size)
    with open(name[:-17], 'ba') as f:
        f.write(encrypted_data)
    if a == 0: print("成功，请查看文件夹下"+name[:-17])
##密钥生成助手
def helpkey():
    print("本算法通过您输入的常用密码计算加盐SHA-512一百万次，中间进行多次混淆，然后截取生成32位密钥。")
    print("注意如果您通过记忆输入的密码，获得密钥，解密时候请使用本助手再次输入密码获取密钥，确保盐值一致获得正确密钥")
    salt = "Y937kpargU68..Xv0_.8V_T_mv1O5n_rD_!Ez0NJ3Y!!,3g835xUBcsZ3W_.HSdi_.AsW3laWjC_7!!!!qNt.O!g75._TRK!,3b,!S!W!m..qz7sW.v6CAaU29.mStmh"    
    sugar = "e703f7bcaf7b472b9f368cfeb51334fc"
    password = input("请输入设定密码：")
    pwd = sugar+password+salt
    i = 0
    while True:
        i+=1
        sha512 = hashlib.sha512()
        sha512.update(pwd.encode('utf-8'))
        pwd = sha512.hexdigest()
        if i%163 == 0:
            pwd = pwd[17:71]
        elif i%1387 == 0:
            pwd = pwd[:67]
        elif i%10997 == 0:
            pwd = pwd[65:]
        if i>10000000: break
    return pwd[:32]
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
def menu():
    print("1.加密文件")
    print("2.加密文本")
    print("3.解密文件")
    print("4.解密文本")
    print("5.密钥生成助手（仅帮助您通过常用密码生成自定义密钥）")
    print("6.全自动加密测试模式（对于重要文件加密前进行测试确定当前平台可靠性）")
    print("0.退出程序")
    sel = input("请选择：\n")
    return sel
def main():
    print("欢迎来到树懒对称加密系统，本系统基于AES-CBC算法，pad方式为PKCS-7。请选择功能")
    while True:
        sel = menu()
        if sel == "1":
            en_file_menu()
        elif sel == "2":
            en_msg_menu()
        elif sel == "3":
            de_file(0,0,0)
            print("解密成功，文件在同目录")
        elif sel == "4":
            orgtext = de_msg(0,0,0,0)
            print(orgtext)
        elif sel == "5":
            hpkey = helpkey()
            print("生成的密钥为",hpkey)
        elif sel == "6":
            check()
        elif sel == "0":
            print("树懒加密退出中")
            break
        else:
            print("未知选项")
main()
