# -*- coding: utf-8 -*-

class InfoMaker:
    
    count = 1   # 显示序列号
        
    def makeHTML(self, info, fileName, dateList=[]):
    
        def makeEachInfo(dic): 
            f.write('''		<div class="info">
			<p>''' + dic['title'] + '''</p>
            <p class="count">''' + '%d' % self.count + '''</p>
			<a href="''' + dic['url'] + '''" target="_blank">Address</a>
            <p>''' + dic['price'] + '''</p>''')
            
            f.write('''
            <p>''' + dic['time'][:45] + '''</p>
            <p>''' + dic['introduce'] + '''</p>''')  # 描述

            for v in dic['pic']:
                # f.write('''<img src="''' + v + '''">''')  # 可能因为前面禁止重新定向，新的img地址没带http:
                f.write('''<img src="http:''' + v + '''">''')

            f.write('''</div>''')

       
        ## -------------------------------------------------
        
        print ("file name is : " + fileName)
        f = open(fileName, 'w', encoding = 'utf-8')
        f.write('''<!DOCTYPE HTML>
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
<body>''')

        # 写入每一个信息
        print("一共有%d个信息"%len(info))
        for i in range(len(info)):
        
            if len(dateList) > 0:
                # 判断收集的信息是否在设定时间内
                infoTimeStr = info[i]['time']
                if len(infoTimeStr) > 0:
                    isInTime = False
                    for t in dateList:   # 查看每一个有效时间，是否在发布时间
                        if t in infoTimeStr:
                            isInTime = True
                            break
                
                    if isInTime == False:
                        continue

                # 生成信息
                makeEachInfo(info[i])
                self.count += 1
            else:
                # 不需要判断时间
            
                # 生成信息
                makeEachInfo(info[i])
                self.count += 1            
        
        


        f.write('''</body>


</html>''')
        
    def makeXLSX(self):
        pass
        
        
Maker = InfoMaker()