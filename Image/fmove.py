# 因为开始时的多线程爬取图片ID每次都不同，所以通过json来移动图片重命名
import json
import os

file1 = open('/home/sunweifeng/Picture/pexels/pexels.json')
file1 = file1.readlines()
mydict = dict()
for line in file1:
    text = json.loads(line)
    mydict[text['url']] = text['id']

file2 = open('/home/sunweifeng/桌面/pexels12000/12000pexels.json')
file2 = file2.readlines()
for line in file2:
    text = json.loads(line)
    old = '/home/sunweifeng/桌面/pexels12000/image12000/' + str(text['id']) + '.jpeg'
    new = '/home/sunweifeng/Picture/pexels/image/' + str(mydict[text['url']]) + '.jpeg'
    os.rename(old, new)
