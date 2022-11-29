from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Signature import PKCS1_v1_5 as sign_PKCS
import base64
from Crypto.Hash import SHA3_512
from tkinter import *
import tkinter.filedialog
import os
import tkinter.messagebox
import time
import threading
import tkinter.ttk

class radiobutton:
    global algg,direction,upwd,name
    def __init__(self):
        self.root = Tk()
        self.root.title("树懒公钥加密系统")  # 设置窗口标题
        self.root.geometry("1024x768")  # 设置窗口大小 注意：是x 不是*

        self.onekey = IntVar()

        self.genkeylabel = Label(self.root, text='1.密钥生成',font=('微软雅黑', 15,'bold'))
        self.genkey = Button(self.root, text='生成全新公私密钥对',font=('微软雅黑', 12,'bold'))

        self.mykeylabel = Label(self.root, text='2.导入我方密钥对',font=('微软雅黑', 15,'bold'))
        self.findmypub = Button(self.root, text='选择公钥',font=('微软雅黑', 12,'bold'))
        self.findmypri = Button(self.root, text='选择私钥',font=('微软雅黑', 12,'bold'))

        self.hiskeylabel = Label(self.root, text='3.导入对方公钥',font=('微软雅黑', 15,'bold'))
        self.findhispub = Button(self.root, text='选择公钥',font=('微软雅黑', 12,'bold'))
        self.checkone = Checkbutton(self.root, text="仅使用一把公钥加密，请作为对方公钥导入.",font=('微软雅黑', 15,'bold'),variable = self.onekey,onvalue=1,offvalue=0)

        self.textlabel = Label(self.root, text='4.输入信息',font=('微软雅黑', 15,'bold'))
        self.text = Text(self.root,height=13,width=80,font=('微软雅黑', 10,'bold'))

        self.filelabel = Label(self.root, text='5.加密小文件',font=('微软雅黑', 15,'bold'))
        self.findfile = Button(self.root, text='浏览',font=('微软雅黑', 12,'bold'))
        self.warn = Label(self.root, text='警告：公钥算法非常缓慢，不适合加密大文件',font=('微软雅黑', 15,'bold'))

        self.conclulabel = Label(self.root, text='参数总结',font=('微软雅黑', 15,'bold'))
        self.conclu = Text(self.root,height=5,width=40,font=('微软雅黑', 10,'bold'),state=DISABLED)
        #开始网格布局

        #密钥生成
        self.genkeylabel.grid(row=1, column=0, sticky='W')
        self.genkey.grid(row=1, column=1, sticky='E')
        #导入我方
        self.mykeylabel.grid(row=2, column=0, sticky='W')
        self.findmypub.grid(row=2, column=1, sticky='W')
        self.findmypri.grid(row=2, column=2, sticky='W')
        #导入对方
        self.hiskeylabel.grid(row=3, column=0, sticky='W')
        self.findhispub.grid(row=3, column=1, sticky='W')
        self.checkone.grid(row=3, column=2,columnspan=99, sticky='W')
        #文本输入区
        self.textlabel.grid(row=4, column=0, sticky='W')
        self.text.grid(row=4, column=1,columnspan=99, sticky='W')
        #文件区
        self.filelabel.grid(row=5, column=0, sticky='W')
        self.findfile.grid(row=5, column=1, sticky='W')
        self.warn.grid(row=5, column=2,columnspan=99, sticky='W')
        #总结区域
        self.conclulabel.grid(row=6, column=0, sticky='W')
        self.conclu.grid(row=6, column=1,columnspan=99, sticky='W')
        self.root.mainloop()
if __name__ == '__main__':
    radiobutton()
