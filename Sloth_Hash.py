import os
import hashlib
from tkinter import *
import tkinter.filedialog

global chunk_size
chunk_size = 8192

def Md5(typ,content):
    obj = hashlib.md5()
    if typ == 1:
        obj.update(content.encode('utf-8'))
    else:
        with open(content, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if len(chunk) == 0:
                    break
                obj.update(chunk)
    return obj.hexdigest()

def Sha1(typ,content):
    obj = hashlib.sha1()
    if typ == 1:
        obj.update(content.encode('utf-8'))
    else:
        with open(content, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if len(chunk) == 0:
                    break
                obj.update(chunk)
    return obj.hexdigest()

def Sha256(typ,content):
    obj = hashlib.sha256()
    if typ == 1:
        obj.update(content.encode('utf-8'))
    else:
        with open(content, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if len(chunk) == 0:
                    break
                obj.update(chunk)
    return obj.hexdigest()

def Sha512(typ,content):
    obj = hashlib.sha512()
    if typ == 1:
        obj.update(content.encode('utf-8'))
    else:
        with open(content, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if len(chunk) == 0:
                    break
                obj.update(chunk)
    return obj.hexdigest()
def Sha3256(typ,content):
    obj = hashlib.sha3_256()
    if typ == 1:
        obj.update(content.encode('utf-8'))
    else:
        with open(content, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if len(chunk) == 0:
                    break
                obj.update(chunk)
    return obj.hexdigest()

def Sha3512(typ,content):
    obj = hashlib.sha3_512()
    if typ == 1:
        obj.update(content.encode('utf-8'))
    else:
        with open(content, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if len(chunk) == 0:
                    break
                obj.update(chunk)
    return obj.hexdigest()


class radiobutton:

    def __init__(self):
        root = Tk()
        root.title("树懒哈希计算器")  # 设置窗口标题
        root.geometry("1000x500")  # 设置窗口大小 注意：是x 不是*
        '''单选框样式'''
        # 算法选择
        self.CheckVar1 = IntVar()
        self.CheckVar2 = IntVar()
        self.CheckVar3 = IntVar()
        self.CheckVar4 = IntVar()
        self.CheckVar5 = IntVar()
        self.CheckVar6 = IntVar()

        self.rb_alg_Label = Label(root, text='选择计算范围：',font=('微软雅黑', 15,'bold'))
        self.check1 = Checkbutton(root, text="MD5",font=('微软雅黑', 15,'bold'),variable = self.CheckVar1,onvalue=1,offvalue=0)
        self.check2 = Checkbutton(root, text="SHA1",font=('微软雅黑', 15,'bold'),variable = self.CheckVar2,onvalue=1,offvalue=0)
        self.check3 = Checkbutton(root, text="SHA256",font=('微软雅黑', 15,'bold'),variable = self.CheckVar3,onvalue=1,offvalue=0)
        self.check4 = Checkbutton(root, text="SHA512",font=('微软雅黑', 15,'bold'),variable = self.CheckVar4,onvalue=1,offvalue=0)
        self.check5 = Checkbutton(root, text="SHA3_256",font=('微软雅黑', 15,'bold'),variable = self.CheckVar5,onvalue=1,offvalue=0)
        self.check6 = Checkbutton(root, text="SHA3_512",font=('微软雅黑', 15,'bold'),variable = self.CheckVar6,onvalue=1,offvalue=0)

        # 加密解密方向选择
        self.iv_direction = IntVar()
        self.rb_direction_Label = Label(root, text='选择计算对象类型：',font=('微软雅黑', 15,'bold'))
        self.rb_direction1 = Radiobutton(root, text='字符串哈希', font=('微软雅黑', 15,'bold'),value=1, variable=self.iv_direction)
        self.rb_direction2 = Radiobutton(root, text='文件哈希', font=('微软雅黑', 15,'bold'),value=2, variable=self.iv_direction)
        self.iv_direction.set(2)
        self.iv_password = IntVar()
        self.rb_password_Label = Label(root, text='输入要计算的字符串：',font=('微软雅黑', 15,'bold'))
        self.rb_password1 = Entry(root,width=80)

        # 文件选择器
        self.iv_file = IntVar()
        self.rb_file_Label = Label(root, text='选择文件计算哈希：', font=('微软雅黑', 15,'bold'))
        self.rb_file = Button(root, text='浏览', font=('微软雅黑', 15,'bold'), command=self.function2)
        
        self.iv_all1= IntVar()
        self.all_alg1 = Label(root, text='文件目录： ', font=('微软雅黑', 15,'bold'))
        self.all_alg2 = Label(root, text='', font=('微软雅黑', 15,'bold'))
        # 启动按钮
        self.iv_start = IntVar()
        self.rb_start = Button(root, text='开始计算', font=('微软雅黑', 15,'bold'), command=self.function1)
        self.clean = Button(root,text='清空输出框', font=('微软雅黑', 15,'bold'), command=self.function3)
        #总结标签
        self.te = Text(root,height=15,width=120,state=DISABLED)
        self.scr = Scrollbar(root)
        self.te.config(yscrollcommand=self.scr.set)
        self.scr.config(command=self.te.yview)
        '''grid布局'''
        self.rb_alg_Label.grid(row=2, column=0, sticky='E')
        self.check1.grid(row=2, column=1, sticky='W')
        self.check2.grid(row=2, column=2, sticky='W')
        self.check3.grid(row=2, column=3, sticky='W')
        self.check4.grid(row=2, column=4, sticky='W')
        self.check5.grid(row=2, column=5, sticky='W')
        self.check6.grid(row=2, column=6, sticky='W')

        self.rb_direction_Label.grid(row=3, column=0, sticky='E')
        self.rb_direction1.grid(row=3, column=1, sticky='W')
        self.rb_direction2.grid(row=3, column=2, sticky='W')

        self.rb_password_Label.grid(row=4, column=0,columnspan=1, sticky='E')
        self.rb_password1.grid(row=4, column=1, columnspan=9,sticky='W')

        self.rb_file_Label.grid(row=5, column=0, sticky='E')
        self.rb_file.grid(row=5, column=1, sticky='W')

        self.all_alg1.grid(row=6, column=0, sticky='E')
        self.all_alg2.grid(row=6, column=1, columnspan=99, sticky='W')

        self.rb_start.grid(row=7, column=4, sticky='W')
        self.clean.grid(row=7, column=2, sticky='W')
        self.te.grid(row=8, column=0, columnspan=7, sticky='E')
        self.scr.grid(row=8,column=9,sticky=N+S)
        root.mainloop()
 
    def function1(self):
        self.te.config(state=NORMAL)
        before = self.te.get(1.0,END)
        self.te.delete(1.0,END)
        a,b,c,d,e,f=0,0,0,0,0,0
        a = self.CheckVar1.get()
        b = self.CheckVar2.get()
        c = self.CheckVar3.get()
        d = self.CheckVar4.get()
        e = self.CheckVar5.get()
        f = self.CheckVar6.get()
        typ = self.iv_direction.get()
        if typ == 1:
            content = self.rb_password1.get()
            self.te.insert(1.0,"---------------"+str(content)+"计算结果----------------\n")
            if a == 1:
                value=Md5(typ,str(content))
                self.te.insert(2.0,'MD5值为：')
                value = value+"\n\n"
                self.te.insert(3.0,value)
            if b == 1:
                value=Sha1(typ,str(content))
                self.te.insert(4.0,'Sha1值为：')
                value = value+"\n\n"
                self.te.insert(5.0,value)
            if c == 1:
                value=Sha256(typ,str(content))
                self.te.insert(6.0,'Sha256值为：')
                value = value+"\n\n"
                self.te.insert(7.0,value)
            if d == 1:
                value=Sha512(typ,str(content))
                self.te.insert(8.0,'Sha512值为：')
                value = value+"\n\n"
                self.te.insert(9.0,value)
            if e == 1:
                value=Sha3256(typ,str(content))
                self.te.insert(10.0,'Sha3_256值为：')
                value = value+"\n\n"
                self.te.insert(11.0,value)
            if f == 1:
                value=Sha3512(typ,str(content))
                self.te.insert(12.0,'Sha3_512值为：')
                value = value+"\n\n"
                self.te.insert(13.0,value)
            self.te.insert(14.0,'------------结束-------------\n')
            self.te.insert(15.0, before)
        if typ == 2:
            if name != '':
                self.te.insert(1.0,"---------------"+str(name)+"计算结果----------------\n")
                if a == 1:
                    value=Md5(typ,name)
                    self.te.insert(2.0,'MD5值为：')
                    value = value+"\n\n"
                    self.te.insert(3.0,value)
                if b == 1:
                    value=Sha1(typ,name)
                    self.te.insert(4.0,'SHA1值为：')
                    value = value+"\n\n"
                    self.te.insert(5.0,value)
                if c == 1:
                    value=Sha256(typ,name)
                    self.te.insert(6.0,'SHA256值为：')
                    value = value+"\n\n"
                    self.te.insert(7.0,value)
                if d == 1:
                    value=Sha512(typ,name)
                    self.te.insert(8.0,'SHA512值为：')
                    value = value+"\n\n"
                    self.te.insert(9.0,value)
                if e == 1:
                    value=Sha3256(typ,name)
                    self.te.insert(10.0,'SHA3_256值为：')
                    value = value+"\n\n"
                    self.te.insert(11.0,value)
                if f == 1:
                    value=Sha3512(typ,name)
                    self.te.insert(12.0,'SHA3_512值为：')
                    value = value+"\n"
                    self.te.insert(13.0,value)
                self.te.insert(14.0,'------------结束-------------\n')
                self.te.insert(15.0, before)
        self.te.config(state=DISABLED)
    def function2(self):
        filename = tkinter.filedialog.askopenfilename()
        if filename != '':
            global name
            name = filename
            self.all_alg2.config(text=name)
    def function3(self):
        self.te.config(state=NORMAL)
        self.te.delete(1.0,END)
        self.te.config(state=DISABLED)
if __name__ == '__main__':
    radiobutton()
