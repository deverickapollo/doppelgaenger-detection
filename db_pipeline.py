#!/usr/bin/python
# Item pipeline used to process data after scraping 
import logging, item, db_access
from db_access import *
from contextlib import closing

class sqLitePipeline(object):
    # Take the item and put it in database - do not allow duplicates
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        conn = spider.connection
        curr = db_access.sql_return_row_from_url(conn, adapter["url"])
        result = curr.fetchone()
        if result:
            logging.log(logging.WARNING, "Article already in database table: %s", item)
        else:
            db_access.insert_into_article(conn,item)
            conn.commit()
            logging.log(logging.INFO, "Article stored: %s", item)
        return item

    def close_spider(self, spider):
        close_db_connection(spider.connection)

    def handle_error(self, e):
        logging.error('%s raised an error', e)

class commentPipeline(object):
    # Take the item and put it in database - do not allow duplicates
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        conn = spider.connection
        curr = db_access.sql_return_comment_from_id(conn, adapter["comment_id"])
        result = curr.fetchone()
        if result:           
            logging.log(logging.WARNING, "Comment already in database table: %s", item)
        elif 29 < len(adapter["comment_text"].split()) < 301:
            db_access.insert_into_comment(conn,item)
            conn.commit()
            logging.log(logging.INFO, "Comment stored: %s", item)
        else:
            logging.log(logging.WARNING, "Comment too long or too short: %s", item)
        return item

    def close_spider(self, spider):
        close_db_connection(spider.connection)

    def handle_error(self, e):
        logging.error('%s raised an error', e)