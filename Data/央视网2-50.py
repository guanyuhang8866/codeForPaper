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
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

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
            html = html.decode("gbk")
        html = etree.HTML(html)
        for i in code:
            try:
                title = html.xpath(i)[0]
                break
            except:
                pass
        if attr:
            for i in title:
                out.append(i.attrib[attr])
        else:
            for i in title:
                out.append(i.xpath('string(.)').strip())
            a = ""
            for i in out:
                a += i
            out = [a]
    if method == "css" :
        html = lxml.html.fromstring(html)
        title = html.cssselect(code)
        if attr:
            for i in title:
                out.append(i.attib[attr])
        else:
            out.append(title.text_content())
    if method =="re":
        try:
            html = html.decode()
        except:
            html = html.decode("gbk")
        out = re.findall(code,html)
    return out
a = requests.get("http://172.16.4.63:8080/intelligent/getRegions").json()
dic1 = {}
dic2 = {}
dic3 = {}
for i in a:
    dic1[i["abbr"].replace("省","").replace("市","").replace("区","").replace("县","")] = i["value"]
    for j in i["subs"]:
        dic2[j["abbr"].replace("市","").replace("区","").replace("县","")] = j["value"]
        for k in j["subs"]:
            dic3[k["abbr"].replace("区","").replace("县","")] = k["value"]
dic2["湘西"] = "433100"
dic2.pop('湘西，湘西州，湘西自治州')
cityName = list(dic2.keys())
def main():
    os.chdir("E:/data/新闻/")
    code = r'=(http:.+?\.s{0,1}html)&'
    for j in range(2,50):
        print("城市:",cityName[j])
        num = 1
        filed = 0
        with open(cityName[j] + ".txt", "a", encoding="utf-8") as json_file:
            for i in range(1,1001):
                urllist = list()
                if filed>10:
                    break
                print("page ",i)
                url = "https://search.cctv.com/search.php?qtext=" + urllib.parse.quote(cityName[j]) + "&sort=relevance&type=web&vtime=&datepid=1&channel=&page="+ str(i)
                try:
                    urllist = get_str(url, code, "re", httpmethod="GET", FormData=None, attr="href", ip=False)
                except:
                    print("当前页打开失败")
                    filed +=1
                urllist = np.unique(urllist)
                for k in range(len(urllist)):
                    code1 = ['//*[@class="body"]',
                             '//*[@class="cnt_bd"]'
                            ]
                    try:
                        text = get_str(code=code1, url=urllist[k], method="xpath")[0].replace("\r", "").replace("\n","").replace("\u3000", "").replace("\t", "")
                        json_file.write(text + "\t" + dic2[cityName[j]]+"\n")
                    except:
                        print(urllist[k])
    pass
main()
