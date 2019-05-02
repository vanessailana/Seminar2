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
@cross_origin(origin="https://quiet-waters-20201.herokuapp.com/")
def jobRec(user_id):
   

    mydb = mysql.connector.connect(host="35.238.104.188",user="root",passwd="root",port=3306, db='680'
                               )

    mycursor = mydb.cursor()

    # get jobs 

    mycursor.execute("SELECT * FROM jobs")


    #jobs users can get recommendatiosn
    jobs = pd.DataFrame(mycursor.fetchall());


    mycursor.execute("SELECT *from  users ");

    user_based_approach = pd.DataFrame(mycursor.fetchall());

    mycursor.execute("SELECT * from  applicants");
    apps = pd.DataFrame(mycursor.fetchall());

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
    

    return stuff;


@app.route('/stackrec')
@cross_origin(origin="https://quiet-waters-20201.herokuapp.com/")
def recStack():
    randomCity=['losangeles','sanfransico','newyork','miami','london','washington']
    randomElement=random.choice(randomCity)
    feed=feedparser.parse("http://careers.stackoverflow.com/jobs/feed?location="+randomElement)
    entry=sorted(feed.entries[:50], key=lambda x: random.random())
    stackOverflowJobs = []
    for e in entry:
        job = {'title': e.title, 'desc': e.description, 'location': e.location}
        stackOverflowJobs.append(job)
    return jsonify(stackOverflowJobs)






