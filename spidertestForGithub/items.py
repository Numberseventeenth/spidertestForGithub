# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

"""
    糗事百科(段子)item
"""
class QiushibaikeItem(scrapy.Item):
    # define the fields for your item here like:
    author = scrapy.Field()
    content = scrapy.Field()
"""
    小程序社区（教程）item
"""
class WxappItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    datestr = scrapy.Field()
    seewatch = scrapy.Field()
    reply = scrapy.Field()
    url = scrapy.Field()  # 文章url
    content = scrapy.Field()
"""
    阳光热线问政平台（督办回复）-- 内容页
"""
class YgrxArticleItem(scrapy.Item):
    # 标题
    title = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 日期
    data = scrapy.Field()
    # 状态
    status = scrapy.Field()
    # 编号
    num = scrapy.Field()
    # 标题详情
    title_detail = scrapy.Field()
    # 问政部门
    question_department = scrapy.Field()
    # 回复
    reply = scrapy.Field()
"""
    半次元榜单-绘画榜
"""
class BcyItem(scrapy.Item):
    image_urls = scrapy.Field()
"""
    苏宁-图书-大分类
"""
class big_category(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
"""
    苏宁-图书-中分类
"""
class big_category(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()

