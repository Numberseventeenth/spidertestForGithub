import scrapy
from scrapy import Selector
from spidertestForGithub.items import BcyItem

"""
    半次元榜单-绘画榜
"""
class BcySpiderSpider(scrapy.Spider):
    name = 'bcy_spider'
    allowed_domains = ['bcy.net']
    start_urls = ['https://bcy.net/illust/toppost100']

    def parse(self, response):
        sel = Selector(response)
        image_urls = sel.xpath("//img[@class='rank-cos-img']/@src").extract()
        item = BcyItem()
        for image in image_urls:
            item['image_urls'] = image
            yield item
