from tkinter import *
import tkinter.filedialog
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import os
from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Protocol.KDF import scrypt
import tkinter.messagebox
def helpkey(password,salt):
    key = scrypt(password, salt, key_len=32, N=2**20, r=8, p=1)  # Generate a key using the password and salt
    return key

def getfilesalt(filename):
    try:
        realfilename = filename+'.SafeSloth'
        file = open(realfilename, 'rb')
        salt = file.read(32)
        file.close()
    except:
        realfilename = filename+'.Cha.SafeSloth'
        file = open(realfilename, 'rb')
        salt = file.read(32)
        file.close()
    return salt

def en_file_cha(filename,salt,key):
    BUFFER_SIZE = 1024 * 1024  # The size in bytes that we read, encrypt and write to at once
    
    input_filename = filename  # Any file extension will work
    output_filename = input_filename + '.Cha.SafeSloth'  # You can name this anything, I'm just putting .encrypted on the end

    file_in = open(input_filename, 'rb')  # rb = read bytes. Required to read non-text files
    file_out = open(output_filename, 'wb')  # wb = write bytes. Required to write the encrypted data

    file_out.write(salt)  # Write the salt to the top of the output file
    nonce = get_random_bytes(24)
    file_out.write(nonce)  # Write out the nonce to the output file under the salt
    #print(cipher.nonce)
    aad = get_random_bytes(32)
    file_out.write(aad)
    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)# Create a cipher object to encrypt data
    cipher.update(aad)

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

def de_file_cha(filename,key):
    BUFFER_SIZE = 1024 * 1024  # The size in bytes that we read, encrypt and write to at once


    input_filename = filename+'.Cha.SafeSloth'  # The encrypted file
    output_filename = filename  # The decrypted file

# Open files
    file_in = open(input_filename, 'rb')
    file_out = open(output_filename, 'wb')

# Read salt and generate key
    salt = file_in.read(32)  # Only to continue here, The salt we generated was 32 bits long

# Read nonce and create cipher
    nonce = file_in.read(24)  # The nonce is 16 bytes long
    aad = file_in.read(32)
    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    cipher.update(aad)

# Identify how many bytes of encrypted there is
# We know that the salt (32) + the nonce (16) + the data (?) + the tag (16) is in the file
# So some basic algebra can tell us how much data we need to read to decrypt
    file_in_size = os.path.getsize(input_filename)
    encrypted_data_size = file_in_size - 104  # Total - salt - nonce - tag = encrypted data

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

def Gui_Guider(algg,direction,upwd,name):
    if algg==1 or algg == "1":#aes
        if direction =="1" or direction==1:#en
            salt = get_random_bytes(32)
            key = helpkey(upwd,salt)
            en_file(name,salt,key)
        elif direction=="2" or direction==2:#de
            if algg==1 or algg == "1":
                name=name[:-10]
            else:
                name=name[:-14]
            salt = getfilesalt(name)
            key = helpkey(upwd,salt)
            de_file(name,key)
    elif algg == 2 or algg =="2":#cha
        if direction =="1" or direction==1:#en
            salt = get_random_bytes(32)
            key = helpkey(upwd,salt)
            en_file_cha(name,salt,key)
        elif direction=="2" or direction==2:#de
            if algg==1 or algg == "1":
                name=name[:-10]
            else:
                name=name[:-14]
            salt = getfilesalt(name)
            key = helpkey(upwd,salt)
            de_file_cha(name,key)

class radiobutton:

    def __init__(self):
        root = Tk()
        root.title("Sloth Encryption")  # 设置窗口标题
        root.geometry("900x300")  # 设置窗口大小 注意：是x 不是*
        '''单选框样式'''
        # 算法选择
        self.iv_alg = IntVar()
        self.rb_alg_Label = Label(root, text='Chose algorithm：')
        self.rb_alg1 = Radiobutton(root, text='AES256-GCM', value=1, variable=self.iv_alg)
        self.rb_alg2 = Radiobutton(root, text='xChaCha20-Poly1305', value=2, variable=self.iv_alg)
        #iv_alg.set(1)
        # 加密解密方向选择
        self.iv_direction = IntVar()
        self.rb_direction_Label = Label(root, text='En/Decrypt：')
        self.rb_direction1 = Radiobutton(root, text='Encrypt', value=1, variable=self.iv_direction)
        self.rb_direction2 = Radiobutton(root, text='Decrypt', value=2, variable=self.iv_direction)
        #iv_direction.set(1)

        # 密码输入
        self.iv_password = IntVar()
        self.rb_password_Label = Label(root, text='Enter or set password：')
        self.rb_password1 = Entry(root,width=80)
        # 文件选择器
        self.iv_file = IntVar()
        self.rb_file_Label = Label(root, text='Chose a file to en/decrypt：')
        self.rb_file = Button(root, text='Browse', command=self.function2)
        #提交参数
        self.iv_ok = IntVar()
        self.save = Button(root, text='Save settings', command=self.function3)
        # 启动按钮
        self.iv_start = IntVar()
        self.rb_start = Button(root, text='Start',  state=DISABLED, command=self.function1)
        # 哈希工具
        self.iv_click_colour = IntVar()
        self.rb_click_colour_Label = Label(root, text='鼠标点击颜色：')
        #总结标签
        self.iv_all1= IntVar()
        self.all_alg1 = Label(root, text='Algorithm： ')
        self.all_direction1 = Label(root, text='En/Decrypt： ')
        self.all_password1 = Label(root, text='Password： ')
        self.all_file1 = Label(root, text='File Name： ')

        #总结内容
        self.iv_all = IntVar()
        self.all_alg = Label(root, text='None')
        self.all_direction = Label(root, text='')
        self.all_password = Label(root, text='')
        self.all_file = Label(root, text='')

        '''grid布局'''
        self.rb_alg_Label.grid(row=2, column=0, sticky='E')
        self.rb_alg1.grid(row=2, column=1, sticky='W')
        self.rb_alg2.grid(row=2, column=2, sticky='W')

        self.rb_direction_Label.grid(row=8, column=0, sticky='E')
        self.rb_direction1.grid(row=8, column=1, sticky='W')
        self.rb_direction2.grid(row=8, column=2, sticky='W')

        self.rb_password_Label.grid(row=14, column=0, sticky='E')
        self.rb_password1.grid(row=14, column=1, sticky='W')

        self.rb_file_Label.grid(row=20, column=0, sticky='E')
        self.rb_file.grid(row=20, column=1, sticky='W')
        #self.rb_direction2.grid(row=20, column=2, sticky='W')

        ##conclusion label
        self.all_alg1.grid(row=28, column=0, sticky='E')
        self.all_direction1.grid(row=30, column=0, sticky='E')
        self.all_password1.grid(row=32, column=0, sticky='E')
        self.all_file1.grid(row=34, column=0, sticky='E')
        ##conclusion content
        self.all_alg.grid(row=28, column=1, sticky='W')
        self.all_direction.grid(row=30, column=1, sticky='W')
        self.all_password.grid(row=32, column=1, sticky='W')
        self.all_file.grid(row=34, column=1, sticky='W')

        self.rb_start.grid(row=40, column=1, sticky='W')
        self.save.grid(row=40, column=2, sticky='W')

        root.mainloop()
 
    def function1(self):
        Gui_Guider(algg,direction,upwd,name)
        tkinter.messagebox.showinfo("提示","加解密处理完成")
        #print("算法",algg,"方向",direction,"密码",upwd,"文件",name)
    def function2(self):
        filename = tkinter.filedialog.askopenfilename()
        if filename != '':
            global name
            name = filename
            self.rb_start.config(state=NORMAL)
            self.all_file.config(text=name)

    def function3(self):
        global algg,direction,upwd

        if self.iv_alg.get()==1:
            algg= "1"
            self.all_alg.config(text='AES256-GCM')
        elif self.iv_alg.get()==2:
            algg= "2"
            self.all_alg.config(text='xChaCha20-Poly1305')

        if self.iv_direction.get()==1:
            direction = "1"
            self.all_direction.config(text='Encrypt')
        elif self.iv_direction.get()==2:
            direction = "2"
            self.all_direction.config(text='Decrypt')

        self.all_password.config(text=self.rb_password1.get())
        upwd=self.rb_password1.get()
        self.all_file.config(text=name)
if __name__ == '__main__':
    radiobutton()

