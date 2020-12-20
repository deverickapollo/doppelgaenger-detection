#!/usr/bin/python
# Item pipeline used to process data after scraping 
import logging, item, database.db_access as db
from database.db_access import *
from contextlib import closing
from feature_matrix import feature_matrix
total_comment_count = 0
total_user_count = 0
total_article_count = 0

#The average comment length
comments_per_user = 0
avg_comment_length = 0
total_comment_words = 0

class sqLitePipeline(object):
    # Take the item and put it in database - do not allow duplicates
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        conn = spider.connection
        cursor = db.sql_return_row_from_url(conn, adapter["url"])
        result = cursor.fetchone()
        if result:
            logging.log(logging.WARNING, "Article already in database table: %s", item)
        else:
            db.insert_into_article(conn,item)
            global total_article_count
            total_article_count += 1
            conn.commit()
            logging.log(logging.INFO, "Article stored: %s", item)
        return item

    def close_spider(self, spider):
        print("Total Articles Inserted: ", str(total_article_count))
        logging.log(logging.INFO, "Total Articles stored: %s", total_article_count)

    def handle_error(self, e):
        logging.error('%s raised an error', e)

class commentPipeline(object):
    # Take the item and put it in database - do not allow duplicates
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        comment_id = adapter["comment_id"]
        conn = spider.connection
        cursor = db.sql_return_comment_from_id(conn, comment_id)
        result = cursor.fetchone()
        comment_string = result[1]
        

        if result is not None and comment_string == adapter["comment_text"]:
            logging.log(logging.WARNING, "Comment already in database table: %s", item)
        elif 29 < len(adapter["comment_text"].split()) < 301:
            curse = db.sql_check_username_exist(conn, adapter["comment_author_username"])
            user_exist_fetch = curse.fetchone()
            curse2 = db.sql_check_userid_exist(conn, adapter["comment_author_id"])
            user_exist2_fetch = curse2.fetchone()
            logging.log(logging.INFO, "Username %s and ID %s to insert", adapter["comment_author_username"],adapter["comment_author_id"])
            if user_exist_fetch is not None and user_exist2_fetch is not None: 
                logging.log(logging.INFO, "User %s with userid %s is already in the database", adapter["comment_author_username"],adapter["comment_author_id"])
            elif user_exist_fetch is None and user_exist2_fetch is None:
                logging.log(logging.INFO, "The results before the fail %s", user_exist_fetch)
                db.insert_into_user(conn,item)
                global total_user_count
                total_user_count += 1
            db.insert_into_comment(conn,item)
            global total_comment_count 
            global total_comment_words
            total_comment_words += len(adapter["comment_text"].split())
            total_comment_count += 1
            conn.commit()
            logging.log(logging.INFO, "Comment stored: %s", item)
            logging.log(logging.INFO, "Computing Comment Statistics on: %s", item)
            statistics = feature_matrix(comment_string)
            logging.log(logging.INFO, "Computing Statistics Complete")
            logging.log(logging.INFO, "Statistic stored: %s", item)
            db.insert_into_stats(conn, comment_id, statistics)
        else:
            logging.log(logging.WARNING, "Comment too long or too short: %s", item)
        return item

    def close_spider(self, spider):
        avg_comment_length = total_comment_words/total_comment_count
        comments_per_user = total_comment_count/total_user_count

        print("Total Comments Inserted: ", str(total_comment_count))
        print("Total Users Inserted: ", str(total_user_count))

        print("Average Comment Length: ", str(avg_comment_length))
        print("Average Comments Per User: ", str(comments_per_user))

        logging.log(logging.INFO, "Total Comments stored: %s", total_comment_count)
        logging.log(logging.INFO, "Total Users stored: %s", total_user_count)

        logging.log(logging.INFO, "Average Comment Length: %s", str(avg_comment_length))
        logging.log(logging.INFO, "Average Comment Per User: %s", str(comments_per_user))
    def handle_error(self, e):
        logging.error('%s raised an error', e)