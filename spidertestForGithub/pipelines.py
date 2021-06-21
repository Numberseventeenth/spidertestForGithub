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
import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors
from scrapy.pipelines.images import ImagesPipeline

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
'''
    苏宁-图书-分类
'''
# class SuningCategoryPipleline(object):
#     def __init__(self):
#         dbparams = {
#             'host':'127.0.0.1',
#             'port':3306,
#             'user':'root',
#             'password':'12345',
#             'database':'pythondemo',
#             'charset':'utf8'
#         }
#         self.conn = pymysql.connect(**dbparams)
#         self.cursor = self.conn.cursor()
#         self._sql = None
#     def process_item(self,item,spider):
#         self.cursor.execute(self.sql,(item['big_category'],item['sub_category'],item['min_category'],item['url']))
#         self.conn.commit()
#         yield item
#     @property
#     def sql(self):
#         if not self._sql:
#             self._sql = """
#                 insert into suningbookcategory(id,big_category,sub_category,min_category,url)values(null,%s,%s,%s,%s)
#             """
#             return self._sql
#         return self._sql
"""
    简书--文章--mysql同步
"""
class JianshuSpiderPipeline(object):

    def __init__(self):
        dbparams = {
            'host':'127.0.0.1',
            'port':3306,
            'user':'root',
            'password':'12345',
            'database':'pythondemo',
            'charset':'utf8'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None


    def process_item(self, item, spider):
        self.cursor.execute(self._sql,(item['title'],item['content'],item['origin_url'],item['article_id']))
        self.conn.commit()
        yield item
    @property
    def sql(self):
        if not self._sql:
            self._sql = """
                insert into jianshu(id,title,content,origin_url,article_id)
                values(null,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql
"""
    简书--文章--mysql异步
"""
class JianshuTwistedPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '12345',
            'database': 'pythondemo',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql',**dbparams)
        self._sql = None
    print('连接mysql成功')

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
                 insert into jianshu(id,title,content,origin_url,article_id,author,avatar,pub_time,word_count,read_count,like_count,comment_count)
                values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql

    def process_item(self,item,spider):
        defer = self.dbpool.runInteraction(self.insert_item,item)
        defer.addErrback(self.handle_error,item,spider)
    def insert_item(self,cursor,item):
        cursor.execute(self.sql,(item['title'],item['content'],item['origin_url'],item['article_id'],item['author'],item['avatar'],
                                  item['pub_time'],item['word_count'],item['read_count'],item['like_count'],item['comment_count']))
    def handle_error(self,error,item,spider):
        print(error)
"""
    汽车之家--宝马5系高清图片下载
"""
class BmwPipeline:
    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'images')
        if not os.path.exists(self.path):
            os.mkdir(self.path)
    def process_item(self,item,spider):
        catagory = item['catagory']
        urls = item['urls']
        catagory_path = os.path.join(self.path,catagory)
        if not os.path.exists(catagory_path):
            os.makedirs(catagory_path)
        for url in urls:
            image_name = url.split('_')[-1]
            response = requests.get(url,stream=True)
            with open(os.path.join(catagory_path,image_name),'wb')as f:
                for block in response.iter_content(1024):
                    if not block:
                        break
                    f.write(block)
        return item
"""
    汽车之家--宝马5系高清图片下载(内置)
"""
class BmwImagePipline(ImagesPipeline):
    # 这个方法是在发送下载请求之前调用
    # 其实这个方法本身是去发送下载请求的
    def get_media_requests(self, item, info):
        requests_objs = super(BmwImagePipline,self).get_media_requests(item,info)
        for requests_obj in requests_objs:
            requests_obj.item = item
        return requests_objs

    def file_path(self, request, response=None, info=None):
        # 这个方法是图片将要被存储的时候调用，来获取这个图片的路径
        path = super(BmwImagePipline,self).file_path(request,response,info)
        category = request.item.get('category')
        images_store = settings.IMAGES_STORE
        category_path = os.path.join(images_store,category)
        if not os.path.exists(category_path):
            os.mkdir(category_path)
        image_name = path.replace("full/",'')
        image_path = os.path.join(category_path,image_name)
        return image_path
"""
    boss直聘网--工作爬虫
"""
class BossPipeline(object):
    # boss直聘
    def __init__(self):
        self.fp = open('jobs.json','wb')
        self.exporter = JsonLinesItemExporter(self.fp,ensure_ascii=False)
    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item
    def close_spider(self,spider):
        self.fp.close()
"""
    房天下(所有城市的新房和二手房)
"""
class FangPipeline(object):
    def __init__(self):
        self.newhouse_fp = open('newhouse.json','wb')
        self.esfhouse_fp = open('esfhouse.json','wb')
        self.newhouse_exporter = JsonLinesItemExporter(self.newhouse_fp,ensure_ascii=False)
        self.esfhouse_exporter = JsonLinesItemExporter(self.esfhouse_fp,ensure_ascii=False)
    def process_item(self,item,spider):
        self.newhouse_exporter.export_item(item)
        self.esfhouse_exporter.export_item(item)
        return item
    def close_spider(self,spider):
        self.newhouse_fp.close()
        self.esfhouse_fp.close()

