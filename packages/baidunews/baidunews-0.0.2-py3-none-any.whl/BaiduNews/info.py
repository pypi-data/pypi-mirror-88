#coding=utf-8

# import logging
# logging.basicConfig(filename='logging.log',
#                     format='%(asctime)s %(message)s',
#                     filemode="w", level=logging.DEBUG)

# 更新：



loginParam={

    "home": {
        "ie": "utf-8",
        "medium": "0",
        "rtt": "1",
        "bsst": "1",
        "rsv_dl": "news_b_pn",
        "cl": "2",
        "wd": "000028 国药一致 国药集团一致药业股份有限公司",
        "tn": "news",
        "rsv_bp": "1",
        "rsv_sug3": "8",
        "rsv_n": "2",
        "oq": "",
        "rsv_btype": "t",
        "f": "8",
        "inputT": "36337",
        "rsv_sug4": "47408",
        "x_bfe_rqs": "03E80",
        "x_bfe_tjscore": "0.000000",
        "tngroupname": "organic_news",
        "newVideo": "12",
        "pn": 0,
    },

    "news": {
        "rtt": "1",
        "bsst": "1",
        "cl": "2",
        "tn": "news",
        "rsv_dl": "ns_pc",
        "word": "中国银行%20电子银行",
        "x_bfe_rqs": "03E80",
        "x_bfe_tjscore": "0.000000",
        "tngroupname": "organic_news",
        "newVideo": "12",
        "p_tk": "9690pxzI+bl3c5beWvpUk28dxjeGllMEb0/2uEfnSPNGDK9Gb7kK1iHJl7UD9Bb+P5ZXE7UmfBXGD+iPjLzq/oD6+PTalcHS2hisTAx8BrjAeDNIW8JymnSeLZOAS2bMTNSi",
        "p_timestamp": "1606068875",
        "p_signature": "b96efcc1e1ffe0e31836f8e26ef1a61c",
        "pn": 0,
    },



}

loginUrls =  {
    'proxyWeb': 'https://www.xicidaili.com/nn/',
    'proxies': {
        "http": 'http://127.0.0.1:80',
        # "https": 'https://127.0.0.1:1080'
    },
    "home":"https://www.baidu.com/s?",
    "news":"https://www.baidu.com/s?",


}
loginHeaders = {
    "home":{
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Cookie": "BAIDUID=DB6D20448BFEBEDC053A472393AD9822:FG=1; PSTM=1598841497; BIDUPSID=18550DA82A4DD1C4347F3A59FEA6617D; BD_UPN=12314753; NOJS=1; ispeed_lsm=2; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDUSS=EFFQVZYZEdWc3ltQ1o0M0pDWjhOa1hZN0VnS1cwckVSa1NPTEZIemhoVW9OdnRmRVFBQUFBJCQAAAAAAAAAAAEAAACKaJBCSVNFVTExMzAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACip018oqdNfe; BDUSS_BFESS=EFFQVZYZEdWc3ltQ1o0M0pDWjhOa1hZN0VnS1cwckVSa1NPTEZIemhoVW9OdnRmRVFBQUFBJCQAAAAAAAAAAAEAAACKaJBCSVNFVTExMzAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACip018oqdNfe; delPer=0; BD_CK_SAM=1; PSINO=1; COOKIE_SESSION=2_0_8_7_0_2_0_0_8_1_1_1_0_0_0_0_0_0_1607930249%7C9%23325506_21_1607582448%7C9; BD_HOME=1; BAIDUID_BFESS=43CC4B6A06513B7330D1BF1B8CE6AB6C:FG=1; H_PS_PSSID=; BDRCVFR[C0p6oIjvx-c]=mk3SLVN4HKm; BDSVRTM=792",
        "Host": "www.baidu.com",
        "Referer": "https://www.baidu.com/s?ie=utf-8&medium=0&rtt=1&bsst=1&rsv_dl=news_t_sk&cl=2&wd=000028+%E5%9B%BD%E8%8D%AF%E4%B8%80%E8%87%B4+%E5%9B%BD%E8%8D%AF%E9%9B%86%E5%9B%A2%E4%B8%80%E8%87%B4%E8%8D%AF%E4%B8%9A%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&tn=news&rsv_bp=1&rsv_sug3=8&rsv_n=2&oq=&rsv_btype=t&f=8&inputT=36337&rsv_sug4=47408",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60"
    },
    "news": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "BIDUPSID=07A5EF20F795C6F28A1664BF003C4348; PSTM=1598845012; BAIDUID=07A5EF20F795C6F20E6FDCA63C2A7B4B",
        "Host": "www.baidu.com",
        "Referer": "https://wappass.baidu.com/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    },

}

loginMsg='''

https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word=%E4%B8%AD%E5%9B%BD%E9%93%B6%E8%A1%8C+%E7%94%B5%E5%AD%90%E9%93%B6%E8%A1%8C&x_bfe_rqs=03E80&x_bfe_tjscore=0.000000&tngroupname=organic_news&newVideo=12&pn=10


'''

loginCookie='wxuin=1610134497; devicetype=android-24; version=2607023a; lang=zh_CN; rewardsn=; wxtokenkey=777; pass_ticket=n7zaWPtBa5p3vItJykj3ZkhXHZ3HchLLwnoEsl+lH2ICQgOCN0EXBSUl85YaESOe; wap_sid2=COHn4v8FEooBeV9ITm1XYmY2bE9rWkpTZDZxbEljVTRpWWdQUkVNbFNxNk1SNURWQWlSVWpzbF9PbnVWb3piN1hERk9rVVBtQ0VHTEdxVVdObjNWZEptSkxVRk5SbDNubTBFdXRYRmIyYVcxazViTUgxOFFJNEkwTkNXVzl5SXhRblRiV3RGb3FzeXR4d1NBQUF+MPvxpf0FOA1AAQ=='

