import scrapy
from spidertestForGithub.items import TiebaItem

class TiebaSpiderSpider(scrapy.Spider):
    name = 'tieba_spider'
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['https://tieba.baidu.com/f?kw=程潇']

    def parse(self, response):
        lis = response.xpath("//ul[@id='thread_top_list']//li")
        for li in lis:
            item = TiebaItem()
            # 标题
            title = li.xpath(".//div[contains(@class,'threadlist_title')]/a/text()").get()
            author_name = li.xpath(".//a[contains(@class,'frs-author-name')]/text()").get()
            # 链接
            url = li.xpath(".//div[contains(@class,'threadlist_title')]/a/@href").get()
            item['url'] = response.urljoin(url)
            item['title'] = title
            item['author_name'] = author_name
            yield scrapy.Request(url=item['url'],callback=self.detail_parse,meta={'item':item})
        # 下一页
        next_url = response.xpath("//a[@class='next pagination-item ']/@href").get()
        if next_url is not None:
            yield scrapy.Request(url=response.urljoin(next_url),callback=self.parse)
    # 处理每个帖子详细信息
    def detail_parse(self,response):
        item = response.meta['item']
        # 内容
        content = response.xpath("//div[contains(@class,'d_post_content_main')]")[0]
        content_str = content.xpath(".//div[contains(@class,'d_post_content')]//text()").getall()
        content_image_urls =  content.xpath(".//div[contains(@class,'d_post_content')]//img/@src").getall()
        item['content_str'] = content_str
        item['content_image_urls'] = content_image_urls
        # 楼层
        lous = response.xpath("//div[@class='l_post j_l_post l_post_bright  ']")
        lous_str = lous.xpath(".//div[contains(@class,'j_d_post_content')]//text()").getall()
        lous_name = lous.xpath(".//li[@class='d_name']//a[@alog-group='p_author']/text()").get()
        lou_num_and_time = lous.xpath(".//ul[@class='p_tail']//li//span//text()").getall()
        for lou in lou_num_and_time:
            lou_num = lou_num_and_time[0]
            lou_time = lou_num_and_time[1]
        # 回复 ---- js获取的








