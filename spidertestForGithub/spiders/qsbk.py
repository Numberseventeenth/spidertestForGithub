import scrapy
from spidertestForGithub.items import QiushibaikeItem

"""
    爬取糗事百科的段子
"""
class QsbkSpider(scrapy.Spider):
    name = 'qsbk'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/page/1']
    base_domain = 'https://www.qiushibaike.com'

    def parse(self, response):
        content_lists = response.xpath("//div[@class='col1 old-style-col1']/div")
        for content_list in content_lists:
            author = content_list.xpath(".//h2/text()").get().strip()
            # 转换成字符串
            content = content_list.xpath(".//div[@class='content']//text()").getall()
            content = ''.join(content)
            item = QiushibaikeItem(author=author, content=content)
            # duazi = {
            #     'author':author,
            #     'content':content
            # }
            yield item
        next_url = response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()
        if not next_url:
            return
        else:
            yield scrapy.Request(self.base_domain + next_url, callback=self.parse)
