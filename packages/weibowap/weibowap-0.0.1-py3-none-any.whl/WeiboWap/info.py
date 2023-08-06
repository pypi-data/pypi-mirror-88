#coding=utf-8

# import logging
# logging.basicConfig(filename='logging.log',
#                     format='%(asctime)s %(message)s',
#                     filemode="w", level=logging.DEBUG)

# 12.4更新：新增了话题和关键字的查询入口
# 12.5更新：修正新增了个人微博的查询search_weibo2


loginParam={

    "keyword": {
        "q": "鲍毓明涉嫌性侵养女",
        # "nodup": "1",
        # "Refer": "index",
        "page": 1,
    },

    "topic": {
        "q": "鲍毓明涉嫌性侵养女",
        "nodup": "1",
        "page": 1,
    },

    "retweet": {
        "ajwvr": "6",
        "id": "4554794956226910",
        "page": 1,
    },

    "comment": {
        "ajwvr": "6",
        "id": "4554794956226910",
        "page": 1,
        "filter": "hot",
        "sum_comment_number": "85",
        "filter_tips_before": "0",
        "from": "singleWeiBo",
    },

    "weibo": {
        "hasori": "0",
        "haspic": "0",
        "starttime": "20100101",
        "endtime": "20190102",
        "advancedfilter": "1",
        "page": 1
    },

    "weibo2": {
        "is_search": "1",
        "visible": "0",
        "is_ori": "1",
        "is_pic": "1",
        "is_video": "1",
        "is_music": "1",
        "is_article": "1",
        "is_forward": "1",
        "is_text": "1",
        "start_time": "2020-03-01",
        "end_time": "2020-09-30",
        "is_tag": "0",
        "profile_ftype": "1",
        "page": 1,
        "pagebar": 0,
        "pre_page": 0,
    }

}

loginUrls =  {
    'proxyWeb': 'https://www.xicidaili.com/nn/',
    'proxies': {
        # "http": 'http://127.0.0.1:80',
        "https": 'https://127.0.0.1:1080'
    },
    "url":"https://weibo.cn/{:s}/profile?",
    "retweet":"https://weibo.com/aj/v6/mblog/info/big?",
    "comment":"https://weibo.com/aj/v6/comment/big?",
    "weibo":"https://weibo.cn/{:s}/profile?",
    "weibo2":"https://weibo.com/u/{:s}?",
    "keyword":"https://s.weibo.com/weibo?",
    "topic":"https://s.weibo.com/weibo?",
    "base":"https://weibo.com/u/{:s}?",


}
loginHeaders = {

    "home": {
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": "SINAGLOBAL=5579701838206.736.1605880029171; _s_tentry=login.sina.com.cn; Apache=1980597842038.3274.1607741765054; ULV=1607741765062:13:4:1:1980597842038.3274.1607741765054:1607050977044; wb_view_log_3479726797=1536*8641.25; login_sid_t=cf53eed9f11092b2cab4e2805607f91e; cross_origin_proto=SSL; UOR=login.sina.com.cn,weibo.com,login.sina.com.cn; wb_view_log=1536*8641.25; WBtopGlobal_register_version=2020121301; SCF=Alx6A-qiJFwbh6ziknk_s1AyMls2FBOF9t8ivMLmXxCS888rKZV0iwim_0S-V2NhAl1kmO56EbCQ446_Bq2HjMk.; wb_view_log_5331698381=1536*8641.25; wb_view_log_7535112061=1536*8641.25; WBStorage=8daec78e6a891122|undefined; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Whz_p4Vk9iPZuSmielcUwwR5JpX5KzhUgL.FoMfe0BfSK2p1hM2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNSKeXSK-peKnN; SSOLoginState=1607796068; SUB=_2A25y0XUmDeThGeFL6FYU9S_NwzuIHXVRp-HurDV8PUNbmtAKLWHjkW9NQj5heAUbEuYkWAcLeacwN-eKSQ1ZVFUa; ALF=1639332086; wvr=6; wb_view_log_7534551187=1536*8641.25; webim_unReadCount=%7B%22time%22%3A1607796146302%2C%22dm_pub_total%22%3A2%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A3%2C%22msgbox%22%3A0%7D",
        # "referer": "https://weibo.com/lancome?is_hot=1&sudaref=passport.weibo.com",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36 Edg/87.0.664.41",
        "x-requested-with": "XMLHttpRequest"
    },

    "weibo": {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": "_T_WM=63021290217; SCF=Alx6A-qiJFwbh6ziknk_s1AyMls2FBOF9t8ivMLmXxCSMJxgJ5TwiwDy2AnsID1lUSmf_UeupbDgmFOSpAhdHZs.; SUB=_2A25y0-XrDeRhGeNN6FMX-SbPwz2IHXVuP4ujrDV6PUJbktAKLXXCkW1NSdUQYnoF-osjBxBHFl2hShiSeakUiF9X; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFnujsQ4XW.R31ucss9mDQF5NHD95Qfe0epSo.Re0npWs4DqcjGCPSLUPULIBtt; SSOLoginState=1607964091",
        "referer": "https://weibo.cn",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    },



}

loginMsg='''

https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word=%E4%B8%AD%E5%9B%BD%E9%93%B6%E8%A1%8C+%E7%94%B5%E5%AD%90%E9%93%B6%E8%A1%8C&x_bfe_rqs=03E80&x_bfe_tjscore=0.000000&tngroupname=organic_news&newVideo=12&pn=10


'''

loginCookie='wxuin=1610134497; devicetype=android-24; version=2607023a; lang=zh_CN; rewardsn=; wxtokenkey=777; pass_ticket=n7zaWPtBa5p3vItJykj3ZkhXHZ3HchLLwnoEsl+lH2ICQgOCN0EXBSUl85YaESOe; wap_sid2=COHn4v8FEooBeV9ITm1XYmY2bE9rWkpTZDZxbEljVTRpWWdQUkVNbFNxNk1SNURWQWlSVWpzbF9PbnVWb3piN1hERk9rVVBtQ0VHTEdxVVdObjNWZEptSkxVRk5SbDNubTBFdXRYRmIyYVcxazViTUgxOFFJNEkwTkNXVzl5SXhRblRiV3RGb3FzeXR4d1NBQUF+MPvxpf0FOA1AAQ=='

