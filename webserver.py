import guardianbot, logging, asyncio, time, sqlite3 as sql, db_access
from flask import Flask, render_template, request
from flask import g
from timeloop import Timeloop
from datetime import timedelta

app = Flask(__name__)
logging.basicConfig(filename='logs/webapp.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
DATABASE = r'database/dopplegaenger.db'
tl = Timeloop()

@app.route('/')
def home():
    conn = db_access.get_db(DATABASE)
    conn.row_factory = sql.Row
    cur = db_access.sql_full_report(conn)
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
            tl.stop()
            db_access.close_connection()
            break
