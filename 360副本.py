import requests
import random
import time
import sys
import configparser

from lxml import etree
import re


class Search(object):

    def __init__(self,keyword):
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8-sig')

        self.client = int(config.get('set', 'client'))  # 客户端类型 【1：360PC】【2:360M】【3：搜狗PC】【4搜狗M】【5神马M】

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

        self.url = ''  # 搜索页链接
        self.keywords = []  # 关键词列表

        self.keyword = keyword

        # self.ad_index_pattern = ''
        # self.ad_url_pattern = ''
        # self.ad_landurl_pattern = ''

        self.ID = ''  # 搜索引擎
        self.ad_index = []  # 显示URL
        self.ad_url = []  # 广告链接


    def get_html(self):
        while True:
            UA = random.choice(self.UA_list_PC)
            if self.client == 1 or self.client == 3:
                UA = random.choice(self.UA_list_PC)
                print('选择%s,PC端'%self.client)  # 调试用
            else:
                UA = random.choice(self.UA_list_M)
                print('选择%s,移动端' % self.client)  # 调试用
            headers = {'User-Agent': UA}
            try:
                r = requests.get(self.url, headers=headers)
                r.encoding = r.apparent_encoding
                return r.text
            except:
                print('获取网页出错，10秒后重试')
                time.sleep(10)
    def get_keywords(self):
        with open('关键词.txt', 'r') as f:
            self.keywords = f.read().splitlines()
    def parse(self, html):
        sel = etree.HTML(html)
        try:
            self.ad_index = sel.xpath(self.ad_index_pattern)
            self.ad_url = sel.xpath(self.ad_url_pattern)
            # 去除搜狗显示链接日期
            if self.client == 2:
                ad_index1 = []
                for i in self.ad_index:
                    ad_index1.append(i.strip().replace('\n',''))
                self.ad_index = ad_index1
            elif self.client == 3:
                ad_index1 = []
                for i in self.ad_index:
                    ad_index1.append(i.split()[0])
                self.ad_index = ad_index1
            
            # 核对【显示链接】【广告链接】是否对应
            if len(self.ad_index) != len(self.ad_url):
                for i in self.ad_index:
                    print('index:%s\n'%i)
                for i in self.ad_url:
                    print('ad_url:%s\n'%i)
                print('未对齐')
            else:
                print('%-10s%-40s%-40s'%('ID','Index','url'))
                for a,b in zip(self.ad_index,self.ad_url):
                    print('%-10s%-40s%-40s'%(self.ID,a,b))
        except:
            print('未找到')
    def show(self):
        print('我的URL：%s\n'%self.my_index)
        for i in self.ad_index:
            print('显示URL:%s'%i)
        if self.my_index in self.ad_index:
            print('我的排名：%s\n' % (self.ad_index.index(self.my_index) + 1))
        else:
            print('暂无排名\n')
    def choice(self):
        #判断搜索类型
        if self.client == 1:
            self.url = 'https://www.so.com/s?q=' + self.keyword
            self.ID = 'QiHu PC'
            self.ad_index_pattern = '//ul[@id="e_idea_pp"]/li[not(@id)]//cite/text()'
            self.ad_url_pattern = '//ul[@id="e_idea_pp"]/li[not(@id)]/a/@href'
        elif self.client == 2:
            self.url = 'https://m.so.com/s?q=' + self.keyword
            self.ID = 'QiHu M'
            self.ad_index_pattern = '//div[@class="r-results"]/div[@class="tg-wrap"]//a[@class="e_fw_brand_link"]/text()'
            self.ad_url_pattern = '//div[@class="r-results"]/div[@class="tg-wrap"]//a[@class="e_fw_brand_link"]/@href'
        elif self.client == 3:
            self.ID = 'SoHu PC'
            self.url = 'https://www.sogou.com/web?query=' + self.keyword
            #self.ad_index_pattern = '//div[@class="biz_sponsor"]/div[@class="biz_rb "]//div[@class="biz_fb"]/cite/text()'
            #self.ad_url_pattern =   '//div[@class="biz_sponsor"]/div[@class="biz_rb "]/h3[@class="biz_title"]/a[1]/@href'
            self.ad_index_pattern = '//div[@class="biz_rb "]//div[@class="biz_fb"]/cite/text()'
            self.ad_url_pattern =   '//div[@class="biz_rb "]/h3[@class="biz_title"]/a[1]/@href'
        elif self.client == 4:
            self.ID = 'SoHu M'
            self.url = 'https://wap.sogou.com/web/searchList.jsp?&keyword=' + self.keyword
            self.ad_index_pattern = '//div[@class="ad_result"]//div[@class="citeurl"]/text()'
            self.ad_url_pattern = '//ul[@id="e_idea_pp"]/li[not(@id)]/a/@href'
        elif self.url == 5:
            self.ID = 'ShenMa M'
            self.url = 'http://m.sm.cn/s?q=' + self.keyword
            self.ad_index_pattern = '//ul[@id="e_idea_pp"]/li[not(@id)]//cite/text()'
            self.ad_url_pattern = '//ul[@id="e_idea_pp"]/li[not(@id)]/a/@href'
        else:
            print('类型错误')
        print('您的网站：%s' % self.my_index)
        print('白名单：%s' % self.whitelist)
        print('黑名单：%s' % self.blacklist)
        print('点击模式：%s'%self.switch)
        print('搜索引擎：%s'%self.ID)
        print('搜索URL：%s'%self.url)



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

def QiHu():
    try:
        sel = etree.HTML(r.text)
        s = sel.xpath('//*[@id="container"]/div[1]/p[1]/text()')[0]  # 落地页
        print(s + '休息30秒')
        time.sleep(30)
    except:
        pass

if __name__ == '__main__':
    keyword = input('输入关键词\n')
    app = Search(keyword)
    app.choice()
    html = app.get_html()
    app.parse(html)
    app.show()


    #get_keywords()
    # print(keywords)
    # for keyword in keywords:
    # main(keyword)
    # time.sleep(1.2)



