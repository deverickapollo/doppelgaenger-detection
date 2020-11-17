import guardianbot, logging, asyncio, time, sqlite3 as sql
from flask import Flask, render_template, request
from flask import g
from timeloop import Timeloop
from datetime import timedelta

app = Flask(__name__)
logging.basicConfig(filename='logs/webapp.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

DATABASE = r'database/dopplegaenger.db'
tl = Timeloop()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect(DATABASE)
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
    cur.execute("select url, title, author, datetime(publish_date, 'unixepoch') as date from article")

    rows = cur.fetchall(); 
    return render_template("list.html",rows = rows)


@tl.job(interval=timedelta(hours = 12))
def spider_run():
    guardianbot.main()

if __name__ == '__main__':
    tl.start(block=False)
    while True:
        try:
            spider_run()
            app.run()
        except KeyboardInterrupt:
            close_connection()
            tl.stop()
            break
