import numpy as np
import pandas as pd
import mysql.connector
from flask_cors import CORS,cross_origin
import matplotlib.pyplot as plt
import seaborn as sns
import random
import re, cgi
from sklearn.utils import shuffle
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




#@app.route('/recommendations/<int:user_id>')
def jobRec():
   

    mydb = mysql.connector.connect(host="35.238.104.188",user="root",passwd="root",port=3306, db='680'
                               )

    mycursor = mydb.cursor()

    # get jobs 

    mycursor.execute("SELECT * FROM jobs")


    #jobs users can get recommendatiosn
    jobs = pd.DataFrame(mycursor.fetchall());


    mycursor.execute("SELECT *from  users_ml ");

    user_based_approach = pd.DataFrame(mycursor.fetchall());

    mycursor.execute("SELECT * from  applicants");
    apps = pd.DataFrame(mycursor.fetchall());
    
    
    #find jobs that are similar
    jobs['Title'] = jobs[7].fillna('')
    TAG_RE = re.compile(r'<[^>]+>')
    jobs[2] = TAG_RE.sub('', str(jobs[2]))
    #jobs_US_base_line['Requirements'] = jobs_US_base_line['Requirements'].fillna('')
    jobs[2] = jobs[7] + jobs[2]
    tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(jobs[2])
    cosine_sim = linear_kernel(tfidf_matrix)
   
    cosine_sim[0]

    jobs=jobs.reset_index();
    
    #indice of jobs

    indices = pd.Series(jobs.index,index=jobs['Title'])
    
    title='Maintenance Tech';
    
    if title not in indices:
        a=recStack();
        print(a);
    else:

        idx = indices[title]
        
        sim_scores = list(enumerate(cosine_sim[idx]))
        
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        job_indices = [i[0] for i in sim_scores]
        
        print("Similar jobs based on the job you picked\n")
        
        print(jobs[7].iloc[job_indices].head(10))
        
        user_based_approach[7]=user_based_approach[7].fillna('');
        
        user_based_approach[8]=user_based_approach[8].fillna('');
        
        user_based_approach[11]=str(user_based_approach[11].fillna(''));
     
        user_based_approach[7]=user_based_approach[8]+ user_based_approach[11] +  user_based_approach[7];
        
        tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
        
        tfidf_matrix = tf.fit_transform(user_based_approach[7])

        cosine_sim = linear_kernel(tfidf_matrix)
        
        user_based_approach = user_based_approach.reset_index()
        
        userid = user_based_approach[0]
        
        indices = pd.Series(user_based_approach.index, index=user_based_approach[4])
        
        #user_id, replace but eventnually needs to be a parameter for function
        idx = indices[1]

        sim_scores = list(enumerate(cosine_sim[idx]))

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        user_indices = [i[0] for i in sim_scores]
        
        jobs_userwise = apps[4].isin(user_indices) #
        
        df1 = pd.DataFrame(data = apps[3])
        
        joblist = df1[3].tolist()

        check_user=user_based_approach[user_based_approach.index == 1]

        Job_list = jobs[0].isin(joblist)
        
        results=pd.DataFrame(data=jobs[Job_list])
        
        
        
        
        
        if len(check_user[3]) >0 and len(results)==0:
        
        
        
            feed=feedparser.parse("http://careers.stackoverflow.com/jobs/feed?location="+check_user[3])
            entry=sorted(feed.entries[:50], key=lambda x: random.random())
            stackOverflowJobs = []
            for e in entry:
                job = {'title': e.title, 'desc': e.description, 'location': e.location}
                stackOverflowJobs.append(job)
                print(stackOverflowJobs)


        if len(results)==0 and len(check_user[3])==0:
                recStack()
                    
        else:
        
            print("recommendations based on your profile")
            print(results.sample(frac=1).head(20))



        return;
def recStack():
    randomCity=['losangeles','sanfransico','newyork','miami','london','washington']
    randomElement=random.choice(randomCity)
    feed=feedparser.parse("http://careers.stackoverflow.com/jobs/feed?location="+randomElement)
    entry=sorted(feed.entries[:50], key=lambda x: random.random())
    stackOverflowJobs = []
    for e in entry:
        job = {'title': e.title, 'desc': e.description, 'location': e.location}
        stackOverflowJobs.append(job)
        return stackOverflowJobs;


def shuffle(df, n=1, axis=0):
    df = df.copy()
    for _ in range(n):
            df.apply(np.random.shuffle, axis=axis)
            return df

print(jobRec())
