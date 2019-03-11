import os
import re
import jieba
import random

def readtxt(file):
    with open(file,encoding="utf-8") as content:
        table = content.read()
    table = table.split("guanyuhang")
    return table

def readFolder(file):
    txtList = {}
    name1 = os.listdir(file)
    for i in range(len(name1)):
        table = readtxt(os.path.join(file, name1[i]))
        txtList[name1[i][0]] = table
    return txtList

def cut_word(text):
    restr = '[0-9\s+\.\!\/_,$%^*();?:\-<>《》【】+\"\']+|[+——！，；。？：、~@#￥%……&*（）]+'
    resu = text.replace('|', '').replace('&nbsp;', '').replace('ldquo', '').replace('rdquo',
                                                                                    '').replace(
        'lsquo', '').replace('rsquo', '').replace('“', '').replace('”', '').replace('〔', '').replace('〕', '')
    resu = re.split(r'\s+', resu)
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ''.join(resu))
    line = re.sub(restr, '', dd)
    seg_list = jieba.lcut(line)
    return seg_list

def main():
    file = "F:/python/codeForPaper/Data/news_E_pvc/"
    txtlist = readFolder(file)
    f = open("content.txt","w",encoding = "utf-8")
    g = open("lable.txt", "w", encoding="utf-8")
    xlist = []
    ylist = []
    for i in txtlist:
        print(i)
        for j in txtlist[i]:
            word = cut_word(j)
            if len(word) > 20:
                xlist.append(" ".join(word) + "\n")
                ylist.append(i + "\n")
    id = list(range(len(ylist)))
    random.shuffle(id)
    for i in id:
        f.write(xlist[i])
        g.write(ylist[i])
    f.close()
    g.close()

main()