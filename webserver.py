import sqlite3
from flask import Flask, render_template, request
from flask import g
import sqlite3 as sql
import os
app = Flask(__name__)

DATABASE = r'database/dopplegaenger.db'

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


@app.route('/list')
def list():
    con = get_db()
    con.row_factory = sql.Row
   
    cur = con.cursor()
    cur.execute("select * from guardian")
   
    rows = cur.fetchall(); 
    return render_template("list.html",rows = rows)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    ## I don't like this method but it works
    os.system("python3 guardianbot.py")
    app.run()