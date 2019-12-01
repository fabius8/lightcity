#!/usr/local/bin/python3

import tkinter as tk
'''松耦合'''
import os


# 弹窗
class MyDialog(tk.Toplevel):
  def __init__(self):
    super().__init__()
    self.title('设置用户信息')
    # 弹窗界面
    self.setup_UI()
  def setup_UI(self):
    # 第一行（两列）
    row1 = tk.Frame(self)
    row1.pack(fill="x")
    tk.Label(row1, text='用户名：', width=8).pack(side=tk.LEFT)
    self.username = tk.StringVar()
    tk.Entry(row1, textvariable=self.username, width=20).pack(side=tk.LEFT)
    # 第二行
    row2 = tk.Frame(self)
    row2.pack(fill="x", ipadx=1, ipady=1)
    tk.Label(row2, text='密码：', width=8).pack(side=tk.LEFT)
    self.passwd = tk.StringVar()
    tk.Entry(row2, textvariable=self.passwd, width=20).pack(side=tk.LEFT)
    # 第三行
    row3 = tk.Frame(self)
    row3.pack(fill="x", ipadx=1, ipady=1)
    tk.Label(row3, text='城市信息：', width=8).pack(side=tk.LEFT)
    self.city = tk.StringVar()
    tk.Entry(row3, textvariable=self.city, width=20).pack(side=tk.LEFT)

    row4 = tk.Frame(self)
    row4.pack(fill="x")
    tk.Button(row4, text="取消", command=self.cancel).pack(side=tk.RIGHT)
    tk.Button(row4, text="确定", command=self.ok).pack(side=tk.RIGHT)


  def ok(self):
    self.userinfo = [self.username.get(), self.passwd.get(), self.city.get()] # 设置数据
    self.destroy() # 销毁窗口

  def cancel(self):
    self.userinfo = None  # 空！
    self.destroy()

# 主窗
class MyApp(tk.Tk):
  def __init__(self):
    super().__init__()
    #self.pack() # 若继承 tk.Frame ，此句必须有！
    self.title('用户信息')
    # 程序参数/数据
    self.username = '13888888888'
    self.passwd = '88888888'
    self.city = '北京'
    # 程序界面
    self.setupUI()
  def setupUI(self):
    # 第一行（两列）
    row1 = tk.Frame(self)
    row1.pack(fill="x")
    tk.Label(row1, text='用户名：', width=8).pack(side=tk.LEFT)
    self.l1 = tk.Label(row1, text=self.username, width=20)
    self.l1.pack(side=tk.LEFT)
    # 第二行
    row2 = tk.Frame(self)
    row2.pack(fill="x")
    tk.Label(row2, text='密码：', width=8).pack(side=tk.LEFT)
    self.l2 = tk.Label(row2, text=self.passwd, width=20)
    self.l2.pack(side=tk.LEFT)
    # 第三行

    row3 = tk.Frame(self)
    row3.pack(fill="x")
    tk.Label(row3, text='城市信息：', width=8).pack(side=tk.LEFT)
    self.l3 = tk.Label(row3, text=self.city, width=20, wraplength=80)
    self.l3.pack(side=tk.LEFT)

    row3 = tk.Frame(self)
    row3.pack(fill="x")
    tk.Button(row3, text="设置", command=self.setup_config).pack(side=tk.RIGHT)
  # 设置参数
  def setup_config(self):
    # 接收弹窗的数据
    res = self.ask_userinfo()
    #print(res)
    if res is None: return
    # 更改参数
    self.username, self.passwd, self.city = res
    # 更新界面
    self.l1.config(text=self.username)
    self.l2.config(text=self.passwd)
    self.l3.config(text=self.city)
    filename = self.username + '_' + self.passwd + '.json'
    with open("temp.txt", "w", encoding='utf-8') as f:
        f.write(self.city)
    f.close()
    command = "./convertcity.py"
    os.system(command)
    command = "cp temp.json " + filename
    os.system(command)

  # 弹窗
  def ask_userinfo(self):
    inputDialog = MyDialog()
    self.wait_window(inputDialog) # 这一句很重要！！！
    return inputDialog.userinfo
if __name__ == '__main__':
  app = MyApp()
  app.mainloop()
