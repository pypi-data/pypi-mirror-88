# -*- coding:utf-8 -*-

# __author:ly_peppa
# date:2020/11/23


# 0.0.1更新：googlenews改为baidunews



import re
import json
import requests
from bs4 import BeautifulSoup
from NyTimesCN import info
from pymongo import MongoClient
import time
import random
import datetime
import xlsxwriter
from urllib import parse
import pandas as pd


class NyTimes():

    def __init__(self):
        self.author_wx = 'ly_peppa'
        self.author_qq = '3079886558'
        self.author_email = 'iseu1130@sina.cn'
        self.urls = {}                      # 目标网页
        self.headers = {}                   # Get/Post请求头
        self.param = {}
        self.cookie=requests.cookies.RequestsCookieJar()
        self.session = requests.session()
        self.client = MongoClient("localhost", 27017)
        self.db=self.client['nytimes']
        self.keywords=None
        self.df_search=None
        self.df_detail=None

    # 从配置文件中更新登录链接信息
    def update_info(self):
        self.urls = info.loginUrls                                                  #http地址
        self.headers = info.loginHeaders
        self.param = info.loginParam
        self.cookie.set("cookie", info.loginCookie)
        self.session.cookies.update(self.cookie)

    # 发送Get请求
    def requests_get(self, url, param=None, headers=None):
        try:
            url = url if param is None else url+parse.urlencode(param)
            time.sleep(random.random() * 1 + 0.1)  # 0-1区间随机数
            #没有缓存就开始抓取
            print(json.dumps(self.urls['proxies']) + ' --> ' + url)
            # response = self.session.get(url, proxies=self.proxy, headers=headers, verify=False)
            # self.session.keep_alive = False
            response = requests.get(url, proxies=self.urls['proxies'], timeout=10)
            response.encoding = response.apparent_encoding
            value = response if response.status_code == requests.codes.ok else None
        except Exception as e:
            value = None
        finally:
            return value

    # 发送Get请求
    def requests_post(self, url, param=None, data=None, headers=None):
        try:
            url = url if param is None else url+parse.urlencode(param)
            time.sleep(random.random() * 1 + 0.1)  # 0-1区间随机数
            #没有缓存就开始抓取
            print(json.dumps(self.urls['proxies']) + ' --> ' + url)
            # response = self.session.get(url, proxies=self.proxy, headers=headers, verify=False)
            # self.session.keep_alive = False
            response = requests.post(url, data=data, proxies=self.urls['proxies'], timeout=10)
            print(response)
            response.encoding = response.apparent_encoding
            value = response if response.status_code == requests.codes.ok else None
        except Exception as e:
            value = None
        finally:
            return value

    # 搜索新闻
    def search_news(self, keywords, day=-365*50, pn=None):
        self._matches = self.db['search_'+keywords]
        self.keywords = keywords
        result=None
        try:
            self.df_search = pd.DataFrame(columns=['id', 'type', 'score', 'site', 'kicker', 'headline', 'byline', 'publication_date', 'web_url', 'web_url_with_host', 'description'])
            self.param['cn']['query']=self.keywords
            self.param['cn']['from'] = 0
            # self.param['cn']['size'] = 100

            self.news_next(keywords, day=day, pn=pn)

            result=self.df_search

        except Exception as e:
            print(e)
        finally:
            return result

    # 搜索新闻
    def news_next(self, keywords, day=-365*50, pn=None):
        result=None
        try:
            if pn is not None:
                if self.param['cn']['from']>=(pn*self.param['cn']['size']):
                    return result

            response=self.requests_get(self.urls['cn'], param=self.param['cn'], headers=self.headers['cn'])
            if response is None:
                return result
            res_json=response.json()
            total=res_json['total']
            # print(res_json['items'][0].keys())
            for item in res_json['items']:
                row=list(item.values())
                print(row)
                self.df_search.loc[len(self.df_search)] = row

                # 更新数据库
                match = self._matches.find_one({'symbol': item['id']})  # 代码
                flag = (match is None)
                if flag:  # 逐条操作数据库比较耗时；暂时关闭
                    match = {}
                    match['symbol'] = item['id']
                    match['keyword'] = keywords
                    match['id'] = item['id']
                    match['type'] = item['type']
                    match['score'] = item['score']
                    match['site'] = item['site']
                    match['kicker'] = item['kicker']
                    match['headline'] = item['headline']
                    match['byline'] = item['byline']
                    match['publication_date'] = item['publication_date']
                    match['web_url'] = item['web_url']
                    match['web_url_with_host'] = item['web_url_with_host']
                    match['description'] = item['description']
                    match['html'] = None
                    match['text'] = None
                    match['content'] = None

                if flag:
                    self._matches.insert_one(match)
                else:
                    self._matches.update_one({'symbol': match['symbol']}, {"$set": match}, True)

            self.param['cn']['from'] = self.param['cn']['from'] + self.param['cn']['size']
            if self.param['cn']['from']<total:
                self.news_next(keywords, day=day, pn=pn)
            # result=self.df_search

        except Exception as e:
            print(e)
        finally:
            return result

    # 搜索新闻
    def news_parse(self, keywords, day=-365*50, pn=None):
        result=None
        try:
            # if pn is not None:
            #     if self.param['home']['pn']>pn:
            #         return result
            # self.param['home']['pn'] = self.param['home']['pn'] + 10
            response = self.requests_get(self.urls['home'], self.param['home'], headers=self.headers['home'])
            if response is None:
                return result
            soup = BeautifulSoup(response.text, "html.parser")
            polite = soup.find('ol', attrs={'data-testid': 'search-results', 'aria-live': 'polite'})

            # page_inner = soup.find('div', id='page').find('a', text='下一页 >')
            search_results=polite.find_all('li',attrs={'class':re.compile("css-1l4w6pd"), 'data-testid': 'search-bodega-result'})
            # print(search_results)
            for item in search_results:
                # print(item)
                # myxawk=
                # stamp=item.find('p', class_='css-myxawk').text.strip()
                # stamp = item.find('span', attrs={'date-testid':re.compile("css-1l4w6pd")}).text.strip()
                subc=item.find('p', class_='css-myxawk').text.strip()
                url = self.urls['base']+item.div.div.div.a['href'].strip()
                title=item.div.div.div.a.h4.text.strip()
                summary = item.find('p', class_='css-16nhkrn').text.strip()
                author = item.find('p', class_='css-15w69y9').text.strip()
                edition = item.find('span', class_='css-bc0f0m')
                edition=None if edition is None else  edition.text.strip()
                # pubstamp = item.find('span', class_='css-bc0f0m').text.split('|')[-1].strip()


                row=[subc,url, title, summary, author, edition]
                print(row)
            #     self.df_search.loc[len(self.df_search)]=row
            # if page_inner:
            #     self.news_next(keywords, day=day, pn=pn)
            # result=self.df_search

        except Exception as e:
            print(e)
        finally:
            return result

    # 查看详情
    def news_detail(self, top=100):
        result=None
        try:
            if self.df_search is None:
                print('self.df_search is None, self.search_news() first')
                return
            self.df_detail = pd.DataFrame(columns=['id', 'type', 'score', 'site', 'kicker', 'headline', 'byline', 'publication_date', 'web_url', 'web_url_with_host', 'description', "html", "text", 'content'])
            for index, row in self.df_search.iterrows():
                # if index>=top:
                #     continue
                try:
                    response = self.requests_get(row['web_url_with_host'])
                    if response is None:
                        row['html'] = "error"
                        row['text']="error"
                        row['content'] = "error"
                    else:
                        soup = BeautifulSoup(response.text, "html.parser")
                        result = soup.get_text().strip()
                        row['html'] = response.text.strip()
                        row['text']=soup.get_text().strip()
                        row['content'] = soup.article.get_text().strip()

                        # nofollow=soup.find('a', rel='nofollow')
                        # row['en_url']=nofollow['href']
                        # response = self.requests_get(row['en_url'])
                        # if response is None:
                        #     row['en_html'] = "error"
                        #     row['en_text'] = "error"
                        #     row['en_content'] = "error"
                        # else:
                        #     soup = BeautifulSoup(response.text, "html.parser")
                        #     result = soup.get_text().strip()
                        #     row['en_html'] = response.text.strip()
                        #     row['en_text'] = soup.get_text().strip()
                        #     row['en_content'] = soup.article.get_text().strip()

                    print(row)
                    self.df_detail.loc[len(self.df_detail)] = row
                except Exception as e:
                    print(e)
                    continue

            result = self.df_detail
            # result = self.df_detail.applymap(lambda x: x.encode('unicode_escape').
            #                            decode('utf-8') if isinstance(x, str) else x)

        except Exception as e:
            print(e)
        finally:
            return result

    # 查看详情
    def news_detail2(self, top=100):
        self._matches2 = self.db['search_COVID-19']
        self._matches = self.db['detail_COVID-19']
        result=None
        try:
            matches=self._matches2.find()
            for row in matches:
                # if index>=top:
                #     continue
                try:
                    match = self._matches.find_one({'symbol': row['id']})  # 代码
                    flag = (match is None)
                    if flag:  # 逐条操作数据库比较耗时；暂时关闭
                        response = self.requests_get(row['web_url_with_host'])
                        if response is None:
                            row['html'] = "error"
                            row['text'] = "error"
                            row['content'] = "error"
                        else:
                            soup = BeautifulSoup(response.text, "html.parser")
                            # result = soup.get_text().strip()
                            row['html'] = response.text.strip()
                            row['text'] = soup.get_text().strip()
                            row['content'] = soup.article.get_text().strip()

                        match = row
                        print(row)

                    if flag:
                        self._matches.insert_one(match)
                    else:
                        pass
                        # self._matches.update_one({'symbol': match['symbol']}, {"$set": match}, True)

                        # nofollow=soup.find('a', rel='nofollow')
                        # row['en_url']=nofollow['href']
                        # response = self.requests_get(row['en_url'])
                        # if response is None:
                        #     row['en_html'] = "error"
                        #     row['en_text'] = "error"
                        #     row['en_content'] = "error"
                        # else:
                        #     soup = BeautifulSoup(response.text, "html.parser")
                        #     result = soup.get_text().strip()
                        #     row['en_html'] = response.text.strip()
                        #     row['en_text'] = soup.get_text().strip()
                        #     row['en_content'] = soup.article.get_text().strip()

                    # print(row)
                    # self.df_detail.loc[len(self.df_detail)] = row
                except Exception as e:
                    print(e)
                    continue

            result = self.df_detail
            # result = self.df_detail.applymap(lambda x: x.encode('unicode_escape').
            #                            decode('utf-8') if isinstance(x, str) else x)

        except Exception as e:
            print(e)
        finally:
            return result

    # 保存
    def news_save(self):
        if self.df_detail is not None:
            self.df_detail.to_csv('detail_{:s}.csv'.format(self.keywords), encoding='utf_8_sig')
            self.df_detail.to_excel('detail_{:s}.xlsx'.format(self.keywords))
            return
        if self.df_search is not None:
            self.df_search.to_csv('search_{:s}.csv'.format(self.keywords), encoding='utf_8_sig')
            self.df_search.to_excel('search_{:s}.xlsx'.format(self.keywords))


    # 获取网页文本
    def html_text(self, web_content):
        result=None
        try:
            soup = BeautifulSoup(web_content, "html.parser")
            result=soup.get_text().strip()
        except Exception as e:
            print(e)
        finally:
            return result

    # 获取网页文本
    def html_content(self, web_content):
        result=None
        try:
            soup = BeautifulSoup(web_content, "html.parser")
            result=soup.article.get_text().strip()
        except Exception as e:
            print(e)
        finally:
            return result

    def extract_article(self, web_content):
        # 防止遇到error卡退
        result="error"
        try:
            soup = BeautifulSoup(web_content, 'lxml')
            articleContent = soup.find_all('p')
            article = []
            for p in articleContent:
                article.append(p.text)
            result = '\n'.join(article).strip()
        except Exception as e:
            print(e)
        finally:
            return result


    def datacleaning(self, text, keyword):
        pattern = re.compile("[,;.，；。]+[^,;.，；。]*" + keyword + "+[^,;.，；。]*[,;.，；。]+")
        result = re.findall(pattern, text)
        for i in range(len(result)):
            result[i] = result[i].replace("\xa0", " ")
            result[i] = result[i].replace("\n", "")
        str = '>>'.join(result)
        return str

    # def textblob_sentiment(self, text):
    #     blob = TextBlob(text)
    #     return blob.sentiment


    def print_df(self, df):
        for index, row in df.iterrows():
            print(index)
            print(row)


    def start(self):
        self.update_info()
        # df_search=self.search_news('中国银行 电子银行',day=-3, pn=None)
        # print(df_search)
        # df_detail=self.news_detail(top=10)
        # print(df_detail)
        # self.news_save()

        # response=self.requests_get(self.urls['cn'], param=self.param['cn'], headers=self.headers['cn'])
        # # response = self.requests_post(self.urls['cn'], data=self.param['data'], headers=self.headers['news'])
        # print(response.text)
        # print(json.loads(response.text))

        # df_search=self.search_news('新型冠状病毒')
        # print(df_search)
        # df_search.to_excel('df_新型冠状病毒.xlsx', engine='xlsxwriter')

        self.news_detail2()

        # df_detail = self.news_detail()
        # print(df_detail)
        # df_detail.to_excel('df_detail.xlsx', engine='xlsxwriter')




if __name__ == '__main__':

    ac=NyTimes()
    ac.start()


