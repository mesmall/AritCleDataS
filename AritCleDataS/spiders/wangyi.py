#encoding:utf-8
import re

import scrapy
import json
from scrapy.selector import Selector
import os
class WangyiSpider(scrapy.Spider):

    name = 'wangyi'

    def start_requests(self):

        #types = ["娱乐"]
        types = ["新闻","娱乐","体育","财经","军事","科技","手机","数码","时尚","游戏","教育","健康","旅游","汽车"]
        common = "https://3g.163.com/touch/reconstruct/article/list/"
        #urls = ["BA10TA81wangning"]
        urls = ["BBM54PGAwangning","BA10TA81wangning","BA8E6OEOwangning",
                "BA8EE5GMwangning","BAI67OGGwangning","BA8D4A3Rwangning",
                "BAI6I0O5wangning","BAI6JOD9wangning","BA8F6ICNwangning",
                "BAI6RHDKwangning","BA8FF5PRwangning","BDC4QSV3wangning",
                "BEO4GINLwangning","汽车"]
        #汽车接口和其他不一致，单独针对处理
        for i in range(0, 100, 10):
            url = "http://c.m.163.com/nc/auto/list/5bmz6aG25bGx/" + str(i) + '-' + str(i + 10) + '.html'
            print("爬取页码：" + url)
            meta = {'type': types[len(types)-1],
                    'urlFlag':'list'}

            yield scrapy.Request(url=url, callback=self.parse,meta=meta)
        #其他领域接口通用处理
        flag = 0
        for type in types:
            if str(type).__contains__("汽车"):
                continue
            url = common+urls[flag]+"/"
            for i in range(0,100,10):
                detailurl = url + str(i) + '-' + str(i + 10) + '.html'
                detailurl = detailurl.replace(" ","")
                print("爬取页码："+detailurl)
                meta = {'type': types[flag],
                        'urlFlag':urls[flag]}
                yield scrapy.Request(url=detailurl, callback=self.parse, meta=meta)
            flag = flag+1



    def parse(self, response):
        print("文章类型："+response.meta['type'])
        print("详情内容："+response.text)
        if (len(response.text) == 0):
            print("#################3无数据返回3#################")
            return
        if str(response.meta['type']).__contains__("汽车"):
            text = json.loads(response.text)
            count = 0
            for info in text['list']:
                if ('url_3w' in info):
                    if ('title' in info):
                        if (len(info['title'].replace(" ", "")) == 0):
                            continue
                        if (len(info['url_3w'].replace(" ", "")) == 0):
                            continue
                        if (info['url_3w']).__contains__('http'):
                            count = count + 1
                            print("符合条件本页第多少条："+str(count))
                        else:
                            continue
                        # if (count == 15001):
                        #     return
                        meta = {'count': count,
                                'title':info['title'].replace(" ", "")}
                        yield scrapy.Request(url=info['url_3w'], callback=self.parse_content_qiche, meta=meta)
        else:
            text = response.text.replace("artiList(", "").replace(")", "")
            if(len(text)==0):
                print("#################3无数据返回3#################")
                return
            text = json.loads(text)
            count = 0
            if(str(text).__contains__(response.meta['urlFlag'])):
                for info in text[response.meta['urlFlag']]:
                    if ('url' in info):
                        if ('title' in info):
                            if (len(info['title'].replace(" ", "")) == 0):
                                continue
                            if (len(info['url'].replace(" ", "")) == 0):
                                continue
                            if (info['url']).__contains__('http'):
                                count = count + 1
                                print("符合条件本页第多少条：" + str(count))
                            else:
                                continue
                            # if (count == 15001):
                            #     return
                            meta = {'title':info['title'].replace(" ", ""),
                                    'type':response.meta['type'],
                                    'urlFlag':response.meta['urlFlag']
                            }
                            yield scrapy.Request(url=info['url'], callback=self.parse_content_other, meta=meta)
            else:
                print("###############################################3")
                print(response.meta['urlFlag'])
    def parse_content_other(self,response):
        print(response.meta)
        # print response.body
        sel = Selector(response)
        content_div = sel.xpath('//div[@class="content"]')
        contents = content_div.xpath('string(.)').extract()[0]
        contents = (response.meta['title']+"。"+contents).replace(" ","").strip().replace("\t",'').replace("\n","")
        contents = response.meta['type']+"\t"+contents+"\n"

        fileName = response.meta['type']+'.txt'
        nowDir = os.path.dirname(os.path.abspath(__file__))
        parentDir = os.path.dirname(os.path.abspath(nowDir))
        dataDir = os.path.join(parentDir, 'data')
        wangyiDir = os.path.join(dataDir, "wangyi")
        qiche = os.path.join(wangyiDir, fileName)
        with open(qiche, 'a+') as f:
            print(contents)
            f.write(contents)
            print('写入成功！')
    def parse_content_qiche(self,response):
        print(response.meta)
        # print response.body
        sel = Selector(response)
        content_div = sel.xpath('//div[@id="endText"]')
        contents = ''
        for content in content_div:
            contents = contents+ content.xpath('string(.)').extract()[0]
        contents = contents.replace(" ","").strip().replace("\t",'').replace("\n","").replace("版权声明：本文版权为网易汽车所有，转载请注明出处。","")
        title = sel.xpath('//div[@id="epContentLeft"]/h1[1]/text()').extract()[0]
        contents = "汽车"+"\t"+title.replace(" ","")+"。"+contents+"\n"
        # print(contents)
        nowDir = os.path.dirname(os.path.abspath(__file__))
        parentDir = os.path.dirname(os.path.abspath(nowDir))
        dataDir = os.path.join(parentDir,'data')
        wangyiDir = os.path.join(dataDir,"wangyi")
        qiche = os.path.join(wangyiDir,"汽车.txt")
        with open(qiche,'a+') as f:
                print(contents)
                f.write(contents)
                print('写入成功！')


