# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class ImagePipeline(object):
#     def process_item(self, item, spider):
#         return item

# import codecs
import json
from image import settings
import os
import requests
import traceback

# 写入本地文件
class pexelsPipeline(object):
    count_n = 0  # id
    def __init__(self):
        dir_path = settings.FILE_STORE
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        self.file = open('%s/pexels.json' % dir_path, 'a', encoding='utf-8')
        #self.check = open('%s/pexels.log' % dir_path, 'w', encoding='utf-8')
        #self.file = codecs.open('/home/sunweifeng/Desktop/pexels.json', mode='wb', encoding='utf-8')

    def process_item(self, item, spider):
        # 创建目录
        dir_path = os.path.join(settings.FILE_STORE, 'image')
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        # 图片路径
        self.count_n += 1
        item['id'] = self.count_n
        item['images_local'] = os.path.join(dir_path, (str(item['id']) + '.jpeg'))
        # 写入json
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line)
        ## 下载图片
      #  image_file = item['images_local']
      #  with open(image_file, 'wb') as handle:
      #      status = 0
        #    # 图片链接失败重连
      #      while status != 200:
      #          try:
        #            # 忽略SSL, timeout默认100秒
      #              response = requests.get(item['image_url'], verify=False, timeout=100.0)
      #              status = response.status_code
        #            # 保存
      #              for block in response.iter_content(100000000):
      #                  if not block:
      #                      self.check.write(str(status) + '-' + str(item['id']) + '\n')
      #                      break
      #                  handle.write(block)
      #          except:
      #              traceback.print_exc(self.check)
      #              status = 0
      #          finally:
        #            # 保存日志
      #              self.check.write(str(status) + ':' + str(item['id']) + '\n')
        return item
