import scrapy
import time
import json
import random

class RenrenLoginSpider(scrapy.Spider):
    name = 'renren_login'
    allowed_domains = ['rrwapi.renren.com']
    start_urls = ['http://renren.com/']
    appKey = 'bcceb522717c2c49f895b561fa913d10'
    callId = str(int(time.time() * 1000))

    def get_sig(self):
        list = [chr(i) for i in range(97, 123)] + [str(i) for i in range(10)]
        num = random.sample(list, 32)
        num = ''.join(num)
        print('签名：%s' % num)
        return num

    def start_requests(self):
        #5384  login
        url = 'http://rrwapi.renren.com/account/v1/loginByPassword'
        data = {
            'appKey': self.appKey,
            'callId': self.callId,
            'password': "228868a483f2d2c4037cfbd442edce28",
            'sessionKey': "",
            'sig': self.get_sig(),
            'user': "13633429425"
        }
        temp = json.dumps(data)
        # 使用FromRequest发送数据不能转换成json
        # response = scrapy.FormRequest(url=url,formdata=data,callback=self.parse_page)
        response = scrapy.Request(url=url,body=temp,callback=self.parse_page,method='POST')
        yield response

    def parse_page(self,response):
        text_json = json.loads(response.text)
        if text_json['errorMsg'] == '成功':
            print('人人网登录成功')
            sessionKey = text_json['data']['sessionKey']
            uid = text_json['data']['uid']
            secretKey = text_json['data']['secretKey']
            userName = text_json['data']['userName']
            loginState = text_json['data']['loginState']
            # 访问http://rrwapi.renren.com/topic/v1/hotList接口
            # 目前访问失败-------签名失效
            hotlist_url = 'http://rrwapi.renren.com/topic/v1/hotList'
            data = {
                'appKey': self.appKey,
                'app_ver': "1.0.0",
                'callId': self.callId,
                'count': 5,
                'product_id': 2080928,
                'sessionKey': sessionKey,
                'sig': self.get_sig(),
                'uid': uid
            }
            temp = json.dumps(data)
            response = scrapy.Request(url=hotlist_url, body=temp, callback=self.parse_hotlist, method='POST')
            yield response
        else:
            print('人人网登录失败')


    def parse_hotlist(self,response):
        with open('renren_hotlist.html', 'w', encoding='utf-8')as fp:
            fp.write(response.text)

