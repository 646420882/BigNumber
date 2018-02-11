import requests
import random
import time
import sys
import configparser
from multiprocessing import Pool
from lxml import etree
import re


class Search(object):

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8-sig')

        self.client = config.get('set', 'client')  # 客户端类型

        self.my_index = config.get('set', 'my_index')  # 自己的显示链接
        self.whitelist = config.get('set', 'whitelist').split(',')  # 白名单
        self.blacklist = config.get('set', 'blacklist').split(',')  # 黑名单

        self.switch = int(config.get('click', 'switch'))  # 模式 【0 不点击】【1选定点击】【2排除白名单点击】【3黑名单点击】
        self.click_num = int(config.get('click', 'click_num'))  # 单个链接点击次数
        self.sleep = int(config.get('click', 'sleep'))  # 每次间隔时间

        self.UA_list_PC = [
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        ]  # PC端UA列表
        self.UA_list_M = [
            "NOKIA5700/ UCWEB7.0.2.37/28/999",
            "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
            "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
        ]  # 移动端UA列表

        self.ad_id = []  # 广告位置
        self.ad_index = []  # 显示URL
        self.ad_landurl = []  # 落地页链接
        self.ad_url = []  # 广告链接

    def get_html(self,url):
        while True:
            if self.client == 'M' or 'm':
                UA = random.choice(self.UA_list_M)
            else:
                UA = random.choice(self.UA_list_PC)
            headers = {'User-Agent': UA}
            try:
                r = requests.get(url, headers=headers)
                return r.text
            except:
                print('获取网页出错')

def parse(html):
    global ad_id, ad_index, ad_url, ad_landurl
    # ad_index:显示链接 ad_title:广告标题 ad_url:广告标题链接
    sel = etree.HTML(html)
    ####左侧头部####
    try:
        ad_index1 = sel.xpath('//ul[@id="e_idea_pp"]/li//cite/text()')[:-1]  # 删掉360自身广告  # 显示URL
        for i in ad_index1:
            ad_index.append(i)
            ad_id.append('left-head')
        ad_url1 = sel.xpath('//ul[@id="e_idea_pp"]/li/a/@href')  # 广告链接
        for i in ad_url1:
            ad_url.append(i)
        ad_landurl1 = sel.xpath('//ul[@id="e_idea_pp"]/li/a/@e-landurl')  # 落地页
        for i in ad_landurl1:
            ad_landurl.append(i)
    except:
        print('头部没有广告')
        ####左侧尾部####
    try:
        ad_index1 = sel.xpath('//ul[@id="e_idea_pp_vip_bottom"]/li//cite/text()')
        for i in ad_index1:
            ad_index.append(i)
            ad_id.append('left-foot')
        ad_url1 = sel.xpath('//ul[@id="e_idea_pp_vip_bottom"]/li/a/@href')
        for i in ad_url1:
            ad_url.append(i)
        ad_landurl1 = sel.xpath('//ul[@id="e_idea_pp_vip_bottom"]/li/a/@e-landurl')
        for i in ad_landurl1:
            ad_landurl.append(i)
    except:
        print('尾部没有广告')
        ####右侧广告位####
    try:
        ad_index1 = sel.xpath('//ul[@id="rightbox"]/li//cite/text()')[:-1]  # 删掉360自身广告
        for i in ad_index1:
            ad_index.append(i)
            ad_id.append('right')
        ad_url1 = sel.xpath('//ul[@id="rightbox"]/li/h3/a/@href')[:-1]  # 删掉360自身广告
        for i in ad_url1:
            ad_landurl.append('未显示')
            ad_url.append(i)
    except:
        print('右边没有广告')
def show():
    n = 1
    for a, b, c, d in zip(ad_id, ad_index, ad_landurl, ad_url):
        print('排名' + str(n) + '  位置：' + a + '\n' + '首页:' + b + '\n' + '落地页:' + c + '\n' + '链接:' + d + '\n')
        n += 1
    if my_index in ad_index:
        print('我的排名：%s\n' % (ad_index.index(my_index) + 1))
    else:
        print('暂无排名\n')
def sort(keyword):
    if my_index in ad_index:
        return keyword + ':' + str(ad_index.index(my_index) + 1)
    else:
        return keyword + ':' + '暂无排名'
def click(click_index, click_url, click_num):
    if click_index in whitelist:
        sys.exit('当前网站在白名单中,程序结束')
    print('\nindex：%s\nurl:%s\n点击次数：%s\n\n' % (click_index, click_url, click_num))

    n = 1
    while n <= click_num:
        try:
            r = requests.get(click_url, timeout=10)
            if r.status_code == 200 or r.status_code == 404:
                print('第%s次点击' % n)

        except:
            print('网页无响应，等待%s秒' % sleep)
            time.sleep(sleep)
        n += 1
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(content + '\n')
        f.close()
def main(keyword):
    url = 'https://www.so.com/s?q=' + keyword
    html = get_html(url)
    parse(html)
    show()
    key = sort(keyword)
    print(key)
    write_to_file(key)
    if switch == 1:
        try:
            a = int(input('选择排名\n'))
            click_index = ad_index[a - 1]
            click_url = ad_url[a - 1]
        except:
            sys.exit('输入错误')
        click(click_index, click_url, click_num)
        print('\n点击完成')
    elif switch == 2:
        for click_index, click_url in zip(ad_index, ad_url):
            if click_index in whitelist:
                continue
            click(click_index, click_url, click_num)
        print('\n点击完成')
def get_keywords():
    global keywords
    with open('关键词.txt', 'r') as f:
        keywords = f.read().splitlines()
def 360():
    try:
        sel = etree.HTML(r.text)
        s = sel.xpath('//*[@id="container"]/div[1]/p[1]/text()')[0]  # 落地页
        print(s + '休息30秒')
        time.sleep(30)
    except:
        pass

if __name__ == '__main__':
    print('您的网站：%s' % my_index)
    print('白名单：%s\n' % whitelist)

    get_keywords()
    # print(keywords)
    # for keyword in keywords:
    # main(keyword)
    # time.sleep(1.2)
    pool = Pool()
    pool.map(main, keywords)
    pool.close()
    pool.join()


