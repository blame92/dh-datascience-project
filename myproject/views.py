# -*- coding: utf-8 -*-
from myproject import app
from flask import render_template
from flask import request
import csv

def looking_for_cluster(movie):
    try:
        ifile = open("./myproject/static/movie_clusterID.csv", "rb")
        reader = csv.reader(ifile)
        test_list = ['hola']
        for row in reader:
            if movie in row[3]:
                print movie
                test_list.append(row[6])
                
        ifile.close()
        return test_list
    except:
        print test_list
 

############################################# app.route ###########################################
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    
    
@app.route('/loading', methods = ["POST"])
def value():
    movie_input = request.form['movie']
    cluster = looking_for_cluster(movie_input)
    return render_template('loading.html', movie = movie_input)
    

@app.route('/loading')
def loading():
    return render_template('loading.html')
    
@app.route('/topics')
def topics():
    return render_template('lda.html')
    


@app.route('/results', methods = ["GET","POST"])
def results():
    return render_template('results.html')



