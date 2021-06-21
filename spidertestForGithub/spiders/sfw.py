import scrapy
import re
from spidertestForGithub.items import NewHouseItem,ESFHouseItem

class SfwSpider(scrapy.Spider):
    name = 'sfw'
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    # 解析所有城市的url
    def parse(self, response):
        trs = response.xpath("//div[@class='outCont']//tr")
        province = None
        for tr in trs:
            tds = tr.xpath(".//td[not(@class)]")
            province_td = tds[0]
            province_text = province_td.xpath(".//strong/text()").get()
            if province_text == ' ':
                province_text = None
            # 有strong标签里面为空
            if province_text:
                province = province_text
            city_td = tds[1]
            city_links = city_td.xpath(".//a")
            for city_link in city_links:
                city = city_link.xpath(".//text()").get()
                city_url = city_link.xpath(".//@href").get()
                # print("%s,%s,%s" % (province,city,city_url))
                # 构建新房的url  https://hf.newhouse.fang.com/house/s/
                if 'bj.' in city_url:
                    newhouse_url = "https://newhouse.fang.com/house/s/"
                    esf_url = "https://esf.fang.com/"
                else:
                    city_url = city_url.split('.')
                    city_url.insert(1, "newhouse")
                    newhouse_url = '.'.join(city_url)
                    # 构建二手房url
                    city_url[1] = 'esf'
                    esf_url = ".".join(city_url)
                # print(newhouse_url)
                # print(esf_url)
                yield scrapy.Request(url=newhouse_url,callback=self.parse_newhouse,meta={'info':(province,city)})

                yield scrapy.Request(url=esf_url,callback=self.parse_esf,meta={'info':(province,city)})



    def parse_newhouse(self,response):
        province,city = response.meta.get('info')
        lis = response.xpath("//div[contains(@class,'nl_con')]/ul/li")
        for li in lis:
            name = li.xpath(".//div[@class='nlcd_name']/a/text()").get()
            # name不为空时取
            if name:
                name = re.sub(r'\s','',name)
                house_type_list = li.xpath(".//div[contains(@class,'house_type')]//a//text()").getall()
                rooms = list(filter(lambda x:x.endswith("居"),house_type_list))
                area = "".join(li.xpath(".//div[contains(@class,'house_type')]/text()").getall())
                area = re.sub(r'\s|－|/',"",area)
                address = li.xpath(".//div[contains(@class,'address')]/a/@title").get()
                district_text = "".join(li.xpath(".//div[contains(@class,'address')]/a/text()").getall())
                district = re.search(r".*\[(.+)\].*",district_text).group(1)
                sale = li.xpath(".//div[contains(@class,'fangyuan')]/span/text()").get()
                price = re.sub(r'\s|广告','',"".join(li.xpath(".//div[contains(@class,'nhouse_price')]//text()").getall()))
                origin_url = li.xpath(".//div[@class='nlcd_name']/a/@href").get()
                item = NewHouseItem(
                    name=name,
                    price=price,
                    rooms=rooms,
                    area=area,
                    address=address,
                    district=district,
                    sale=sale,
                    origin_url=origin_url,
                    province=province,
                    city=city
                )
                yield item
        next_url = response.xpath("//div[@class='page']//a[@class='next']/@href").get()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url),callback=self.parse_newhouse,meta={'info':(province,city)})

    def parse_esf(self,response):
        province,city = response.meta.get('info')
        dls = response.xpath("//dl[@class='clearfix']")
        for dl in dls:
            item = ESFHouseItem(province=province,city=city)
            name = dl.xpath(".//p[@class='add_shop']/span/text()").get()
            if name:
                infos = dl.xpath(".//p[class='tel_shop']/text()").getall()
                infos = list(map(lambda x:re.sub(r'\s','',x),infos))
                for info in infos:
                    if '厅' in info:
                        item['rooms'] = info
                    elif '层' in info:
                        item['floor'] = info
                    elif '向' in info:
                        item['toward'] = info
                    elif '年' in info:
                        item['year'] = info.replace('年建','')
                    elif 'm' in info:
                        item["area"] = info
                item['address'] = dl.xpath(".//div[@class='add_shop']/span/text()").get()
                item['price'] = dl.xpath(".//div[@class='price_right']//b/text()").get()
                item['unit'] = dl.xpath(".//div[@class='price_right']/span[last()]/text()").get()
                item['origin_url'] = response.urljoin(dl.xpath(".//h4[@class='clearfix']/a/@href").get())
                item['name'] = name
                yield item
        next_url = response.xpath("//div[@class='page_al']/p[last()-1]/a/@href").get()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse_esf,
                                 meta={'info': (province, city)})





