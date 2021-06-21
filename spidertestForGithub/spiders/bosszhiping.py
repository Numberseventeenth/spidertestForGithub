import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from spidertestForGithub.items import BossItem

"""
    boss直聘网--工作爬虫
"""
class ZhipinSpider(CrawlSpider):
    name = 'zhipin'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/c100010000/?query=python&page=1']

    rules = (
        # 匹配职位列表页的规则
        Rule(LinkExtractor(allow=r'.+\?query=python&page=\d'), follow=True),
        # 匹配职位详情页的规制
        Rule(LinkExtractor(allow=r'.+job_detail/\d+.html'), callback="parse_job", follow=False),
    )

    def parse_job(self, response):
        # 解析详情页
        title = response.xpath("//span[@class='job-title']/text()").get().strip()
        salary = response.xpath("//span[@class='badge']/text()").get().strip()
        city = response.xpath("//a[@class='text-city']/text()").get().strip()
        job_info = response.xpath("//div[contains(@class,'job-primary')]//div[@class='info-primary']/p//text()").getall()
        work_years = job_info[0]
        education = job_info[1]
        company = response.xpath("//a[@ka='job-detail-company_custompage']/text()").get()
        item = BossItem(
            title=title,
            salary=salary,
            city=city,
            work_years=work_years,
            education=education,
            company=company
        )
        yield item
