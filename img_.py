#!/usr/bin/env python3
# -*- coding: utf_8 -*-

"""
说明
http://mi.talkingdata.com/report-detail.html?id=527
将此页面的图片全部爬取出来,下载到文件夹中
"""


import os
import re
import requests
import scrapy
from bs4 import BeautifulSoup

root = "E://Python//_requests_study//"	# 根目录
class ImgSpider(scrapy.Spider):
    name = "img_"
    allowed_domains = ["www.talkingdata.com"]
    start_urls = ['http://mi.talkingdata.com/report-detail.html?id=527']
    global root
    # print((re.search(r"\d{3}", start_urls[0]))[0])
    root = root + (re.search(r"\d{3}", start_urls[0]))[0] + '//'
    # print(root)


    def parse(self, response):
        soup = BeautifulSoup(response.body)
        tag = soup.find_all('img')
        for i in tag:
            try:
                https = i.attrs['src']
                http = re.findall(r"https://www.talkingdata.com/reports/archives/img/\d{2}_\d{13}",https)[0]
                # print(http)
                # yield 产生器
                yield scrapy.Request(http, self.parse_detail)
            except:
                pass

    def parse_detail(self, response):
        # soup = BeautifulSoup(response.body)
        global root
        try:
            path = root + response.url.split('/')[-1] + '.png'	# split '/'分组
            # print(path)
            if not os.path.exists(root):		# 判断更目录是否存在，不存在则建立
                os.mkdir(root)
            print(root)
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
                # print(https)
                # print(type(tag))