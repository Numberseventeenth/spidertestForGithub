import requests
import json
# 引入队列
from multiprocessing import Queue
from concurrent.futures import ThreadPoolExecutor
from app.douguomeishi.handel_mongo import mongo_info

'''
    app版豆果美食菜谱抓取
'''

# 创建队列
queue_list = Queue()

# 封装请求函数，相同的请求头
def header_request(url,data):
    header = {
        "client": "4",
        "version": "7005.2",
        "device": "CDY-AN00",
        "sdk": "29,10",
        "channel": "huawei",
        "resolution": "2400*1080",
        "display-resolution": "2292*1080",
        "dpi": "3.0",
        "pseudo-id": "unknown",
        "brand": "HUAWEI",
        "scale": "3.0",
        "timezone": "28800",
        "language": "zh",
        "cns": "20",
        "carrier": "CMCC",
        # "imsi": "null",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; CDY-AN00 Build/HUAWEICDY-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36",
        "act-code": "1624412581",
        "act-timestamp": "1624412582",
        # "uuid": "f14c1b91-69f7-4f60-be70-829318b094bd",
        "battery-level": "0.81",
        "battery-state": "1",
        "oaid": "00000000-0000-0000-0000-000000000000",
        "ssid": "d811",
        # "bssid": "b8:3a:08:6c:6f:b1",
        # "syscmp-time": "1621225308000",
        "terms-accepted": "1",
        "newbie": "1",
        "reach": "1",
        "app-state": "0",
        # "cid": "140200",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "Keep-Alive",
        # "session-info": "zZ9ob7xjJtQKWPylkgRuVUAybFclCkq5iKDSHrdXXrqPqwXCuSCPnB2dWH/o+R3wGYD8L56DmyoQYUNLUG4VhqleUaNxMy5crOdADRBt8YZA29UbdXhQC/yXS87clQEV8Wrlpj+3s9Z6u0ffuFP8uXQ37sK6qDclTAVUJySliIs=",
        "Host": "api.douguo.net",
        # "Content-Length": "130",
    }
    # 请求函数构造好了
    response = requests.post(url=url,headers=header,data=data)
    return response

# 菜谱分类页面
def handle_index():
    url = "https://api.douguo.net/recipe/flatcatalogs"
    data = {
        "client": "4",
        # "_session": "162441611584459774e9b65048b84",
        # "v": "1624411171",
        "_vs": "0",
        # "sign_ran": "ba6a1cbda845230e45901917c204af75",
        # "code": "c03da1ce26f83c73",
    }
    response = header_request(url=url,data=data)
    # print(response.text)
    index_response_dict = json.loads(response.text)
    for index_item in index_response_dict['result']['cs']:
        for item in index_item['cs']:
            data_2 = {
                "client": "4",
                # "_session": "162443206278959774e9b65048b84",
                "keyword": item['name'],
                "order": "0",
                "_vs": "400",
                # "type": "0",
                # "auto_play_mode": "2",
                # "sign_ran": "4c1eef53bbb591f3c0b88ec7151119f5",
                # "code": "4df27fc3b9848b46",
            }
            queue_list.put(data_2)

# 线程的处理函数，把队列中的data get出来
# 请求菜谱中的列表页和内容页
def handle_caipu_list(data):
    print('当前处理的食材：' ,data['keyword'])
    caipu_list_url = "https://api.douguo.net/recipe/v2/search/0/20"
    # 第一次请求
    caipu_list_response = header_request(url=caipu_list_url,data=data)
    # print(caipu_list_response.text)
    caipu_list_response_dict = json.loads(caipu_list_response.text)
    for item in caipu_list_response_dict['result']['list']:
        caipu_info = {}
        caipu_info['shicai'] = data['keyword']
        if item['type'] == 13:
            caipu_info['usename'] = item['r']['an']
            caipu_info['shicai_id'] = item['r']['id']
            caipu_info['caipu_name'] = item['r']['n']
            caipu_info['cook_difficulty'] = item['r']['cook_difficulty']
            caipu_info['cook_time'] = item['r']['cook_time']
            caipu_info['describe'] = item['r']['cookstory'].replace("\n",'').replace(' ','')
            caipu_info['zuoliao_list'] = item['r']['major']
            # caipu_info['tags'] = item['r']['tags']

            detail_url = "https://api.douguo.net/recipe/v2/detail/" + str(item['r']['id'])
            detail_data = {
                "client": "4",
                # "_session": "162443533482059774e9b65048b84",
                "author_id": "0",
                "_vs": "11102",
                "_ext": '{"query":{"kw":' + caipu_info['caipu_name'] +',"src":"11102","idx":"2","type":"13","id":'+ str(caipu_info['shicai_id']) +'}}',
                # "is_new_user": "1",
                # "sign_ran": "721e3006097522b9d1728e339d6e2163",
                # "code": "c4f0a9ea957238ce",
            }
            # 第二次请求
            detail_response = header_request(url=detail_url,data=detail_data)
            detail_response_response_dict = json.loads(detail_response.text)
            caipu_info['tips'] = detail_response_response_dict['result']['recipe']['tips']
            caipu_info['cook_step'] = detail_response_response_dict['result']['recipe']['cookstep']
            print('当前入库的菜谱是：',caipu_info['caipu_name'])
            # 存入数据库
            mongo_info.insert_item(caipu_info)
        else:
            continue

handle_index()
# 实现多线程抓取，引入了线程池
pool = ThreadPoolExecutor(max_workers=2)
while queue_list.qsize() > 0:
    pool.submit(handle_caipu_list,queue_list.get())
