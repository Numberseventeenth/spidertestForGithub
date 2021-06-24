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
    简书网站--文章
"""
class ArticleItem(scrapy.Item):
    # 简书网站文章
    title = scrapy.Field()
    content = scrapy.Field()
    article_id = scrapy.Field()
    origin_url = scrapy.Field()
    author = scrapy.Field()
    # 头像
    avatar = scrapy.Field()
    pub_time = scrapy.Field()
    word_count = scrapy.Field()
    read_count = scrapy.Field()
    like_count = scrapy.Field()
    comment_count = scrapy.Field()
"""
    苏宁-图书-分类
"""
class suning_category(scrapy.Item):
    big_category = scrapy.Field()
    sub_category = scrapy.Field()
    min_category = scrapy.Field()
    url = scrapy.Field()
"""
    汽车之家--宝马5系高清图片下载
"""
class BmwItem(scrapy.Item):
    category = scrapy.Field()
    image_urls = scrapy.Field()   # 固定名称
    images = scrapy.Field()       # 固定名称
"""
    boss直聘网--工作爬虫
"""
class BossItem(scrapy.Item):
    title = scrapy.Field()
    salary = scrapy.Field()
    city = scrapy.Field()
    work_years = scrapy.Field()
    education = scrapy.Field()
    company = scrapy.Field()
"""
    房天下(所有城市的新房)
"""
class NewHouseItem(scrapy.Item):
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 小区的名字
    name = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 几居，这是个列表
    rooms = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 行政区
    district = scrapy.Field()
    # 是否在售
    sale = scrapy.Field()
    # 房天下详情页的url
    origin_url = scrapy.Field()
"""
    房天下(所有城市的二手房)
"""
class ESFHouseItem(scrapy.Item):
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 小区的名字
    name = scrapy.Field()
    # 几室几厅
    rooms = scrapy.Field()
    # 层
    floor = scrapy.Field()
    # 朝向
    toward = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 年代
    year = scrapy.Field()
    # 总价
    price = scrapy.Field()
    # 单价
    unit = scrapy.Field()
    # 房天下详情页的url
    origin_url = scrapy.Field()
"""
    百度贴吧----帖子抓取
"""
class TiebaItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    author_name = scrapy.Field()
    content_str = scrapy.Field()
    content_image_urls = scrapy.Field()







