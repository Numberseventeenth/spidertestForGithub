import scrapy
import re
import datetime
from spidertestForGithub.items import YgrxArticleItem
"""
    抓取阳光热线问政平台（督办回复）
"""
class YgrxSpiderSpider(scrapy.Spider):
    name = 'ygrx_spider'
    allowed_domains = ['sun0769.com']
    start_urls = ['https://wz.sun0769.com/political/index/supervise?page=1']

    def parse(self, response):
        urls = response.xpath("//span[@class='state3']/a/@href").getall()
        for url in urls:
            yield scrapy.Request(url=response.urljoin(url), callback=self.parse_detail)
        # 下一页
        next_url = response.xpath("//a[contains(@class,'prov_rota')]/@href").get()
        if next_url is not None:
            yield scrapy.Request(url=response.urljoin(next_url),callback=self.parse)

    def parse_detail(self, response):
        # 处理详情页
        title = response.xpath("//p[@class='focus-details']/text()").get()
        # author_str = response.xpath("//span[contains(@class,'details-head')]/text()").get()
        # author = author_str.split()
        # fls = response.xpath("//div[contains(@class,'focus-date-list')]//span").getall()

        author = ''.join(response.xpath("//span[@class='fl details-head']//text()").getall())
        author = re.sub(r'\s', '', author)
        data_str = response.xpath("//div[contains(@class,'focus-date-list')]//span[2]/text()").get()
        data_str = re.match(r"发布日期(.*)", data_str).group(1)
        # 转换成日期格式  发布日期2021-06-04 20:25:17   '2021-05-24 09:43:01'
        data = datetime.datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S").date()
        status_str = response.xpath("//div[contains(@class,'focus-date-list')]//span[3]/text()").get()
        # '状态：已回复'
        status_str = re.sub(r'\s', '', status_str)
        status = status_str.split("：")[1]
        # 编号 编号：287343
        num = response.xpath("//div[contains(@class,'focus-date-list')]//span[4]/text()").get()
        num = re.match(r'.*?(\d+)', num).group(1)
        title_detail = response.xpath("//div[@class='details-box']//text()").getall()
        question_department_str = response.xpath("//div[@class='fl politics-fl']/text()").get()
        # 问政部门：轨道交通局
        question_department = question_department_str.split("：")[1]
        reply = response.xpath("//div[@class='gf-reply mr-two']//text()").getall()
        item = YgrxArticleItem(
            title=title,
            author=author,
            data=data_str,
            status=status,
            num=num,
            title_detail=title_detail,
            question_department=question_department,
            reply=reply
        )
        yield item
