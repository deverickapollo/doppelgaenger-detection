import guardianbot, logging, asyncio, time, sqlite3 as sql, db_access
from flask import Flask, render_template, request, g
from timeloop import Timeloop
from datetime import timedelta
import subprocess

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

@tl.job(interval=timedelta(seconds = 60))
def spider_run():
    list_files = subprocess.run(["watch", "-n60", "python3", "guardianbot.py"])
    logging.log(logging.INFO, "Running Bot")

if __name__== "__main__":
    tl.start()
    while True:
        try:
            app.run()
        except KeyboardInterrupt:
            tl.stop()
            db_access.close_connection()
            break
