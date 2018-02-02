import requests
import random
import re
from lxml import etree

keyword = '律师事务所'
page = 1
#url = 'https://www.so.com/s?ie=utf-8&src=360chrome_toolbar_search&q=' + keyword
url = 'https://www.so.com/s?q=' + keyword + '&pn=' + str(page)
click_num = 10

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
ad_index = []
ad_url = []

whitelist=['www.ftlvsuo.com','www.lawyer64.cn','www.jylvsuo.com','www.jyfirm.cn']

def get_html(url):
    global UA_list
    UA = random.choice(UA_list)
    headers = {'User-Agent': UA}
    r = requests.get(url,headers=headers)
    return r.text


def parse(html):
    global ad_index, ad_url
    # ad_index:显示链接 ad_title:广告标题 ad_url:广告标题链接
    sel = etree.HTML(html)

    ad_index1 = sel.xpath('//ul[@id="e_idea_pp"]/li//cite/text()')[:-1]
    for i in ad_index1:
        ad_index.append(i)

    ad_url1 = sel.xpath('//ul[@id="e_idea_pp"]/li/a[@class="e_haosou_fw_bg_title"]/@href')
    for i in ad_url1:
        ad_url.append(i)

def click(click_url,click_num):
    n = 1
    while n <= click_num:
        try:
            r = requests.get(click_url)
            if r.status_code == 200:
                n += 1
                print('第%s次点击'%n)
        except:
            pass
    print('点击完成')
def main():
    html = get_html(url)
    parse(html)
    n = 1
    for a,b in zip(ad_index,ad_url):
        print('排名'+ str(n) +'\n'+ '首页:' + a + '\n' + '链接:' + b )
        n+=1
    try:
        a = str(input('选择排名'))
        click_index = ad_index[a-1]
        click_url = ad_url[a-1]
    except:
        print('输入错误')

main()

