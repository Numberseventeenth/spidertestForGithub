import scrapy
from spidertestForGithub.items import BmwItem

"""
    汽车之家--宝马5系高清图片下载
"""
class Bmw5Spider(scrapy.Spider):
    name = 'bmw5'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/65.html']

    def parse(self, response):
        uiboxs = response.xpath("//div[@class='uibox']")[1:]
        for uibox in uiboxs:
            category = uibox.xpath(".//div[@class='uibox-title']/a/text()").get()
            urls = uibox.xpath(".//ul/li/a/img/@src").getall()
            # print(category)
            # for url in urls:
                # url = 'http:' + url
                # url = response.urljoin(url)  #另一种写法
                # 终极写法
            urls = list(map(lambda url:response.urljoin(url),urls))
            item = BmwItem(category=category,image_urls=urls)
            yield item
