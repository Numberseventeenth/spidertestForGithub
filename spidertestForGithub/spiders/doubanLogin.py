import scrapy


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://accounts.douban.com/j/mobile/login/basic']

    def parse(self, response):
        from_data = {
            'ck':'',
            'remember': 'true',
            'name': '13633429426',
            'password': 'wj13633429425'
        }
        # 涉及滑动验证码

