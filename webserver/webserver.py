import guardianbot, logging, asyncio, time, sqlite3 as sql, database.db_access as db
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
    conn = db.get_db(DATABASE)
    conn.row_factory = sql.Row
    cur = db.sql_full_report(conn)
    rows = cur.fetchall(); 
    return render_template("list.html",rows = rows)

@app.route('/comments/<title>')
def comments(title):
    conn = db.get_db(DATABASE)
    conn.row_factory = sql.Row
    cur = db.sql_return_comments_from_title(conn,title)
    rows = cur.fetchall(); 
    return render_template('comments.html',rows = rows)

@app.route('/user/<username>')
def profile(username):
    conn = db.get_db(DATABASE)
    conn.row_factory = sql.Row
    cur = db.sql_select_all_comments_from_user(conn,username)
    rows = cur.fetchall(); 
    return render_template('profile.html', rows = rows)

@tl.job(interval=timedelta(seconds = 60))
def spider_run():
    # list_files = subprocess.run(["watch", "-n60", "python3", -r, "guardianbot.py"])
    logging.log(logging.INFO, "Running Bot")

if __name__== "__main__":
    tl.start()
    while True:
        try:
            app.run()
        except KeyboardInterrupt:
            tl.stop()
            db.close_connection()
            break
