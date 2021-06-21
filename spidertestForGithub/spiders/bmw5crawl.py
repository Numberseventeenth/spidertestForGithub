import scrapy
from spidertestForGithub.items import BmwItem
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import re


class Bmw5Spider(CrawlSpider):
    name = 'bmw5crawl'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/65.html']

    rules = (
        Rule(LinkExtractor(allow='https://car.autohome.com.cn/pic/series/65.+'),callback="parse_page",follow=True),
    )

    def parse_page(self, response):
        category = response.xpath('//div[@class="choise-cont-text"]/text()').get()
        srcs = response.xpath('//div[contains(@class,"uibox-con")]/ul/li//img/@src').getall()
        # srcs = list(map(lambda x:x.replace(re.match(r'.*?(240x180.+)autohomecar',x).group(1),''),srcs))
        # srcs = list(map(lambda x:response.urljoin(x),srcs))
        srcs = list(map(lambda x:response.urljoin(x.replace(re.match(r'.*?(240x180.+)autohomecar',x).group(1),'')), srcs))
        yield BmwItem(category=category,image_urls=srcs)


    def text_parse(self,response):
        uiboxs = response.xpath("//div[@class='uibox']")[1:]
        for uibox in uiboxs:
            category = uibox.xpath(".//div[@class='uibox-title']/a/text()").get()
            urls = uibox.xpath(".//ul/li/a/img/@src").getall()
            # print(category)
            # for url in urls:
            # url = 'http:' + url
            # url = response.urljoin(url)  #另一种写法
            # 终极写法
            urls = list(map(lambda url: response.urljoin(url), urls))
            item = BmwItem(category=category, image_urls=urls)
            yield item
