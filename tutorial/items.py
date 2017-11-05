# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class DmozItem(Item):
    name = Field()
    description = Field()
    url = Field()


class WebcrawlerScrapyItem(Item):
    '''定义需要格式化的内容（或是需要保存到数据库的字段）'''
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    description = Field()
    url = Field()


class TutorialItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    author = Field()
    pub_date = Field()
    types = Field()
    tags = Field()
    view_count = Field()
    content = Field()


class KqShouShuItem(Item):
    name = Field()
    url = Field()

class KqShoushuDetail(Item):
    name = Field()
    bu_wei = Field()
    ke_shi = Field()
    shou_shu_fang_shi = Field()
    ma_zui = Field()
    shou_shu_gai_shu = Field()
    shi_ying_zheng = Field()
    shi_ying_zheng_url = Field()





