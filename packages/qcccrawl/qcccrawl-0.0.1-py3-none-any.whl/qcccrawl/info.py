#coding=utf-8

# import logging
# logging.basicConfig(filename='logging.log',
#                     format='%(asctime)s %(message)s',
#                     filemode="w", level=logging.DEBUG)

# 更新：



loginParam={

    "home": {
        "key": "山东久日化学科技有限公司",
    },

    "cn": {
        "query": "COVID-19",
        "lang": "",
        "dt": "json",
        "from": 10,
        "size": 100
    },





}

loginUrls =  {
    'proxyWeb': 'https://www.xicidaili.com/nn/',
    'proxies': {
        # "http": 'http://127.0.0.1:80',
        "https": 'https://127.0.0.1:1080'
    },
    "url":"https://www.qcc.com/web/search?key=%E5%B1%B1%E4%B8%9C%E4%B9%85%E6%97%A5%E5%8C%96%E5%AD%A6%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8",
    "base":"https://www.nytimes.com",
    "home":"https://www.qcc.com/web/search?",
    "news":"https://samizdat-graphql.nytimes.com/graphql/v2",
    "cn": "https://cn.nytimes.com/search/data/?",
    "en": "https://www.nytimes.com/search?",


}
loginHeaders = {
    "home":{
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "max-age=0",
        "cookie": "UM_distinctid=1760f69a07cd09-0c843c75182574-5a30124a-144000-1760f69a07db87; zg_did=%7B%22did%22%3A%20%221760f69a091451-0361cfaa565c96-5a30124a-144000-1760f69a0923ff%22%7D; _uab_collina=160657635008694471807417; hasShow=1; acw_tc=752252a516074953532218227e86172024f95129f2d640bf722dc5ca71; QCCSESSID=9dr26a3gu1c6us0tltpv78o737; CNZZDATA1254842228=695004087-1606571715-https%253A%252F%252Fwww.baidu.com%252F%7C1607495409; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201607493840455%2C%22updated%22%3A%201607495857929%2C%22info%22%3A%201607260526827%2C%22superProperty%22%3A%20%22%7B%5C%22%E5%BA%94%E7%94%A8%E5%90%8D%E7%A7%B0%5C%22%3A%20%5C%22%E4%BC%81%E6%9F%A5%E6%9F%A5%E7%BD%91%E7%AB%99%5C%22%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22cuid%22%3A%20%22undefined%22%7D",
        "referer": "https://www.qcc.com/web/search?key=%E5%B1%B1%E4%B8%9C%E4%B9%85%E6%97%A5%E5%8C%96%E5%AD%A6%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.57"
    },
    "cn": {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": "nyt-a=D11dT8T5KAXnM-vTwSLw4k; nyt-purr=cfshcfhssck; purr-cache=<K0<r<C_<G_<S0; _gcl_au=1.1.1850657729.1607245893; walley=GA1.2.1761171692.1607245879; walley_gid=GA1.2.1101779858.1607245895; iter_id=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhaWQiOiI1ZmNjYTA1MTlmY2Y0NjAwMDFhZDYyOGYiLCJjb21wYW55X2lkIjoiNWMwOThiM2QxNjU0YzEwMDAxMmM2OGY5IiwiaWF0IjoxNjA3MjQ1OTA1fQ.E8RgagpKeiKh9tlQZ1QXktO8bc-xP23VsTpqJ2OKLmk; _ga=GA1.2.1562951282.1607255466; _gid=GA1.2.1434335132.1607255466; _cb_ls=1; _cb=DjyZDpCv8NjJ7Z5sO; nyt-gdpr=0; b2b_cig_opt=%7B%22isCorpUser%22%3Afalse%7D; edu_cig_opt=%7B%22isEduUser%22%3Afalse%7D; nyt-us=1; nyt-geo=US; NYT-S=1wwcrX6uPlAHbW.If/UP4p4IGBoZN8X58dkq4VRvmqjyQ0Y1XhUBVu4QS0DwRpKUm5jOoea6bgYnSmrYRS.71QM7Ui.oU0yfoq3DeCo6rhhfXW87VCz6YNO3xDTQO38FS1; nyt-auth-method=sso; _pin_unauth=dWlkPVptTmlaamN4T1RNdFpEUmtZaTAwWkRZekxUZ3pZVGd0TUdNelpqZ3dOREZpTTJReA; _scid=7d1aa91e-1e86-405e-b9f4-dae0343c02ff; FPC=id=f0ff6c0e-529e-4ebd-a3d4-5c329ffe041d; WTPERSIST=regi_id=154810536; _sctr=1|1607270400000; _fbp=fb.1.1607313356792.573512430; LPVID=Q5MzZiZDkzYWY3N2ViZTU5; LPSID-17743901=L34HUkn0QnaLdvoFk0uqjg; datadome=V-x0FvrJ8flQVYoCfJz-K71079-pHQrei0rv4MNxZpQiSl-KYDw~-_YaiSNdDk3DlzFpiHMjMSzrnkWRKcV8ajurHgVcclhAHZEi_PjAU7; nytimes_sec_token=65f855ea1c1bd0dbf31ec81ac3ca3127; NYT-Edition=edition|US; nyt-jkidd=uid=154810536&lastRequest=1607327939375&activeDays=%5B0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C1%2C1%5D&adv=2&a7dv=2&a14dv=2&a21dv=2&lastKnownType=regi; nyt-m=22E5B27A47AEA1D292FB3CEBC43F570E&g=i.0&vp=i.0&iue=i.0&vr=l.4.0.0.0.0&iga=i.0&s=s.core&l=l.2.2316293182.2602256054&ft=i.0&prt=i.0&iru=i.1&iir=i.0&uuid=s.4ee6897b-95d9-4d6e-93a7-8630502577b2&v=i.2&fv=i.0&imu=i.1&imv=i.0&ira=i.0&e=i.1609491600&pr=l.4.0.0.0.0&igu=i.1&igd=i.0&ifv=i.0&n=i.2&er=i.1607327940&cav=i.0&ica=i.0&iub=i.0&t=i.5&igf=i.0&ird=i.0&rc=i.0&ier=i.0; NYTCN-MSS=a%3A5%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22be99d0a99e021f65187b3496314b0ba1%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A12%3A%2210.9.152.131%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A17%3A%22Amazon+CloudFront%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1607330660%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7Db622106fddaa57c1ebfc3039978ce492330d1d45; _chartbeat2=.1607256063148.1607330676339.11.BcyZ_VC72dWCwA8m0BKCUAh9pfDm.1; _cb_svref=https%3A%2F%2Fwww.google.com%2F; AWSALB=zly6M1Jy4MRZVGJvLUm144Ocpd3pZ4qSIXIhK6iqnfGad6KHCOcnGczmYmsi7oywLSt/W1VL5ewJlwx3W42ohCu9wBZ9w7dyHenKBODQs6OtODe7z6aTzxTmeyGE; _gat=1",
        "referer": "https",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

}

loginMsg='''

https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word=%E4%B8%AD%E5%9B%BD%E9%93%B6%E8%A1%8C+%E7%94%B5%E5%AD%90%E9%93%B6%E8%A1%8C&x_bfe_rqs=03E80&x_bfe_tjscore=0.000000&tngroupname=organic_news&newVideo=12&pn=10


'''

loginCookie='nyt-a=D11dT8T5KAXnM-vTwSLw4k; nyt-purr=cfshcfhssck; purr-cache=<K0<r<C_<G_<S0; _gcl_au=1.1.1850657729.1607245893; walley=GA1.2.1761171692.1607245879; walley_gid=GA1.2.1101779858.1607245895; _cb_ls=1; _cb=DyLbDwDGJfaqB0hf8O; iter_id=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhaWQiOiI1ZmNjYTA1MTlmY2Y0NjAwMDFhZDYyOGYiLCJjb21wYW55X2lkIjoiNWMwOThiM2QxNjU0YzEwMDAxMmM2OGY5IiwiaWF0IjoxNjA3MjQ1OTA1fQ.E8RgagpKeiKh9tlQZ1QXktO8bc-xP23VsTpqJ2OKLmk; g_state={"i_p":1607341640678,"i_l":2}; _ga=GA1.2.1562951282.1607255466; _gid=GA1.2.1434335132.1607255466; nyt-gdpr=0; b2b_cig_opt=%7B%22isCorpUser%22%3Afalse%7D; edu_cig_opt=%7B%22isEduUser%22%3Afalse%7D; _cb_svref=https%3A%2F%2Fwww.nytimes.com%2F2020%2F02%2F14%2Fworld%2Fasia%2Fchina-coronavirus.html%3FsearchResultPosition%3D1; nyt-us=1; nyt-geo=US; datadome=HvyVXFfkOm_MMZ6o9KlcfvPgPbGGH7KaF0NNcDkUImRGF_hgZKgGZaAP0n3PYtUBRQPx-6Jg9H5L7Yla~.l6XIRalaYKKhkWUMtSNUOCEA; mnet_session_depth=7%7C1607307260958; nyt-m=E58472F9649D46586C009AF619554FED&l=l.1.2316293182&v=i.1&vr=l.4.0.0.0.0&prt=i.0&ier=i.0&ifv=i.0&t=i.1&n=i.2&g=i.0&vp=i.0&iir=i.0&rc=i.0&ft=i.0&cav=i.0&igu=i.1&igd=i.0&iga=i.0&er=i.1607307399&imu=i.1&ird=i.0&uuid=s.4ee6897b-95d9-4d6e-93a7-8630502577b2&iue=i.0&iub=i.0&igf=i.0&ira=i.0&e=i.1609491600&pr=l.4.0.0.0.0&fv=i.0&ica=i.0&iru=i.1&imv=i.0&s=s.core; nyt-jkidd=uid=0&lastRequest=1607307400019&activeDays=%5B0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C1%2C1%5D&adv=2&a7dv=2&a14dv=2&a21dv=2&lastKnownType=anon; _chartbeat2=.1607245895513.1607307401784.11.BVkTMtBEurMzDMHAIFD5t518BdK0sA.5'

