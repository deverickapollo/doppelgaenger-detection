import sqlite3
from flask import Flask, render_template, request
from flask import g
import sqlite3 as sql
import os
import asyncio
import time
from timeloop import Timeloop
import guardianbot
from datetime import timedelta
import logging

app = Flask(__name__)
logging.basicConfig(filename='logs/webapp.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

DATABASE = r'database/dopplegaenger.db'
tl = Timeloop()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    con = get_db()
    con.row_factory = sql.Row
   
    cur = con.cursor()
    cur.execute("select url, title, author, datetime(publish_date, 'unixepoch') from article")

    rows = cur.fetchall(); 
    return render_template("list.html",rows = rows)


@tl.job(interval=timedelta(hours = 12))
def spider_run():
    os.system("python3 guardianbot.py")

if __name__ == '__main__':
    tl.start(block=False)
    while True:
        try:
            spider_run()
            app.run()
        except KeyboardInterrupt:
            # close_connection()
            tl.stop()
            break
