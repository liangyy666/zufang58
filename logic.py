# -*- coding: utf-8 -*-
import traceback
from bs4 import BeautifulSoup
import requests, time, webbrowser
from keywords import keywords
from UrlData import UrlDB

'''
接受搜索的初始url
搜索每页的地址
自动下一页直到没有下一页
根据上面所得地址爬取详细信息
'''


class Logic:
    NumOfInfo = 0  # 每个关键字信息总和
    NumOfPage = 0  # 每个关键字搜索选取的页数
    AllInfo = 0  # 所有信息总和
    urlList = set()  # 存放所有的信息的地址
    infoList = []  # 存放所有具体信息，里面的元素为字典

    # oldURL = set()  # url备份，用来显示新增的信息
    OnlyNewFlag = False
    myHeaders = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'userid360_xml=15C5160DA670768F9BE059C7D2A5C409; time_create=1535424803214; f=n; commontopbar_new_city_info=4%7C%E6%B7%B1%E5%9C%B3%7Csz; userid360_xml=15C5160DA670768F9BE059C7D2A5C409; time_create=1536200285125; f=n; commontopbar_new_city_info=4%7C%E6%B7%B1%E5%9C%B3%7Csz; commontopbar_myfeet_tooltip=end; id58=c5/njVtUi4tOFnR0CpQCAg==; 58tj_uuid=eb1997db-ebce-4976-a5f4-bee1290833b6; als=0; wmda_uuid=5d001a69ca06b2c6c23db67476242dde; wmda_new_uuid=1; wmda_visited_projects=%3B2385390625025; xxzl_deviceid=WRHFaw0p87dhEF9V0bQUQ%2BXizifktSY0rMgKADJoxV6p%2B4Ho2OnuDs2NbyzzBPS1; myfeet_tooltip=end; ppStore_fingerprint=D2D48870B935132C3C4E1A6DF3CEF1F7C73BBC17D9218944%EF%BC%BF1534169734699; 58home=sz; f=n; commontopbar_new_city_info=4%7C%E6%B7%B1%E5%9C%B3%7Csz; city=sz; new_uv=66; utm_source=; spm=; init_refer=; commontopbar_ipcity=sz%7C%E6%B7%B1%E5%9C%B3%7C0; wmda_session_id_2385390625025=1534253324769-f10bf20d-2f62-3ce2; new_session=0; xzfzqtoken=drlUR404UMCMTbHkfG8DzyJgob5WRP3%2BRnUeQWTvArOhi%2B91iWJmaDF%2B3yYdOPemin35brBb%2F%2FeSODvMgkQULA%3D%3D',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }

    def OnTheWay(self, startURL, stopPage, OnlyNew, BackFile, fileName, setPrice, urldb):  # 程序入口
        # 数据初始化
        self.webURL = startURL[7:startURL.find('com') + 3]  # 去掉http://
        self.OnlyNewFlag = OnlyNew
        self.NumOfInfo = 0
        self.NumOfPage = 0
        totalInfo = 0
        self.SearchName = fileName
        self.setPrice = setPrice.split('_')  # 分割成一个list，最小和最大两个数字
        self.urldb = urldb
        # self.infoList = []
        # ------------
        # 尝试打开备份文件，如果问价你不存在则跳过
        # try:
        #     f = open(BackFile, 'r')
        #     data = f.readlines()
        #     f.close()
        #     for u in data:
        #         if len(u) < 10:
        #             continue
        #         self.oldURL.add(u)
        # except Exception as e:
        #     print("打开备份文件失败！！！！！！！！！！！！！！！")
        #     print(traceback.format_exc())

        # 从起始地址获取页面
        self.NextPage = startURL

        # 获取所有信息的网址，存放在 self.urlList
        tryTimes = 0
        while True:
            self.NumOfPage += 1
            print("正在获取第%02d页" % (self.NumOfPage))

            # 尝试访问网页，尝试访问10次
            try:
                # tmp = requests.get(self.NextPage, timeout=60, headers=self.myHeaders, allow_redirects=False)
                print("URL: " + self.NextPage)
                tmp = requests.get(self.NextPage, timeout=60, headers=self.myHeaders)
            except:
                tryTimes += 1
                print("Get web faile, retry later. Times : %d" % tryTimes)
                if tryTimes == 10:
                    break
                continue

            # 检查该网页是否是需要输入验证码
            if self.CheckYanZhengMa(tmp, self.NextPage):
                try:
                    tmp = requests.get(self.NextPage, timeout=60, headers=self.myHeaders)
                except Exception as e:
                    traceback.print_exc()
                    break

            # 先预设下一页网址为空
            self.NextPage = 'None'

            # 从总的页面获取每个信息的网址
            self.GetUrlFromSearch(tmp.text)
            time.sleep(1)
            if self.NextPage == 'None':
                print("next page is null")
                break
            if stopPage <= self.NumOfPage:
                self.NumOfPage = 0
                print("stop number page")
                break

        # 从每个信息的地址爬取具体内容,存放在 self.infoList
        totalInfo = len(self.urlList) - totalInfo
        for url in self.urlList:
            #   跳过已存在备份文件中的地址
            if self.OnlyNewFlag and self.urldb.check_url(url):
                print("跳过一个地址")
                continue
            #

            self.NumOfInfo += 1
            self.AllInfo += 1
            print("正在获取第%04d个信息，本小区共%04d个信息，目前爬取了%04d个信息。" % (self.NumOfInfo, totalInfo, self.AllInfo))
            self.GetInfoFromText(url)
            time.sleep(2)

        # 把新获取的地址存进备份文件
        # for v in self.urlList:
        #     self.oldURL.add(v)

        # 备份url
        # self.MakeUrlBackUp(BackFile)
        self.urlList.clear()

    def GetInfoFromText(self, url):  # 获取：标题，网址，时间，价格，图片，描述
        try:
            tmp = requests.get(url, timeout=60, headers=self.myHeaders)
        except Exception as e:
            traceback.print_exc()
            tmp = ""
        if self.CheckYanZhengMa(tmp, url):
            try:
                time.sleep(5)
                tmp = requests.get(url, timeout=60, headers=self.myHeaders)
            except Exception as e:
                traceback.print_exc()
                return

        # self.NumOfInfo += 1 # 爬取的信息数加1
        tempsoup = BeautifulSoup(tmp.text, 'html.parser')
        dic = {}
        # 图片地址
        picList = []
        try:
            pic = tempsoup.find('ul', class_="house-pic-list").find_all('img')
        except:
            pic = []

        if len(pic) > 0:
            for v in pic:
                picList.append(v['lazy_src'])
            dic['pic'] = picList
        else:
            dic['pic'] = []
        # 标题
        try:
            title = tempsoup.find('title').text
            dic['title'] = title
        except:
            dic['title'] = 'No title...'
        # 时间
        try:
            dataTime = tempsoup.find_all('p', class_="house-update-info")[0].text
            dic['time'] = dataTime
        except:
            dic['time'] = 'no time'
        # print dic['time'].encode("utf-8")[:45]
        # 价格 
        try:
            price = tempsoup.select(".f36")[0].text  # CSS选择器，通过类名选择
            dic['price'] = price
        except:
            dic['price'] = 'no price'
        # 描述
        try:
            introduce = tempsoup.find('div', class_="house-word-introduce").text
            dic['introduce'] = introduce
        except:
            dic['introduce'] = 'no introduce'
        # 网址
        dic['url'] = url

        # 对描述中含有关键字的信息进行过滤
        haveKeyWords = False
        for v in keywords:
            if v in dic['introduce']:
                print("信息含有过滤的关键字，舍弃该信息")
                haveKeyWords = True
                break
            if v in dic['title']:
                print("标题含有过滤的关键字，舍弃该信息")
                haveKeyWords = True
                break
        if haveKeyWords == False:
            self.infoList.append(dic)

    # 从总的页面获取每个信息的网址
    def GetUrlFromSearch(self, txt):
        tmp = BeautifulSoup(txt, 'html.parser')
        ##-----------
        url = set()
        ur = tmp.select('.listUl')  # 类搜索，出租信息在listUL
        if len(ur) > 0:
            li = ur[0].select('li[logr]')
            for div in li:  # 对于每一个出租信息
                jjr = div.select('.jjr')    # 处理经纪人发布的消息
                if len(jjr)>0:
                    print("扔掉经纪人发布的信息")
                    continue
                money = div.select('.money')
                if len(money) > 0:
                    if len(money[0].select('b')) > 0:
                        getMoney = money[0].select('b')[0].text
                        try:
                            int(getMoney)
                        except:
                            print(getMoney, " 跳过")
                            continue
                        if int(getMoney) >= int(self.setPrice[0]) and int(getMoney) <= int(self.setPrice[1]):
                            print(int(getMoney))
                            trueURL = div.select('a[href]')[0]['href']
                            # print("head:" + self.webURL)
                            # print("body:" + trueURL)
                            if self.webURL in trueURL:  # 此处url开头带有两个斜杠，补上http:
                                url.add("http:" + trueURL)
                            else:
                                print("扔掉了一条广告。")
                        else:
                            print("钱不对1：" + getMoney)
                else:
                    print("钱不对2：" + money)

            for value in url:
                self.urlList.add(value)

        # 获取下一页网址
        try:
            self.NextPage = tmp.find('a', class_='next')['href']  # 搜索结果的下一页
        except:
            self.NextPage = 'None'

    def MakeUrlBackUp(self, backFile):  # 生成写有地址的py文件

        f = open(backFile, 'w')
        for url in self.oldURL:
            f.write(url)
            f.write('\n')
        f.close()

    def CheckYanZhengMa(self, web, url):  # 从requests.get获取的页面，检测是否为验证码页面
        '''
        检测是否为验证码页面，如果是验证码页面，则返回一个0，引发除0错误
        '''
        yanZhengMa = "请输入验证码"
        tempsoup = BeautifulSoup(web.text, 'html.parser')
        title = tempsoup.select("title")[0].text
        if yanZhengMa == title:
            print("title is : " + title)
            print("url is: " + url)
            webbrowser.open(url)
            wait = input("Input the code in the browser, then press enter key to continue.")
            return True
        return False


ai = Logic()
