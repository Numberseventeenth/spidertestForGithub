# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonItemExporter,JsonLinesItemExporter
import json
from spidertestForGithub.settings import MONGO_HOST
from pymongo import MongoClient
import re
from spidertestForGithub import settings
import os
import requests

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

"""
    糗事百科（段子）---- 保存到json文件中
"""
class QiushibaikePipeline:
    def __init__(self):
        self.fp = open('duanzi.json','wb')
        # self.exporter = JsonItemExporter(self.fp,ensure_ascii=False,encoding='utf-8')
        self.exporter = JsonLinesItemExporter(self.fp,ensure_ascii=False,encoding='utf-8')
        self.exporter.start_exporting()
    def open_spider(self,spider):
        print('爬虫开始了')
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.fp.close()
        print('爬虫结束了')
"""
    抓取小程序社区（教程）下的文章----保存到json文件中
"""
class WxappPipeline:
    def __init__(self):
        self.fp = open("wxapp.json",'wb')
        self.exporter = JsonLinesItemExporter(self.fp,ensure_ascii=False,encoding='utf-8')
    def process_item(self,item,spider):
        self.exporter.export_item(item)
        yield item
    def close_spider(self,spider):
        self.fp.close()
"""
    阳光热线问政平台（督办回复）-- 内容页
"""
class YangGuangPipeline:
    def open_spider(self, spider):
        self.client = MongoClient(host='127.0.0.1',port=27017)
        self.collection =self.client['ygrx_spider']['dbhf_article']
    def process_item(self, item, spider):
        # spider.settings.get('MONGO_HOST')
        item["reply"] = self.process_content(item["reply"])
        item["title_detail"] = self.process_content(item["title_detail"])
        self.collection.insert(dict(item))
        return item
    def process_content(self, content):
        content = [re.sub(r"\xa0|\s", "", i) for i in content]
        content = [i for i in content if len(i) > 0]  # 去除列表中的空字符串
        return "".join(content)
"""
    半次元榜单-绘画榜-保存图片
"""
class ImageDownPipeline(object):
    def process_item(self,item,spider):
        if 'image_urls' in item:
            dir_path = '%s/%s' % (settings.IMAGES_STORE,spider.name)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            urly = item['image_urls']
            filename = urly[0:-6].rfind('/')
            name = urly[filename + 1:-6]
            file_name_path = dir_path + '/' + name + '.jpg'
            with open(file_name_path,'wb')as handle:
                response = requests.get(urly,stream=True)
                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)
        return item

