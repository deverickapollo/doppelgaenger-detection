#!/usr/bin/python
# Item pipeline used to process data after scraping 
from db_access import *
from itemadapter import ItemAdapter
from contextlib import closing
import logging
import item 

class sqLitePipeline(object):
    # Take the item and put it in database - do not allow duplicates
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        title = str(adapter["title"])
        url = str(adapter["url"])
        author = str(adapter["author"])
        publish_date = str(adapter["publish_date"])
        publish_time = str(adapter["publish_time"])
        tmp = {
            "title": title, 
            "url": url, 
            "author": author, 
            "publish_date": publish_date, 
            "publish_time": publish_time
        }
        conn = spider.connection
        cursorObj = conn.cursor()
        cursorObj.execute("SELECT * FROM guardian WHERE url=?", (url,))
        result = cursorObj.fetchone()

        if result:
            logging.log(logging.WARNING, "Item already in database: %s", item)
        else:
            # insert_into_guardian(conn,tmp)
            # logging.log(logging.INFO, "Lastrowid: %s", cursorObj.lastrowid)
            cursorObj.execute("INSERT INTO guardian (url, author, title, publish_date, publish_time) VALUES (?, ?, ?, ?, ?)", (url,author,title,publish_date, publish_time))
            conn.commit()
            logging.log(logging.INFO, "Item stored: %s", item)
        return item

    def close_spider(self, spider):
        close_connection(spider.connection)

    def handle_error(self, e):
        logging.error('%s raised an error', e)

