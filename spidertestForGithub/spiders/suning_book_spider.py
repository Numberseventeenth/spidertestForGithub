import scrapy


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
            print(big_categorys[i])
            # 检查是否有p标签
            sub_categorys = []
            sub_categorys_urls = []
            if(submenu_left.xpath(".//p")):
                sub_categorys = submenu_left.xpath(".//p/a/text()").getall()
                sub_categorys_urls = submenu_left.xpath(".//p/a/@href").getall()
                min_categorys = submenu_left.xpath(".//ul")

            else:
                sub_categorys = submenu_left.xpath(".//a/text()").getall()
                sub_categorys_urls = submenu_left.xpath(".//a/@href").getall()
            print(sub_categorys)
            i += 1





