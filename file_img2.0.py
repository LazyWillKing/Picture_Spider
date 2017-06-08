#!/usr/bin/env python3
# -*- coding: utf_8 -*-

"""
说明
http://mi.talkingdata.com/reports.html
http://mi.talkingdata.com/report-detail.html?id=528
将此页面的链接打开,
将子页面的图片全部爬取出来,下载到对应文件夹中
"""

import os
import re
import requests
import scrapy
from bs4 import BeautifulSoup

root = "E://Python//_requests_study//"	# 根目录

class ImgSpider(scrapy.Spider):
    name = "img_2"
    # allowed_domains = ["www.talkingdata.com"]
    start_urls = ['http://mi.talkingdata.com/reports.html']
    # global root
    # print((re.search(r"\d{3}", start_urls[0]))[0])
    # root = root + (re.search(r"\d{3}", start_urls[0]))[0] + '//'
    # print(root)


    def parse(self, response):
        soup = BeautifulSoup(response.body)
        tag = soup.find_all('a')
        global root
        # print(tag)
        for i in tag:
            try:
                https = i.attrs['href']
                # print(https)
                re.match(r"http://mi.talkingdata.com/report-detail.html",https)[0]
                # print(https)    # 符合上面的条件URL可以进入这一步
                # print(http)
                # yield 产生器
                # yield scrapy.Request(http, self.parse_detail)
                # root = root + (re.findall(r"\d{3}", https))[0] + '//'
                # 这里有链接的自动去重？？？
                # print(root)
                yield scrapy.Request(https,self.parse_detail)
            except:
                pass


    def parse_detail(self,response):
        try:
            # print('----')
            soup = BeautifulSoup(response.body)
            # print(soup)
            tag = soup.find_all('img')
            # print(tag)
            for i in tag:
                try:        #　此处必须加入try 
                    https = i.attrs['src']
                    # print(https)
                    http = re.findall(r"https://www.talkingdata.com/reports/archives/img/\d{2}_\d{13}",https)[0]
                    yield scrapy.Request(http,self.picture_img)
                    print(http)
                except:
                    pass
        except:
            pass
        
    def picture_img(self,response):
        print(response.url)
        global root
        print(root)
        try:
            print('++++++++++++++++++++++')
            path = root + response.url.split('/')[-1] + '.png'	# split '/'分组
            print(path)
            # print(path)
            if not os.path.exists(root):		# 判断更目录是否存在，不存在则建立
                os.mkdir(root)
            if not os.path.exists(path):		# 判断文件是否存在
                r = requests.get(response.url)
                with open(path, 'wb')as f:
                    f.write(r.content)
                    f.close()
                    print("succsee")
            else:
                print("File always allowed")
            # print(html)
        except:
            pass
