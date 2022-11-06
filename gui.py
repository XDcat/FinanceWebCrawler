# 测试 Grid 布局管理器的基本用法，使用面向对象的方式
import time
import tkinter as tk
from tkinter import *
from tkinter import messagebox

from main import *


def is_valid_date(string):
    """
    判断字符串是否为一个有效的日期字符串
    :param string: 字符串
    """
    # 日期样式(可扩展)
    data_type = "%Y-%m-%d"
    try:
        time.strptime(string, data_type)
        return True
    except:
        return False


def et1foucus(event):
    et1.delete(0, 'end')


def et2foucus(event):
    et2.delete(0, 'end')


def update_db(event):
    latest_date = et1.get()
    if not is_valid_date(latest_date):
        tk.messagebox.showerror(title="消息提示", message="日期格式有误")
    else:
        tk.messagebox.showinfo(title="消息提示", message=f"爬取并翻译{latest_date}以后的文章，是否确定？")
        update_database(latest_date)
        tk.messagebox.showinfo(title="消息提示", message="完成")


def deal_articles(event):
    info = et2.get()
    start, end = info.split(" ")
    if not is_valid_date(start) or not is_valid_date(end):
        tk.messagebox.showerror(title="消息提示", message="日期格式有误")
    else:
        tk.messagebox.showinfo(title="消息提示", message=f"将{start}和{end}期间的文章转义为word文档，是否确定？")
        get_articles(start_from=start, end_at=end)
        tk.messagebox.showinfo(title="消息提示", message="完成")


def deal_last_month(event):
    tk.messagebox.showinfo(title="消息提示", message="获取上个月的金融文档，是否确定？")
    get_last_month_articles()
    tk.messagebox.showinfo(title="消息提示", message="完成")


if __name__ == '__main__':
    root_window = tk.Tk()
    root_window.title('金融爬虫网页文档翻译')
    # 设置窗口大小:宽x高,注,此处不能为 "*",必须使用 "x"
    root_window.geometry('500x200')
    # 设置主窗口的背景颜色,颜色值可以是英文单词，或者颜色值的16进制数,除此之外还可以使用Tk内置的颜色常量
    root_window["background"] = "#BBCCFF"
    # 添加文本内,设置字体的前景色和背景色，和字体类型、大小
    text = tk.Label(root_window, text="金融爬虫", bg="#BBCCFF", fg="black", font=('Song', 20))
    # 将文本内容放置在主窗口内
    # text.pack()

    b1 = Button(root_window, text="打印上个月的金融文献")
    b1.grid(row=0, column=0, sticky=EW)
    date = b1.bind('<ButtonPress-1>', deal_last_month)
    # 可以挑一个窗口，请求输入最晚日期
    et1 = Entry(root_window)
    et1.insert(0, '指定最晚时间，格式为YY-MM-DD')
    et1.grid(row=1, column=1, sticky=EW)
    et1.bind('<FocusIn>', et1foucus)

    b2 = Button(root_window, text="更新数据库")
    b2.bind('<ButtonPress-1>', update_db)
    b2.grid(row=1, column=0, sticky=EW)
    et2 = Entry(root_window, width=300)
    et2.insert(0, '可以指定日期区间，格式为YY-MM-DD YY-MM-DD')
    et2.grid(row=2, column=1, sticky=EW)
    et2.bind('<FocusIn>', et2foucus)
    b3 = Button(root_window, text="生成报告")
    b3.grid(row=2, column=0, sticky=EW)
    b3.bind('<ButtonPress-1>', deal_articles)

    # 添加按钮，以及按钮的文本，并通过command 参数设置关闭窗口的功能
    button = tk.Button(root_window, text="退出", command=root_window.quit)
    # 进入主循环，显示主窗口
    root_window.mainloop()
