import scrapy
from spidertestForGithub.items import suning_category

"""
    苏宁-图书分类
"""
class SuningBookSpiderSpider(scrapy.Spider):
    name = 'suning_book_spider'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com/']

    def parse(self, response):
        # 大分类分组
        big_categorys = response.xpath("//div[@class='menu-item']//h3/a/text()").getall()
        big_category_urls = response.xpath("//div[@class='menu-item']//h3/a/@href").getall()
        # print('大分类')
        # print(big_categorys)
        # print(big_category_urls)
        # 中分类
        submenu_lefts = response.xpath("//div[@class='menu-sub']//div[@class='submenu-left']")[:9]
        i = 0
        for submenu_left in submenu_lefts:
            # print(big_categorys[i])
            # 检查是否有p标签
            sub_categorys = []
            sub_categorys_urls = []
            if(submenu_left.xpath(".//p")):
                sub_categorys = submenu_left.xpath(".//p/a/text()").getall()
                sub_categorys_urls = submenu_left.xpath(".//p/a/@href").getall()
                # 所有的小分类
                min_categorys = submenu_left.xpath(".//ul")
                j = 0
                for min_category in min_categorys:
                    # sub_categorys[j]
                    min_title = min_category.xpath(".//a/text()").getall()
                    min_title_url = min_category.xpath(".//a/@href").getall()
                    for min,url in zip(min_title,min_title_url):
                        print(big_categorys[i],sub_categorys[j],min)
                        item = suning_category(
                            big_category=big_categorys[i],
                            sub_category=sub_categorys[j],
                            min_category=min,
                            url=url
                        )
                        yield item
                    j += 1
            else:
                sub_categorys = submenu_left.xpath(".//a/text()").getall()
                sub_categorys_urls = submenu_left.xpath(".//a/@href").getall()
                for sub,url in zip(sub_categorys,sub_categorys_urls):
                    print(big_categorys[i], sub)
                    item = suning_category(
                        big_category=big_categorys[i],
                        min_category=sub,
                        url=url
                    )
                    yield item
            i += 1
        pass





