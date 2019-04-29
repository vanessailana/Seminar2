import numpy as np
import pandas as pd
from flask import Flask
from flask import jsonify
from flask import Flask, g, request
import mysql.connector
import pymysql.cursors
import matplotlib.pyplot as plt
import seaborn as sns
import ast 
import random
import json
import feedparser
import mysql.connector
from scipy import stats
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from time import mktime
from datetime import datetime
import pymysql

import atoma
import requests

app = Flask(__name__)

def connect_db():
    return pymysql.connect(host='35.238.104.188', port=3306, user='root', password='root', db='680', cursorclass=pymysql.cursors.DictCursor)
def get_db():
    '''Opens a new database connection per request.'''
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db



@app.route('/recommendations')
def jobRec():
   
  
   con= pymysql.connect(host='35.238.104.188', port=3306, user='root', password='root', db='680', cursorclass=pymysql.cursors.DictCursor)
   
       
   cur = con.cursor()
   cur.execute("SELECT * FROM users")
       
   rows = cur.fetchall()

   
   
   
   return str(rows);


@app.route('/stackrec')
def recStack():
    feed=feedparser.parse("http://careers.stackoverflow.com/jobs/feed?location=losangeles");
    entry=feed.entries[:50]
    stackOverflowJobs = []
    for e in entry:
        job = {'title': e.title, 'desc': e.description, 'location': e.location}
        stackOverflowJobs.append(job)
    return jsonify(stackOverflowJobs)


@app.route('/')
def hello_world():
    return 'Hello, World!'



