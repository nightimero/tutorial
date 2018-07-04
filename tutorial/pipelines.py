# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
# todo： twisted db有时会返回空。 所以先使用简单的数据库池
# from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
from DBUtils.PooledDB import PooledDB
from scrapy.crawler import Settings as settings
from scrapy.exceptions import UsageError


class FilterWordsPipeline(object):
    words_to_filter = ['politics', 'religion']

    def process_item(self, item, spider):
        for word in self.words_to_filter:
            if word in unicode(item['description']).lower():
                raise DropItem('Contains forbidden word %s' % word)
            else:
                return item


class TutorialPipeline(object):
    def __init__(self):
        dbargs = dict(
            host='127.0.0.1',
            db='crawed',
            user='root',  # replace with you user name
            passwd='123456',  # replace with you password
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)

    '''
    The default pipeline invoke function
    '''

    def process_item(self, item, spider):
        res = self.dbpool.runInteraction(self.insert_into_table, item)
        return item

    def insert_into_table(self, conn, item):
        conn.execute(
            'insert into zreading(title,author,pub_date,types,tags,view_counts,content) values(%s,%s,%s,%s,%s,%s,%s)', (
                item['title'], item['author'], item['pub_date'], item['types'], item['tags'], item['view_count'],
                item['content']))


class TutorialPipeline2(object):
    def __init__(self):
        # dbargs = dict(
        #     host='127.0.0.1',
        #     db='crawed',
        #     user='root',  # replace with you user name
        #     passwd='123456',  # replace with you password
        #     charset='utf8',
        #     cursorclass=MySQLdb.cursors.DictCursor,
        #     use_unicode=True,
        # )
        # self.dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        self.pool = PooledDB(MySQLdb, 5, host='127.0.0.1', user='root', passwd='123456', db='crawed', port=3306,
                             charset='utf8')
        self.conn = self.pool.connection()
        self.cur = self.conn.cursor()

    '''
    The default pipeline invoke function
    '''

    def process_item(self, item, spider):
        # r = self.cur.execute("select * from dmoz where url='%s'" % item["url"])
        # r = self.cur.fetchone()
        # print u'链接是：', item["url"], u'测试结果：', r
        self.cur.execute("insert into dmoz(author_name,url,description) values(%s,%s,%s)",
                         (item['name'], item['url'], item['description']))
        return item

        # def process_item(self, item, spider):
        #     self.dbpool.runInteraction(self.select_from_table, item)
        #     self.dbpool.runInteraction(self.insert_into_table, item)
        #     return item

        # def select_from_table(self, conn, item):
        #     # print u'传入参数：',item['url']
        #     conn.execute("select * from dmoz where url='%s'" % item['url'])
        #     res = conn.fetchone()
        #     print u'查询结果是：', res
        #     return res
        #
        # def insert_into_table(self, conn, item):
        #     conn.execute('insert into dmoz(author_name,url,description) values(%s,%s,%s)',
        #                  (str(item['name']), str(item['url']), str(item['description'])))


class TutorialPipelineKqShouShu(object):
    def __init__(self):

        dbargs = dict(
            host='127.0.0.1',
            db='crawed',
            user='root',  # replace with you user name
            passwd='123456',  # replace with you password
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            # use_unicode = False,
            use_unicode=True,
        )
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)

    '''
    The default pipeline invoke function
    '''

    def process_item(self, item, spider):
        print u'测试项目', dir(item)
        print u'测试项目str', item
        print u'测试项目class', item.__class__.__name__
        print u'测试爬虫', dir(spider)
        if item.__class__.__name__ == "KqShouShuItem":
            res = self.dbpool.runInteraction(self.insert_into_table_kq_shou_shu, item)
            return item
        elif item.__class__.__name__ == "KqShoushuDetail":
            res = self.dbpool.runInteraction(self.insert_into_table_kq_shou_shu_detail, item)
            return item
        else:
            return UsageError(u'缺少对于item的类')

    # @staticmethod
    def insert_into_table_kq_shou_shu(self, conn, item):
        conn.execute("""insert into kq_shou_shu(shoushu_name,url) values(%s,%s)""",
                     (item['name'], item['url']))

    # @staticmethod
    def insert_into_table_kq_shou_shu_detail(self, conn, item):
        conn.execute("""insert into kq_shou_shu_detail(shoushu_name,
                                                            bu_wei,
                                                            ke_shi,
                                                            shou_shu_fang_shi,
                                                            ma_zui,
                                                            shou_shu_gai_shu,
                                                            shi_ying_zheng,
                                                            bing_fa_zheng                                                            
                            ) values(%s,%s,%s,%s,%s,%s,%s,%s)""",
                     (item['name'],
                      item['bu_wei'],
                      item['ke_shi'],
                      item['shou_shu_fang_shi'],
                      item['ma_zui'],
                      item['shou_shu_gai_shu'],
                      item['shi_ying_zheng'],
                      item['bing_fa_zheng']
                      ))
