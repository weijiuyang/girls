    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 19:37:51 2019

@author: jiuyang.wei
"""

import sys
import ssl
import requests
import os
import pickle
from bs4 import BeautifulSoup
import urllib3
from key import keys
from setting import *

urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context
#基础配置
session=requests.session()
html_short=r"https://www.xgmn02.com"

headers = { "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "referer":html_short,
            "cookie": "UM_distinctid=174639a924226-0629a84b4d047c-15306251-13c680-174639a9243582; CNZZDATA1263487746=579143261-1599398858-https%253A%252F%252Fwww.google.com%252F%7C1607414870; __51cke__=; __tins__19410367=%7B%22sid%22%3A%201607416062237%2C%20%22vd%22%3A%202%2C%20%22expires%22%3A%201607417866359%7D; __51laig__=2",
            } 

#读取网站
sites=[]
mycursor = mydb.cursor()

with open ("./netsite.txt","r")as f:
    for web in f:
        web = web.replace('top', 'com')
        # web = web.replace('jpxgmn', 'jpmn5')
        web = web.replace('jpxgmn', 'xgmn02')

        # https://www.xgmn01.com
        # web = web.replace('jpxgyw', 'xgmn09')
        sites.append(web.strip())

#读取置顶页（默认5页）       
if(len(sys.argv)==2):
    page_num_argv=int(sys.argv[1])
else:
    page_num_argv=5

sites = sites[1:]
#获得所有结构写真        
for site in sites:

    page_link=site
    print(page_link)
    #获得前几页写真
    for page in range(1,page_num_argv):
        if not page == 1:
            page_link=site+"page_%s"%page+".html"
        #得到当前页更新的所有写真
        r_page = requests.get(page_link, headers=headers,verify = False)  # 向目标url地址发送get请求，返回一个response对象
        r_page.encoding='utf-8'
        text_page=BeautifulSoup(r_page.text, 'html.parser')

        info_suit = text_page.find_all('li', class_='related_box') 

        for info in info_suit:
            link=info.a['href']
            title=info.a['title']
            print(link,title)
            album_html = html_short + link
            album_page = requests.get(album_html, headers=headers,verify = False)  # 向目标url地址发送get请求，返回一个response对象
            print(html_short + link)
            album_page.encoding='utf-8'
            album_soup=BeautifulSoup(album_page.text, 'html.parser')
            keywords,description,institution_name,serialnumber,mnname=keys(album_soup)
            print(keywords,description,institution_name,serialnumber,mnname)
            sql = "select keywords from information where institution = '%s' and serial_number = '%s'" % (institution_name,serialnumber)
            print(sql)
            mycursor.execute(sql)
            result = mycursor.fetchall()
            if not result:
                sql = 'insert into information (institution,serial_number,keywords,description) values ("%s","%s","%s","%s")' % (institution_name,serialnumber,keywords,description)
                print(sql)
                mycursor.execute(sql)
        mydb.commit()
            # exit()
                
                
                
                
                
                             
