# -*- coding:utf-8 -*-
import scrapy
from scrapy import Selector
from tutorial.items import KqShouShuItem, KqShoushuDetail
from scrapy.http import Request
__author__ = 'shawn'


class KqShouShuSpider(scrapy.Spider):
    name = 'kq_shoushu'
    allowed_domain = ['tag.120ask.com']
    start_urls = [
        "http://tag.120ask.com/shoushu/ks/kouqiangke.html"
    ]

    # def __init__(self, content_detail_urls=None):
    #     super(KqShouShuSpider, self).__init__()
    #     if content_detail_urls is None:
    #         self.content_detail_urls = {}

    def start_requests(self):
        urls = [
            "http://tag.120ask.com/shoushu/ks/kouqiangke.html",
            "http://tag.120ask.com/shoushu/ks/shaoshangwaike.html",
        ]
        for url in urls:
            yield scrapy.FormRequest(url=url, callback=self.parse)

    def parse(self, response):
        # filename = response.url.split('/')[-2]
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        sel = Selector(response)
        sites = sel.xpath('//div[@class="w_cxr fr"]/div/ul/li')
        items = []
        for site in sites:
            item = KqShouShuItem()
            item['name'] = site.xpath('a/text()').extract()[0]
            item['url'] = 'http://tag.120ask.com' + site.xpath('a/@href').extract()[0]
            items.append(item)
            yield scrapy.Request(url=item['url'], callback=self.parse_content)
            yield item

    def parse_content(self, response):
        sel = Selector(response)
        item = KqShoushuDetail()
        item['name'] = sel.xpath('//div[@class="w_n"]/h3/text()').extract()[0]
        item['bu_wei'] = ','.join(sel.xpath('//span[@class="w_span"]/a/text()').extract())
        item['ke_shi'] = sel.xpath('//dd[@class="w_d1"]/span[2]/a/text()').extract()[0]
        item['shou_shu_fang_shi'] = sel.xpath('//dd[@class="w_d2"]/span[1]/text()').extract()[0].replace(u"手术方式：","")
        item['ma_zui'] = sel.xpath('//dd[@class="w_d2"]/span[2]/text()').extract()[0].replace(u"麻醉：","")
        item['shou_shu_gai_shu'] = sel.xpath('//dd[@class="w_d3"]/text()').extract()[0]
        content_detail_urls = {}
        content_detail_urls['shi_ying_zheng'] = 'http://tag.120ask.com' + sel.xpath('//div[@class="w_c2 w_c1 clears"]/ul[1]/li[1]/a[2]/@href').extract()[0]
        content_detail_urls['bing_fa_zheng'] = 'http://tag.120ask.com' + sel.xpath('//div[@class="w_c2 w_c1 clears"]/ul[1]/li[2]/a[2]/@href').extract()[0]
        for key, value in content_detail_urls.items():
            yield Request(url=value, meta={'item': item, 'content_key': key}, callback=self.parse_content_detail)

    def parse_content_detail(self, response):
        sel = Selector(response)
        item = response.meta['item']
        content_detail_key = response.meta['content_key']
        item[content_detail_key] = "\n".join(sel.xpath('//div[@class="w_contl fl"]').xpath('.//p/text()').extract())
        yield item
