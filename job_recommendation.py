import numpy as np
import pandas as pd
from flask import Flask
from flask import jsonify
import mysql.connector
from flask_cors import CORS,cross_origin
import matplotlib.pyplot as plt
import seaborn as sns
import random
import ast 
import random
import json
import os
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



@app.route('/recommendations/<int:user_id>')
@cross_origin(origin="http://localhost:4200/unique_recommendations")
def jobRec(user_id):
   

    mydb = mysql.connector.connect(host="35.238.104.188",user="root",passwd="root",port=3306, db='680'
                               )

    mycursor = mydb.cursor()

    # get jobs 

    mycursor.execute("SELECT * FROM jobs")


    #jobs users can get recommendatiosn
    jobs = pd.DataFrame(mycursor.fetchall());


   

    return str(jobs);

@app.route('/stackrec')
@cross_origin(origin="http://localhost:4200/unique_recommendations")
def recStack():
    feed=feedparser.parse("http://careers.stackoverflow.com/jobs/feed?location=losangeles");
    entry=sorted(feed.entries[:50], key=lambda x: random.random())
    stackOverflowJobs = []
    for e in entry:
        job = {'title': e.title, 'desc': e.description, 'location': e.location}
        stackOverflowJobs.append(job)
    return jsonify(stackOverflowJobs)





if __name__ == '__main__':
    port=int(os.environ.get('PORT', 5000))
    app.run(port=port)

