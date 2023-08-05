# -*- coding:utf-8 -*-

import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta
from BaiduNews import info
from urllib import parse
import re
import json

import requests
import random


class Spider():

    def __init__(self, stamp=None):
        self.url = 'https://data.stats.gov.cn/search.htm?'
        self.stamp = (datetime.now()).strftime('%Y%m%d') if stamp is None else stamp
        self.client = MongoClient("localhost", 27017)
        # self.client = MongoClient("mongodb://other:nopassword@127.0.0.1/okooo")
        self.db=self.client['weibocrawl']
        self.cookie=requests.cookies.RequestsCookieJar()
        self.session = requests.session()
        self.param={}
        self.urls = {}                      # 目标网页
        self.headers = {}                   # Get/Post请求头

    # 从配置文件中更新登录链接信息
    def update_info(self):
        self.urls = info.loginUrls                                                  #http地址
        self.headers = info.loginHeaders
        self.param = info.loginParam
        self.cookie.set("cookie", info.loginCookie)
        self.session.cookies.update(self.cookie)

    # 发送Get请求
    def requests_get(self, url, data=None):
        try:
            url = url if data is None else url+parse.urlencode(data)
            print(url)
            # url = url.replace('%2C', ',').replace('%3A', ':').replace('%2B', '+')
            # if url in self.cachePool.keys():
            #     print('cache:')
            #     return self.cachePool[url]
            time.sleep(random.random() * 1 + 0.1)  # 0-1区间随机数
            #没有缓存就开始抓取
            response = self.browser.get(url)
            value=self.browser.page_source


            # value = requests.get(url).text
            # value = requests.get(url, verify=False).text
            # print(value)
            # response = self.session.get(url, proxies=self.urls['proxies'], timeout=10)
            # response.encoding = 'utf-8'
            # value = response if response.status_code == requests.codes.ok else None
        except Exception as e:
            print(e)
            value = None
        finally:
            # pass
            return value
    # 保存htmlPage
    # 保存htmlPage
    def write_page(self, path, page):
        f = open(path, 'w')
        f.write(page.encode('utf-8'))
        f.close()
    # 保存htmlPage
    def read_page(self, path):
        with open(path,'r') as f:
            res=f.read()
            print(res)
            return f.read().decode('gbk')

    def headers_eval(self, headers):
        """
        headers 转换为字典
        :param headers: 要转换的 headers
        :return: 转换成为字典的 headers
        """
        try:
            headers = headers.splitlines()  # 将每行独立为一个字符串
            headers = [item.strip() for item in headers if item.strip() and ":" in item]  # 去掉多余的信息 , 比如空行 , 非请求头内容
            headers = [item.split(':') for item in headers]  # 将 key value 分离
            headers = [[item.strip() for item in items] for items in headers]  # 去掉两边的空格
            headers = {items[0]: items[1] for items in headers}  # 粘合为字典
            headers = json.dumps(headers, indent=4, ensure_ascii=False)  # 将这个字典转换为 json 格式 , 主要是输出整齐一点
            print(headers)
        except Exception:
            print("headers eval get error ...")
            headers = dict()

        return headers

    def headers_get(self, get_headers):
        """
        headers 转换为字典
        :param headers: 要转换的 headers
        :return: 转换成为字典的 headers
        """
        try:
            get0=get_headers.split('?')[0]
            print(get0)
            get1 = get_headers.split('?')[1]
            headers = get1.replace('=',':')
            headers = headers.split('&')  # 将每行独立为一个字符串
            headers = [item.strip() for item in headers if item.strip() and ":" in item]  # 去掉多余的信息 , 比如空行 , 非请求头内容
            headers = [item.split(':') for item in headers]  # 将 key value 分离
            headers = [[item.strip() for item in items] for items in headers]  # 去掉两边的空格
            headers = {items[0]: items[1] for items in headers}  # 粘合为字典
            headers = json.dumps(headers, indent=4, ensure_ascii=False)  # 将这个字典转换为 json 格式 , 主要是输出整齐一点
            print(headers)
        except Exception:
            print("headers eval get error ...")
            headers = dict()

        return headers

    # 下载数据并保存
    def pb_repair(self):
        self._matches = self.db['renwumag1980_2']
        try:
            # 不为空查询
            matches = self._matches.find({'is_original': '转载'})
            # matches = self._matches.find({'video_num': {'$gte': 1}})
            for match in matches:
                try:
                    # content_url=match['content_url']
                    # arc_html = self.requests_get(content_url)
                    # match['arc_html']=arc_html

                    if match['key3'] is not None:
                        continue

                    arc_html=match['arc_html']

                    try:
                        # arc_html=match['arc_html']
                        # print(arc_html)
                        # soup_body = BeautifulSoup(arc_html, "html.parser")
                        print('解析')
                        print(match['content_url'])

                        rex = r'来源 \|(.*?)（ID:.*'

                        pos=arc_html.find('来源 |')
                        pos_str=arc_html[pos:pos+200]
                        # print(pos_str)

                        matchObj = re.match(rex, pos_str, re.M | re.I)
                        if matchObj:
                            rex_src=matchObj.group(1).strip().split(';')[-1]
                            match['key3']=rex_src
                            print(rex_src)
                    except:
                        pass


                    self._matches.update_one({'symbol': match['symbol']}, {"$set": match}, True)
                except Exception as e:
                    print(e)
                    continue
            print(matches.count())
        except:
            print (self.stamp + " error, quit()")
            quit()

    def Imatate(self):
        self.update_info()
        # self._matches = self.db['renwumag1980_2']

        # page=requests.get('https://www.amazon.com/Finer-Things-Timeless-Furniture-Textiles/dp/0770434290/ref=lp_4539344011_1_1?s=books&ie=UTF8&qid=1605336684&sr=1-1').text
        # print(page)
        # return

        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9999")
        # chrome_options.add_argument('--headless')
        # selenium 运行时会从系统的环境变量中查找 webdriver.exe
        # 一般把 webdriver.exe 放到 python 目录中，这样就不用在代码中指定。
        chrome_driver = "C:\Program Files\Google\Chrome\Application/chromedriver.exe"
        self.browser = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)

        cookie={
            "rewardsn":"",
            "wxtokenkey": "777",
        }

        # self.browser.add_cookie({'rewardsn':'','wxtokenkey':'777'})

        # self.browser.add_cookie({'name': 'ASP.NET_SessionId', 'value': 'yy3mnikt0zqeolotjahrrkte'})
        # self.browser.add_cookie({'name': 'fvlid', 'value': '1605284317709aRf8bjOAb0'})

        self.browser.get("https://www.creditchina.gov.cn/")
        # print(self.browser.page_source)
        elem=self.browser.find_element_by_id('search_input')
        elem.send_keys("腾讯")

        self.browser.find_element_by_class_name('search_btn').click()
        print(self.browser.page_source)

        # soup=BeautifulSoup(self.browser.page_source, 'lxml')
        # data=json.loads(soup.text)
        # print(data['data'])

        return

        # self.browser = webdriver.PhantomJS()
        # self.browser.implicitly_wait(10)  # 这里设置智能等待10s

        # url = 'https://linwanwan668.taobao.com/i/asynSearch.htm?mid=w-553869820-0&orderType=hotsell_desc'
        url='https://sycm.taobao.com/portal/home.htm?spm=a211vu.server-home.category.d780.4c575e16BTnoaM'


        try:
            # self.crawl3(url)
            self.pb_repair()
        finally:
            # self.browser.close()
            self.client.close()

    # 解析数据
    def export(self):
        try:
            # for record in self._records.find():
            #     self.parse(record['result'])
            #     for betfair in record['betfair']:
            #         self.parse2(betfair)
            page=self.read_page('test.txt')
            print(page)
        except:
            pass

if __name__ == '__main__':

    hear='''
    
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
cache-control: max-age=0
cookie: UM_distinctid=1760f69a07cd09-0c843c75182574-5a30124a-144000-1760f69a07db87; zg_did=%7B%22did%22%3A%20%221760f69a091451-0361cfaa565c96-5a30124a-144000-1760f69a0923ff%22%7D; _uab_collina=160657635008694471807417; hasShow=1; acw_tc=752252a516074953532218227e86172024f95129f2d640bf722dc5ca71; QCCSESSID=9dr26a3gu1c6us0tltpv78o737; CNZZDATA1254842228=695004087-1606571715-https%253A%252F%252Fwww.baidu.com%252F%7C1607495409; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201607493840455%2C%22updated%22%3A%201607495857929%2C%22info%22%3A%201607260526827%2C%22superProperty%22%3A%20%22%7B%5C%22%E5%BA%94%E7%94%A8%E5%90%8D%E7%A7%B0%5C%22%3A%20%5C%22%E4%BC%81%E6%9F%A5%E6%9F%A5%E7%BD%91%E7%AB%99%5C%22%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22cuid%22%3A%20%22undefined%22%7D
referer: https://www.qcc.com/web/search?key=%E5%B1%B1%E4%B8%9C%E4%B9%85%E6%97%A5%E5%8C%96%E5%AD%A6%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: same-origin
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.57



    '''

    spider=Spider()
    # spider.Imatate()
    # spider.pb_repair()

    # spider.headers_get(hear)
    spider.headers_eval(hear)

    # print(datetime.now())

