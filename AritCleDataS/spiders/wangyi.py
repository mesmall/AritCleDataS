# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.selector import Selector
import os
class WangyiSpider(scrapy.Spider):

    name = 'wangyi'

    def start_requests(self):
        # first_url = "http://c.m.163.com/nc/auto/list/5bmz6aG25bGx/0-10.html"
        # yield scrapy.Request(url=first_url, callback=self.parse, dont_filter=True)
        for i in range(0, 10, 10):
            url = "http://c.m.163.com/nc/auto/list/5bmz6aG25bGx/" + str(i) + '-' + str(i + 10) + '.html'
            print(url)
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        print (response.text)
        # reData = re.post(qicheapi, headers=headers)
        # print(reData.text)
        text = json.loads(response.text)
        count = 0
        for info in text['list']:
            if ('url_3w' in info):
                if ('title' in info):
                    if (len(info['title'].replace(" ", "")) == 0):
                        break
                    if (len(info['url_3w'].replace(" ", "")) == 0):
                        break
                    print(info['title'].replace(" ", ""))
                    print(info['url_3w'])
                    count = count + 1
                    if ('lmodify' in info):
                        print(info['lmodify'])
                    if(count == 15001):
                        return
                    yield scrapy.Request(url=info['url_3w'], callback=self.parse_content)

    def parse_content(self,response):

        # print response.body
        sel = Selector(response)
        content_div = sel.xpath('//div[@id="endText"]')
        contents = ''
        for content in content_div:
            contents = contents+ content.xpath('string(.)').extract()[0]
        contents = contents.replace(" ","").strip().replace("\t",'').replace("\n","").replace("版权声明：本文版权为网易汽车所有，转载请注明出处。","")
        # title = sel.xpath('//div[@id="epContentLeft"]/h1[1]/text()').extract()
        # contents = "汽车\t".join(title).join(contents)
        # print(contents)
        nowDir = os.path.dirname(os.path.abspath(__file__))
        parentDir = os.path.dirname(os.path.abspath(nowDir))
        dataDir = os.path.join(parentDir,'data')
        wangyiDir = os.path.join(dataDir,"wangyi")
        qiche = os.path.join(wangyiDir,"qiche.txt")
        with open(qiche,'a+') as f:
                print(contents.join("\n"))
                f.write(contents.join("\n"))
                print('写入成功！')


