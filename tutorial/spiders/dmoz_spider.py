# -*- coding:utf-8 -*-
from scrapy import Spider
from scrapy.selector import Selector
from tutorial.items import DmozItem
__author__ = 'shawn'


class DmozSpider(Spider):
    name = 'dmoz'
    allowed_domain = ['dmoztools.net']
    start_urls = [
        "http://dmoztools.net/Computers/Programming/Languages/Python/Books/",
        "http://dmoztools.net/Computers/Programming/Languages/Python/Resources/",
    ]

    def parse(self, response):
        # filename = response.url.split('/')[-2]
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        sel = Selector(response)
        sites = sel.xpath('//div[@class="site-item "]')
        items = []
        for site in sites:
            item = DmozItem()
            item['name'] = site.xpath('div/a/div[@class="site-title"]/text()').extract()[0]
            item['url'] = site.xpath('div[@class="title-and-desc"]/a/@href').extract()[0]
            item['description'] = site.xpath('div/div[@class="site-descr "]/text()').extract()[0].strip()
            print item
            items.append(item)
        return items
