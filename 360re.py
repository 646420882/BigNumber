import requests
import random
import time
import sys
import configparser
from lxml import etree
import re
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8-sig')

my_index = config.get('set', 'my_index')
whitelist = config.get('set', 'whitelist').split(',')

switch = config.getboolean('click', 'switch')
click_num = int(config.get('click', 'click_num'))
sleep = int(config.get('click', 'sleep'))
keyword = input('请输入搜索词：\n')


UA_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
ad_index = []  # 显示URL
ad_url = []  # 广告链接
ad_landurl = []  # 落地页链接
ad_id = []  # 广告位置

# whitelist=['www.ftlvsuo.com','www.lawyer64.cn','www.jylvsuo.com','www.jyfirm.cn','m.mzvip.top']

def get_html(url):
    global UA_list
    UA = random.choice(UA_list)
    headers = {'User-Agent': UA}
    r = requests.get(url,headers=headers)
    return r.text
def parse(html):
    global ad_index, ad_url
    # ad_index:显示链接 ad_title:广告标题 ad_url:广告标题链接
    index_pattern =
    ####左侧头部####
    try:
        index_pattern =re.compile('<ul id="e_idea_pp"',re.S)

        ad_index1 = sel.xpath('//ul[@id="e_idea_pp"]/li//cite/text()')[:-1]  # 删掉360自身广告
        for i in ad_index1:
            ad_index.append(i)
            ad_id.append('left-head')
        ad_url1 = sel.xpath('//ul[@id="e_idea_pp"]/li/a/@href')
        for i in ad_url1:
            ad_url.append(i)
        ad_landurl1 = sel.xpath('//ul[@id="e_idea_pp"]/li/a/@e-landurl')
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
            ad_url.append(i)
    except:
        print('右边没有广告')
def show():
    n = 1
    for a, b ,c in zip(ad_id,ad_index, ad_url):
        print('排名' + str(n) + '  位置：' + a + '\n' + '首页:' + b + '\n' + '链接:' + b + '\n')
        n += 1
    if my_index in ad_index:
        print('我的排名：%s\n' % (ad_index.index(my_index) + 1))
    else:
        print('暂无排名\n')
def click(click_num):
    try:
        a = int(input('选择排名\n'))
        click_index = ad_index[a - 1]
        click_url = ad_url[a - 1]
    except:
        sys.exit('输入错误')
    if click_index in whitelist:
        sys.exit('当前网站在白名单中,程序结束')
    print('\n您选择的是\nindex：%s\nurl:%s\n点击次数：%s\n\n'%(click_index,click_url,click_num))

    n = 1
    while n <= click_num:
        try:
            r = requests.get(click_url)
            if r.status_code == 200:
                print('第%s次点击'%n)
                n += 1
        except:
            print('网页无响应，等待30秒')
            time.sleep(sleep)
    print('\n点击完成')
def main(keyword):
    url = 'https://www.so.com/s?q=' + keyword
    html = get_html(url)
    parse(html)
    show()
    if switch:
        click(click_num)
if __name__=='__main__':
    print('您的网站：%s' % my_index)
    print('白名单：%s\n' % whitelist)
    main(keyword)

