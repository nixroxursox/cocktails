import sys
import datetime
import requests

import pymongo as pydb
from pymongo import MongoClient

import sqlite3 as sl

from flask import Flask, redirect, url_for, render_template, session, request, Blueprint, flash, g
import flask_login
from flask_login import LoginManager

import nacl.pwhash
import nacl.utils

from couchbase.cluster import Cluster, ClusterOptions
from couchbase_core.cluster import PasswordAuthenticator


lm = LoginManager()

app = Flask(__name__)
bp = Blueprint('auth', __name__, url_prefix='/auth')


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'GET':
        message = 'Please log in to access the application.'
        return render_template('login.html',message=message)
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            message = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('dashboard'))
            return render_template('login.html', error=error)


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
        #return print(er)

def get_db_mongo(mdbname):
    try:
        db = pydb.MongoClient("mongodb+srv://passw0rd:passw0rd@cluster0.hr0sy.mongodb.net/cluster0?retryWrites=true&w=majority")
        mc = db[mdbname]
        return mc
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to server: %s" % e)
        return e

# Docker couchbase command
# docker run -d --ulimit nofile=40960:40960 --ulimit core=100000000:100000000 --ulimit memlock 000:32000000000 --name couchdb -p 8091-8094:8091-8094 -p 11210:11210 couchbase:community-6.6

def get_couchbase_db():
    pa = PasswordAuthenticator('cosso_user', 'passw0rd')
    try:
        cluster = Cluster('couchbase://127.0.0.1', ClusterOptions(pa))
        return cluster
    except:
        print("exception:", sys.exc_info()[0])
        return "Could not connect to CouchDB"
