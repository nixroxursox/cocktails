import pymongo as pydb
import sqlite3 as sl
from flask import Flask, redirect, url_for, render_template, session, request
import flask_login
import sys
import requests
import sqlite3 as sl
import nacl.pwhash
import nacl.utils
from flask_login import LoginManager
import datetime
from pymongo import MongoClient


lm = LoginManager()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name = user))

    return render_template(login.html)


if __name__ == '__main__':
    app.run(debug=True)


def get_db_sqlite3(dbname):
    dir = 'c:\\Users\\jcbro\\repos\\cocktails\\'
    ext = '.db'
    filename = dir + dbname + ext
    try:
        db = sl.connect(filename)
        sc = db.cursor()
        return sc
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
        c.close()
        return print(er)

def get_db_mongo(mdbname):
    try:
        db = pydb.MongoClient("mongodb+srv://passw0rd:passw0rd@cluster0.hr0sy.mongodb.net/cluster0?retryWrites=true&w=majority")
        mc = db[mdbname]
        return mc
    except pymongo.errors.ConnectionFailure as e:
        return print("Could not connect to server: %s" % e)
