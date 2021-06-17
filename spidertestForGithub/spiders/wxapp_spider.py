import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from spidertestForGithub.items import WxappItem
"""
    抓取小程序社区（教程）下的文章
"""
class WxappSpiderSpider(CrawlSpider):
    name = 'wxapp_spider'
    allowed_domains = ['wxapp-union.com']
    start_urls = ['https://www.wxapp-union.com/portal.php?mod=list&catid=2&page=1']

    rules = (
        Rule(LinkExtractor(allow=r'.+portal.php?mod=list&catid=2&page=\d'), follow=True),
        Rule(LinkExtractor(allow=r'.+article-.+\.html'),callback='parse_detail',follow=False),
    )

    def parse_detail(self, response):
        url = response.url
        title = response.xpath("//div[@class='cl']/h1/text()").get()
        author = response.xpath('//p[@class="authors"]/a/text()').get()
        datestr = response.xpath('//span[@class="time"]/text()').get()
        seewatch = response.xpath('//div[@class="focus_num cl"]/a/text()').get()
        content = response.xpath('//td[@id="article_content"]//text()').getall()
        reply = response.xpath('//div[@class="comment_tit cl"]/a/strong/text()').get()
        item = WxappItem(
            title=title,
            author=author,
            datestr=datestr,
            seewatch=seewatch,
            content=content,
            reply=reply,
            url=url
        )
        yield item
