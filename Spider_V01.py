# -*- coding: utf-8 -*-
import os
import traceback
from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog, threading, time
# 功能模块
from logic import ai
from InfoMaker import Maker
import Data
from UrlData import UrlDB
from chaifen import ChaiFen


#

class Spider(Tk):
    mainURL = 'http://sh.58.com/chuzu/'

    def __init__(self):  # 初始话创建显示界面
        Tk.__init__(self, baseName=None, className='58同城租房信息爬取')
        self.geometry("350x200")
        self.resizable(width=False, height=False)
        # 上框架
        self.top_frm = Frame(self, relief=None, borderwidth=2, width=340, height=50)  # relief=GROOVE,可以显示边框
        self.top_frm.pack(fill=BOTH, padx=10, pady=8, expand=0)
        # 输入框和选择文件按钮
        self.fileTXT = StringVar(self.top_frm)
        # self.fileTXT.set("Choose a file.")
        self.chooseTextEntry = Entry(self.top_frm, width=33, textvariable=self.fileTXT)
        self.chooseTextEntry.place(relx=.01, rely=.1)
        self.fileButton = Button(self.top_frm, text=u"选择文件", width=10, command=self.getPath)
        self.fileButton.place(relx=.75, rely=.09)
        # 下框架
        self.bottom_frm = Frame(self, relief=None, borderwidth=2, width=340, height=130)
        self.bottom_frm.pack(fill=BOTH, padx=10, pady=8, expand=0)

        # 输入价格
        self.enterMinPrice = StringVar(self.bottom_frm)
        self.enterMaxPrice = StringVar(self.bottom_frm)
        priceLabel = Label(self.bottom_frm, text="最小价格").place(relx=.55, rely=.01)
        self.enterMinPriceEntry = Entry(self.bottom_frm, width=10, textvariable=self.enterMinPrice)
        self.enterMinPriceEntry.place(relx=.72, rely=.01)
        priceLabel = Label(self.bottom_frm, text="最大价格").place(relx=.55, rely=.25)
        self.enterMaxPriceEntry = Entry(self.bottom_frm, width=10, textvariable=self.enterMaxPrice)
        self.enterMaxPriceEntry.place(relx=.72, rely=.25)

        # 最大页数
        self.pageTXT = StringVar(self.bottom_frm)
        # self.pageTXT.set("30")
        self.pageLabel = Label(self.bottom_frm, text="最大页数").place(relx=.01, rely=.25)
        self.pageEntry = Entry(self.bottom_frm, width=10, textvariable=self.pageTXT)
        self.pageEntry.place(relx=.2, rely=.25)

        # 起始日期
        self.startDateMonTXT = StringVar(self.bottom_frm)
        # self.startDateMonTXT.set("01")
        self.dateLabel1 = Label(self.bottom_frm, text="开始日期").place(relx=.01, rely=.01)
        self.startDateMonCombobox = Combobox(self.bottom_frm, textvariable=self.startDateMonTXT, width=2,
                                             state="readonly")
        self.startDateMonCombobox["values"] = ("01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12")
        self.startDateMonCombobox.place(relx=.2, rely=.01)
        self.startDateDayTXT = StringVar(self.bottom_frm)
        # self.startDateDayTXT.set("01")
        self.startDateDayCombobox = Combobox(self.bottom_frm, textvariable=self.startDateDayTXT, width=2,
                                             state="readonly")
        self.startDateDayCombobox["values"] = (
            "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", \
            "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31")
        self.startDateDayCombobox.place(relx=.32, rely=.01)

        # 地址选择
        self.locationTXT = StringVar(self.bottom_frm)
        self.locationLabel1 = Label(self.bottom_frm, text="位置选择").place(relx=.55, rely=.5)
        self.locationCombobox = Combobox(self.bottom_frm, textvariable=self.locationTXT, width=7, state="readonly")
        # 
        self.locationCombobox["values"] = list(Data.CityToUrl.keys())
        # self.locationCombobox["values"] = ("上海","广州","深圳")
        self.locationCombobox.place(relx=.72, rely=.5)

        # 个人房源
        self.fangCheck = IntVar(self.bottom_frm)
        self.Checkbutton = Checkbutton(self.bottom_frm, text="个人房源", variable=self.fangCheck, onvalue=1, offvalue=0,
                                       width=7)
        self.Checkbutton.place(relx=.01, rely=.5)
        # 只看新增
        self.NewCheck = IntVar(self.bottom_frm)
        self.NewCheckButton = Checkbutton(self.bottom_frm, text="只看新增", variable=self.NewCheck, onvalue=1, offvalue=0,
                                          width=7)
        self.NewCheckButton.place(relx=.3, rely=.5)
        # 开始按钮
        self.startButton = Button(self.bottom_frm, text="开始", width=10, command=self.run)
        self.startButton.place(relx=.38, rely=.75)
        # 获取默认设置
        self.getDefaultSetting()

    def saveDefaultSetting(self):
        n = open("Default.py", 'w', encoding="utf-8")
        n.write("# -*- coding: utf-8 -*-" + '\n')
        n.write("# The default settings is make at :" + time.strftime('%Y-%m-%d %H:%M') + '\n')
        dic = {}
        dic['person'] = str(self.fangCheck.get())
        dic['newAdd'] = str(self.NewCheck.get())
        dic['startMon'] = self.startDateMonTXT.get()
        dic['startDay'] = self.startDateDayTXT.get()
        dic['minPrice'] = self.enterMinPrice.get()
        dic['maxPrice'] = self.enterMaxPrice.get()
        dic['stopPage'] = self.pageTXT.get()
        dic['fileDir'] = self.fileTXT.get()
        dic['location'] = self.locationTXT.get()
        for key in dic.keys():
            if dic[key] != None:
                n.write(key + "=" + "'" + dic[key] + "'" + "\n")
            else:
                n.write(key + "=None" + "\n")

        del dic
        n.close()

    def getDefaultSetting(self):
        try:
            import Default
            self.fangCheck.set(int(Default.person))  # 个人房源
            self.NewCheck.set(int(Default.newAdd))  # 只看新增
            self.startDateMonTXT.set(Default.startMon)  # 起始月
            self.startDateDayTXT.set(Default.startDay)  # 起始天
            self.enterMinPrice.set(Default.minPrice)  # 输入价格
            self.enterMaxPrice.set(Default.maxPrice)
            self.pageTXT.set(Default.stopPage)  # 最大页数
            self.fileTXT.set(Default.fileDir)  # 文件地址
            self.locationTXT.set(Default.location)  # 地理位置

            self.outName = (Default.fileDir).replace(':', '').replace('/', '_') + '.html'
        except:
            print("读取默认配置失败")

    def getPath(self):
        path = tkinter.filedialog.askopenfilename(parent=self, initialdir='/', title="选择文件")
        self.fileTXT.set(path)

        self.BackUpPath = path.replace('txt', 'py')  # 备份文件的path

        self.outName = path.replace(':', '').replace('/', '_') + '.html'

    def getSettings(self):
        # 个人房源
        if self.fangCheck.get() == 1:
            source = r'0/'
        else:
            source = ''

        # 只看新增
        if self.NewCheck.get() == 1:
            onlyNewAdd = True
        else:
            onlyNewAdd = False

        # 发布时间        
        self.setDate = ['前']
        startMon = int(self.startDateMonTXT.get())
        startDay = int(self.startDateDayTXT.get())
        endMon = int(time.strftime('%m'))
        endDay = int(time.strftime('%d'))

        if startMon == endMon:
            while startDay <= endDay:
                self.setDate.append('%02d' % startMon + '-' + '%02d' % startDay)
                startDay += 1
        else:
            while startDay < 32:
                self.setDate.append('%02d' % startMon + '-' + '%02d' % startDay)
                startDay += 1

            while endDay > 1:
                self.setDate.append('%02d' % endMon + '-' + '%02d' % endDay)
                endDay -= 1

        # 获取价格
        price = self.enterMinPrice.get() + '_' + self.enterMaxPrice.get()

        # 停止页数
        self.stopPage = int(self.pageTXT.get())

        # 文件地址
        # self.data = []
        # f = open(self.fileTXT.get(), 'r', encoding='utf-8')
        # self.data = f.readlines()
        # f.close()

        # 获取备份文件地址
        self.BackUpPath = (self.fileTXT.get()).replace('txt', 'py')

        # 获取地理位置
        self.mainURL = Data.CityToUrl[self.locationTXT.get()]

        return source, price, onlyNewAdd

    def get_file_from_dir(self):
        """从文件夹读取"""
        file_path = os.path.dirname(self.fileTXT.get())
        file_names = []
        for fname in os.listdir(file_path):
            af = os.path.join(file_path, fname)
            if os.path.isfile(af) and "txt" in os.path.splitext(af)[1]:
                file_names.append(os.path.join(file_path, fname))
        return file_names

    def run(self):
        self.saveDefaultSetting()  # 保存设置信息

        t = threading.Thread(target=self.spiderGOGOGO, args=())
        t.start()
        # t.join()

    def spiderGOGOGO(self):
        source, price, onlyNewAdd = self.getSettings()
        file_names = self.get_file_from_dir()
        for fn in file_names:
            try:
                # 打开数据库
                urldb = UrlDB()
                with open(fn, "r") as f1:
                    afilenames = f1.readlines()
                for fileName in afilenames:
                    if len(fileName) < 2:
                        continue
                    print("正在查找小区：" + fileName)
                    url = self.mainURL + source + '?minprice=' + price + '&key=' + fileName + '&sourcetype=5'  # 搜索的起始网址
                    ai.OnTheWay(url, self.stopPage, onlyNewAdd, self.BackUpPath, fileName, price, urldb)
            except Exception as e:
                print(traceback.format_exc())
            finally:
                # 生成html
                Maker.makeHTML(ai.infoList, fn + ".html", self.setDate)  # 存有dic的list，输出文件的name，有效日期list

                # 关闭数据库
                urldb.disconnect_database()

                #
                ai.infoList.clear()

        cf = ChaiFen()
        cf.hebing(file_names[0])


if __name__ == "__main__":
    s = Spider()
    s.mainloop()
