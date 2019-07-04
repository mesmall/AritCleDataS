# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.selector import Selector
class WangyiSpider(scrapy.Spider):

    name = 'wangyi'


    def start_requests(self):
        first_url = "http://c.m.163.com/nc/auto/list/5bmz6aG25bGx/10-20.html"
        yield scrapy.Request(url=first_url, callback=self.parse, dont_filter=True)
        for i in range(10, 20000, 10):
            url = "https://3g.163.com /touch/reconstruct/article/list/BBM54PGAwangning/" + str(i + 1) + '-' + str(i + 10) + '.html'
            yield scrapy.Request(url=url, callback=self.parse)




    def parse(self, response):
        print response.text
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
                    yield scrapy.Request(url=info['url_3w'], callback=self.parse_content)

    def parse_content(self, response):
        # print response.body
        sel = Selector(response)
        content_div = sel.xpath('//div[@id="endText"]')
        content = content_div.xpath('string(.)').extract()[0]






