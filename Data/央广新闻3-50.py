#coding = utf-8
import os
import time
import lxml
import lxml.html
import re
import json
from urllib.parse  import urljoin
import urllib.parse
from lxml import etree
import requests
import cssselect
import urllib
import numpy as np

def get_str(url,code,method,httpmethod = "GET",FormData = None,attr = False ,ip = False):
    out = list()
    if ip:
        ip = requests.get("http://172.16.11.130:5010/get/").text
    if ip:#代理
        pass
    else:#非代理
        if httpmethod =="GET":
            res = urllib.request.Request(url)
            res.add_header("User-Agent",
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134")
            html = urllib.request.urlopen(res, timeout=5).read()
        if httpmethod == "POST":
            data = urllib.parse.urlencode(FormData).encode('utf-8')
            html = urllib.request.urlopen(url, data).read()
    if method == "xpath":
        try:
            html = html.decode()
        except:
            html = html.decode("gbk","ignore")
        html = etree.HTML(html)
        title = html.xpath(code)
        if attr:
            for i in title:
                out.append(i.attrib[attr])
        else:
            for i in title:
                out.append(i.xpath('string(.)').strip())
    if method == "css" :
        html = lxml.html.fromstring(html)
        title = html.cssselect(code)
        if attr:
            for i in title:
                out.append(i.attib[attr])
        else:
            for i in title:
                out.append(i.text_content())
    if method =="re":
        try:
            html = html.decode()
        except:
            html = html.decode("gbk")
        out = re.findall(code,html)
    test = out[0] ####测试结果不为空，负责报错
    return out
a = requests.get("http://172.16.11.36:8080/intelligent/getRegions").json()
dic1 = {}
dic2 = {}
dic3 = {}
for i in a:
    dic1[i["abbr"].replace("省","").replace("市","").replace("区","").replace("县","")] = i["value"]
    for j in i["subs"]:
        dic2[j["abbr"]] = j["value"]
        for k in j["subs"]:
            dic3[k["abbr"].replace("区","").replace("县","")] = k["value"]
dic2["湘西"] = "433100"
dic2.pop('湘西，湘西州，湘西自治州')
cityName = list(dic2.keys())
print(cityName)
def main():
    os.chdir("E:/data/新闻_市_人民网/")
    code = r'href="(http://.+?/\d+?/t\d+?_\d+?.s{0,1}html)"'
    for j in range(8,50):
        print("城市:",cityName[j],j)
        num = 1
        with open(cityName[j] + ".txt", "a", encoding="utf-8") as json_file:
            url = "http://was.cnr.cn/was5/web/search?page=1&channelid=234439&searchword=" + urllib.parse.quote(cityName[j]) + "&keyword=" + urllib.parse.quote(cityName[j]) + "&orderby=LIFO&was_custom_expr=" + urllib.parse.quote(cityName[j]) + "&perpage=10&outlinepage=10&searchscope=&timescope=&timescopecolumn=&orderby=LIFO&andsen=&total=&orsen=&exclude="
            html = urllib.request.urlopen(url).read().decode()
            max_p = int(re.findall(r'找到相关结果约(\d+?)条', html)[0])
            if int(max_p/10) > 1200:
                max_p = 1200
            else:
                max_p = int(max_p/10)
            for i in range(1,max_p):
                urllist = list()
                print("page ",i)
                url = "http://was.cnr.cn/was5/web/search?page=" + str(i) + "&channelid=234439&searchword=" + urllib.parse.quote(cityName[j]) + "&keyword=" + urllib.parse.quote(cityName[j]) + "&orderby=LIFO&was_custom_expr=%28%E6%BC%AF%E6%B2%B3%29&perpage=10&outlinepage=10&searchscope=&timescope=&timescopecolumn=&orderby=LIFO&andsen=&total=&orsen=&exclude="
                try:
                    urllist = get_str(url, code, "re", httpmethod="GET", FormData=None, attr="href", ip=False)
                except:
                    print("打不开")
                urllist = np.unique(urllist)
                for k in range(len(urllist)):
                    code1 = '//*[@class="TRS_Editor"]'
                    code2 = '//*[@class="contentText"]'
                    code3 = '//*[@class="sanji_left"]'
                    code4 = "/html/body/div/section/article"
                    code5 = '//*[@class="image-desc"]'
                    url = urllist[k]
                    try:
                        text = get_str(code=code1, url=url, method="xpath")[0].replace("\r", "").replace("\n","").replace("\u3000", "").replace("\t", "")
                        json_file.write(text + "\t" + dic2[cityName[j]] + "\n")
                    except:
                        try:
                            text = get_str(code=code2, url=url, method="xpath")[0].replace("\r", "").replace("\n","").replace("\u3000", "").replace("\t", "")
                            json_file.write(text + "\t" + dic2[cityName[j]] + "\n")
                        except:
                            try:
                                text = get_str(code=code5, url=url, method="xpath")[0].replace("\r", "").replace("\n","").replace("\u3000", "").replace("\t", "")
                                json_file.write(text + "\t" + dic2[cityName[j]] + "\n")
                            except:
                                try:
                                    text = get_str(code=code3, url=url, method="xpath")[0].replace("\r", "").replace("\n", "").replace("\u3000", "").replace("\t", "")
                                    json_file.write(text + "\t" + dic2[cityName[j]] + "\n")
                                except:
                                    try:
                                        text = get_str(code=code4, url=url, method="xpath")[0].replace("\r","").replace("\n","").replace("\u3000", "").replace("\t", "")
                                        json_file.write(text + "\t" + dic2[cityName[j]] + "\n")
                                    except:
                                        print(url)
    pass
main()
