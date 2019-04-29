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
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

app = Flask(__name__)

def connect_db():
    return pymysql.connect(host='35.238.104.188', user='root', password='root', db='680', port=3306,autocommit = True, charset = 'utf8mb4',
                           cursorclass = pymysql.cursors.DictCursor)
def get_db():
    '''Opens a new database connection per request.'''
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db



@app.route('/recommendations/<int:user_id>')
def jobRec(user_id):
   
  
   cursor=get_db().cursor();

   cursor().execute("SELECT * FROM jobs")


    #jobs users can get recommendatiosn
   jobs = pd.DataFrame(cursor.fetchall());


   cursor().execute("SELECT *from  users ");

   user_based_approach = pd.DataFrame(cursor.fetchall());

   cursor().execute("SELECT * from  applicants");
   apps = pd.DataFrame(cursor.fetchall());

   user_based_approach[12] = user_based_approach[12].fillna('')
   user_based_approach[13] = user_based_approach[13].fillna('')
   user_based_approach[16] = str(user_based_approach[16].fillna(''))
   user_based_approach[7] = user_based_approach[12] + user_based_approach[13] + user_based_approach[16]

   tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
   tfidf_matrix = tf.fit_transform(user_based_approach[7])

   cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
   indices = pd.Series(user_based_approach.index, index=user_based_approach[0])
    
   idx=indices[user_id];
   
   sim_scores = list(enumerate(cosine_sim[idx]))
    #print (sim_scores)
   sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
   user_indices = [i[0] for i in sim_scores]

   user_based_approach = user_based_approach.reset_index()


   indices = pd.Series(user_based_approach.index, index=user_based_approach[0])

   

   sim_scores = list(enumerate(cosine_sim[idx]))
        #print (sim_scores)
   sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
   user_indices = [i[0] for i in sim_scores]

   jobs_userwise = apps[4].isin(user_indices) #
   df1 = pd.DataFrame(data = apps[jobs_userwise])
   joblist = df1[3].tolist()
   Job_list = jobs[0].isin(joblist)

    
    #job recommendations 
   df_temp = pd.DataFrame(data = jobs[Job_list])

   stuff=df_temp.to_json(orient='records')
    

   return str(jobs);


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



