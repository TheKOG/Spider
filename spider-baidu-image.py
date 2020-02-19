#!/usr/bin/python3

import os
import re
import urllib
import json
import socket
import urllib.request
import urllib.parse
import urllib.error
import time

timeout = 5
socket.setdefaulttimeout(timeout)

def SaveImage(url='https://bigimg.cheerfun.dev/get/https://i.pximg.net/img-original/img/2019/06/13/11/24/48/75200423_p0.jpg',path='test.jpg'):
    rq = urllib.request.Request(url)
    rq.add_header('accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')
    rq.add_header('accept-encoding','gzip, deflate, br')
    rq.add_header('accept-languag','zh-CN,zh;q=0.9,en;q=0.8,pl;q=0.7')
    rq.add_header('sec-fetch-dest','document')
    rq.add_header('sec-fetch-mode','navigate')
    rq.add_header('sec-fetch-site','none')
    rq.add_header('upgrade-insecure-requests','1')
    rq.add_header('user-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36')
    rp = urllib.request.urlopen(rq)
    #print(rp.getcode())
    s=rp.read()
    #print(len(s))
    f=open(path,'wb')
    f.write(s)
    f.close()

class Spider:
    __time_sleep = 0.1
    __amount = 0
    __start_amount = 0
    __counter = 0
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    def __init__(self, t=0.1):
        self.time_sleep = t

    def get_suffix(self, name):
        m = re.search(r'\.[^\.]*$', name)
        if m.group(0) and len(m.group(0)) <= 5:
            return m.group(0)
        else:
            return '.jpeg'

    def fuckpps(self, name):
        dic1={'_z2C$q': ':','_z&e3B':'.','AzdH3F':'/'}
        dic2={'w':'a','k':'b','v':'c','1':'d','j':'e','u':'f','2':'g','i':'h',
            't':'i','3':'j','h':'k','s':'l','4':'m','g':'n','5':'o','r':'p','q':'q','6':'r','f':'s','p':'t','7':'u',
            'e':'v','o':'w','8':'1','d':'2','n':'3','9':'4','c':'5','m':'6','0':'7','b':'8','l':'9','a':'0'}
        for key in dic1 :
            name=name.replace(key,dic1[key])
        n=len(name)
        for i in range(0,n):
            if name[i] in dic2:
                name=name[:i]+str(dic2[name[i]])+name[i+1:]
        return name

    def save_image(self, rsp_data, word):
        if not os.path.exists("./" + word):
            os.mkdir("./" + word)
        self.__counter = len(os.listdir('./' + word)) + 1
        for image_info in rsp_data['data']:

            try:
                time.sleep(self.time_sleep)
                pps=self.fuckpps(image_info['objURL'])
                #print(pps)
                suffix = self.get_suffix(pps)
                SaveImage(pps,'./' + word + '/' + str(self.__counter) + str(suffix))
            except urllib.error.HTTPError as urllib_err:
                print(urllib_err)
                continue
            except Exception as err:
                time.sleep(1)
                print(err)
                print("产生未知错误，放弃保存")
                continue
            else:
                print("涩图+1,已有" + str(self.__counter) + "张涩图")
                self.__counter += 1
        return

    def get_images(self, word='白上吹雪'):
        search = urllib.parse.quote(word)
        pn = self.__start_amount
        while pn < self.__amount:
            url='http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord='+search+'&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&word='+search+'&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&fr=&expermode=&force=&pn='+str(
                pn)+'&rn=60&gsm=3c&1582078498412='
            try:
                time.sleep(self.time_sleep)
                req = urllib.request.Request(url=url, headers=self.headers)
                page = urllib.request.urlopen(req)
                rsp = page.read().decode('utf-8')
                rsp=rsp.replace('\/','/')
            except UnicodeDecodeError as e:
                print(e)
                print('-----UnicodeDecodeErrorurl:', url)
            except urllib.error.URLError as e:
                print(e)
                print("-----urlErrorurl:", url)
            except socket.timeout as e:
                print(e)
                print("-----socket timout:", url)
            else:
                rsp_data = json.loads(rsp)
                self.save_image(rsp_data, word)
                print("下载下一页")
                pn += 60
            finally:
                page.close()
        print("下载任务结束")
        return

    def start(self, word, spider_page_num=1, start_page=1):
        self.__start_amount = (start_page - 1) * 60
        self.__amount = spider_page_num * 60 + self.__start_amount
        self.get_images(word)


if __name__ == '__main__':
    spider = Spider(0.05)
    name=input('你想要谁的涩图?请输入:')
    spider.start(name, 10, 1)
