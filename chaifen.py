# -*- coding: utf-8 -*-
import os
import re
from bs4 import BeautifulSoup


class ChaiFen:
    html_soup = "<body>((.|\n)*?)</body>"
    html_end = """</body>
</html>
    """
    html_start = """
    <!DOCTYPE HTML>
<html>
<head>
	<meta charset="utf-8">
	<title>58</title>
	<style>

		.info {
			margin: 10px auto;
			height:auto;
			width:1000px;
			border:gray solid 5px;
			float:left;
		}
		img {
			width: 300px;
			height: 300px;
			float: left;
		}

		.count {
			left:850px;
			position:absolute;
		}

	</style>
</head>
<body>
    """

    def chaifen(self, file_path, lines):
        """
        把一个txt文件拆分成多个文件
        :param file_path: 总文件地址
        :param lines: 每个文件行数,int
        :return:
        """
        with open(file_path, "r", encoding="UTF-8") as f:
            datas = f.readlines()
        totle_line = len(datas)
        filename = os.path.splitext(file_path)[0]
        suffix = os.path.splitext(file_path)[1]
        counts = 1
        while True:
            newfile = filename + "_%03d" % counts + suffix
            with open(newfile, "w") as f:
                endflag = counts * lines if counts * lines < totle_line else totle_line
                for d in datas[(counts - 1) * lines:endflag]:
                    f.write(d)
            if counts * lines > totle_line:
                break
            counts += 1

    def hebing(self, file_path):
        """
        把一个文件夹内的html文件合并成一个html
        :param file_path: 目录
        :return:
        """
        files = []
        path = os.path.dirname(file_path)
        for f in os.listdir(path):
            suffix = os.path.splitext(f)[1]
            if "html" in suffix:
                files.append(os.path.join(path, f))

        with open(os.path.join(path, "all.html"), "w", encoding="utf-8") as f:
            f.write(self.html_start)
            for af in files:
                with open(af, "r", encoding="utf-8") as f1:
                    tmp = f1.read()
                    find = re.findall(self.html_soup, tmp)
                    try:
                        f.write(find[0][0])
                    except :
                        pass

            f.write(self.html_end)

if __name__ == "__main__":
    fpath = "E:/zufang58/xunmei/xunmei.txt"
    cf = ChaiFen()
    cf.chaifen(fpath, 50)
    # cf.hebing(fpath)