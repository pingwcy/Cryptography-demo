from tkinter import *
import tkinter.filedialog
import Sloth_Gui_Guider
 
class radiobutton:

    def __init__(self):
        root = Tk()
        root.title("树懒加密系统")  # 设置窗口标题
        root.geometry("900x300")  # 设置窗口大小 注意：是x 不是*
        '''单选框样式'''
        # 算法选择
        self.iv_alg = IntVar()
        self.rb_alg_Label = Label(root, text='选择算法：')
        self.rb_alg1 = Radiobutton(root, text='AES256-GCM', value=1, variable=self.iv_alg)
        self.rb_alg2 = Radiobutton(root, text='xChaCha20-Poly1305', value=2, variable=self.iv_alg)
        #iv_alg.set(1)
        # 加密解密方向选择
        self.iv_direction = IntVar()
        self.rb_direction_Label = Label(root, text='加解密选择：')
        self.rb_direction1 = Radiobutton(root, text='加密', value=1, variable=self.iv_direction)
        self.rb_direction2 = Radiobutton(root, text='解密', value=2, variable=self.iv_direction)
        #iv_direction.set(1)

        # 密码输入
        self.iv_password = IntVar()
        self.rb_password_Label = Label(root, text='输入或设置密码：')
        self.rb_password1 = Entry(root,width=80)
        # 文件选择器
        self.iv_file = IntVar()
        self.rb_file_Label = Label(root, text='选择加解密文件：')
        self.rb_file = Button(root, text='浏览', command=self.function2)
        #提交参数
        self.iv_ok = IntVar()
        self.save = Button(root, text='保存参数', command=self.function3)
        # 启动按钮
        self.iv_start = IntVar()
        self.rb_start = Button(root, text='启动加解密',  state=DISABLED, command=self.function1)
        # 哈希工具
        self.iv_click_colour = IntVar()
        self.rb_click_colour_Label = Label(root, text='鼠标点击颜色：')
        #总结标签
        self.iv_all1= IntVar()
        self.all_alg1 = Label(root, text='算法： ')
        self.all_direction1 = Label(root, text='加解密： ')
        self.all_password1 = Label(root, text='密码： ')
        self.all_file1 = Label(root, text='文件目录和名称： ')

        #总结内容
        self.iv_all = IntVar()
        self.all_alg = Label(root, text='空')
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
        Sloth_Gui_Guider.Gui_Guider(algg,direction,upwd,name)
        #print("算法",algg,"方向",direction,"密码",upwd,"文件",name)
    def function2(self):
        filename = tkinter.filedialog.askopenfilename()
        if filename != '':
            global name
            name = filename
            self.rb_start.config(state=NORMAL)
            self.all_file.config(text=name)

            #lb.config(text = "您选择的文件是："+filename);
        #else:
            #lb.config(text = "您没有选择任何文件");
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
            self.all_direction.config(text='加密')
        elif self.iv_direction.get()==2:
            direction = "2"
            self.all_direction.config(text='解密')

        self.all_password.config(text=self.rb_password1.get())
        upwd=self.rb_password1.get()
        self.all_file.config(text=name)
if __name__ == '__main__':
    radiobutton()

