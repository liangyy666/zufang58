# -*- coding: utf-8 -*-
from datetime import datetime
import sqlite3
import traceback
import os
import uuid


class UrlDB:
    db_name = 'URLDB.db'
    conn = None

    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), self.db_name)  # 当前文件目录下的db文件地址
        if not os.path.isfile(path):
            self.connect_database()
            self.conn.cursor().execute(
                '''CREATE TABLE urlbackup(ID INT PRIMARY KEY  NOT NULL, URL CHAR(50), RTime date);''')
            self.conn.commit()
            self.conn.close()

        self.connect_database()

    def connect_database(self):
        self.conn = sqlite3.connect(self.db_name)

    def disconnect_database(self):
        try:
            self.conn.commit()
            self.conn.close()
        except Exception as e:
            print(e)
            print(traceback.format_exc())

    def check_url(self, in_url, check_time=None):
        '''
        查看某个URL是否存在db里面
        :return: True or False
        '''
        try:
            result = self.conn.cursor().execute("SELECT * FROM urlbackup WHERE URL = '%s';" % in_url)
            self.conn.commit()
            flag = result.fetchall()
            print(flag)
            if not bool(flag):  # 如果db里面没有改地址，则存进去
                self.save_url(in_url)
            else:   # 已有则判断是否需要计算时间
                tstr = flag[0][2]
                dtme = datetime.strptime(tstr[:19], "%Y-%m-%d %H:%M:%S")
                tmp = datetime.now() - dtme

            return bool(flag)
        except Exception as e:
            print(e)
            print(traceback.format_exc())

    def save_url(self, in_url):
        '''
        把url存进db里面
        :return:
        '''
        try:
            id = uuid.uuid1()
            self.conn.cursor().execute(
                "INSERT INTO urlbackup (ID,URL, RTime)VALUES ('%s', '%s', '%s')" % (id, in_url, datetime.now()))
            self.conn.commit()
        except Exception as e:
            print(e)
            print(traceback.format_exc())


if __name__ == "__main__":
    print(datetime.now())
    URL = "www.baidu.co"
    urldb = UrlDB()
    print(urldb.check_url(URL))
