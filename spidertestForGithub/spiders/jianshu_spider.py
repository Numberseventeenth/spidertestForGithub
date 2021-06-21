import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from spidertestForGithub.items import ArticleItem
import re

class JianshuSpider(CrawlSpider):
    name = 'jianshu_spider'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        title = response.xpath("//h1[@class='_1RuRku']/text()").get()
        content = response.xpath("//article[@class='_2rhmJa']").get()
        url = response.url
        article_id = url.split('/')[-1]
        # ajax
        author = response.xpath("//span[@class='FxYr8x']/a/text()").get()
        avatar = response.xpath("//img[@class='_13D2Eh']/@src").get()
        pub_time = response.xpath("//div[@class='s-dsoj']/time/text()").get()
        count = response.xpath("//div[@class='s-dsoj']/span/text()").getall()
        word_count_str = count[0]
        word_match_re = re.match('.*?(\d+)',word_count_str)
        if word_match_re:
            word_count = int(word_match_re.group(1))
        else:
            word_count = 0
        read_count_str = count[1]
        read_match_re = re.match('.*?(\d+)',read_count_str.replace(',',''))
        if read_match_re:
            read_count = int(read_match_re.group(1))
        else:
            read_count = 0
        like_count_str = response.xpath("//span[@class='_1LOh_5']/text()").get()
        like_match_re = re.match('.*?(\d+).*',like_count_str)
        if like_match_re:
            like_count = int(like_match_re.group(1))
        else:
            like_count = 0
        comment_count = response.xpath("//span[@class='_2R7vBo']/text()").get()
        item = ArticleItem(
            title=title,
            content=content,
            article_id=article_id,
            origin_url=response.url,
            author=author,
            avatar=avatar,
            pub_time=pub_time,
            word_count=word_count,
            read_count=read_count,
            like_count=like_count,
            comment_count=comment_count
        )
        yield item



