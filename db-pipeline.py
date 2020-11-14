#!/usr/bin/python
# Item pipeline used to process data after scraping 
from db_access import *
from itemadapter import ItemAdapter


class sqLitePipeline(object):
    # Take the item and put it in database - do not allow duplicates
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        
        # sql = "select * from dopplegaenger where url=?", item['url']
        # self.cursor.execute("select * from dopplegaenger where url=?", item['url'])
        # result = self.cursor.fetchone()
        # if result:
        #     log.msg("Item already in database: %s" % item, level=log.DEBUG)
        # else:
        #     self.cursor.execute(
        #         "insert into dopplegaenger (url, desc) values (?, ?)",
        #             (item['url'][0], item['desc'][0])

        #     self.connection.commit()

        #     log.msg("Item stored : " % item, level=log.DEBUG)
        # return item

    def close_spider(self, spider):
        self.file.close()

    def handle_error(self, e):
        log.err(e)

