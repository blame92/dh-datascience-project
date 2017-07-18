# -*- coding: utf-8 -*-
from myproject import app
from flask import render_template
from flask import request
import csv
import json
import unicodedata

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii
    
def create_list_of_movies():
    ifile = open("./myproject/static/df_lda_topics.csv", "rb")
    reader = csv.reader(ifile)
    movie_list = []
    for row in reader:
        movie_list.append(row[2])
    ifile.close()
    data = {}
    data['movies'] = movie_list
    with open('movie_list.json', 'w') as outfile:
        json.dump(data, outfile)
    
def get_movie_link(movie_id,movie_name):
    link = "http://www.cinemargentino.com/films/"
    link_id = link + movie_id + "-"
    m = movie_name.replace(" ", "-")
    return link_id + m
    
def create_movie_json(movie_rec, original):
    data = {}
    data['list'] = movie_rec
    data['original'] = original
    with open('movie.json', 'w') as outfile:
        json.dump(data, outfile)

def looking_for_topic(movie):
        ifile = open("./myproject/static/df_lda_topics.csv", "rb")
        reader = csv.reader(ifile)
        recommended_list = []
        topic_number = -1;
        for row in reader:
            try:
                if movie == remove_accents(row[2].decode('utf-8')):
                    
                    topic_number = row[4]
                    break;
            except Exception as e:
                print e
        
        for row in reader:
            recommended_movie = {}
            if topic_number == row[4]:
                recommended_movie['name'] = row[2]
                recommended_movie['id'] = row[0]
                recommended_movie['topic'] = row[4]
                recommended_movie['link'] = get_movie_link(row[0],row[2])
                recommended_list.append(recommended_movie)
                
        ifile.close()
        create_movie_json(recommended_list,movie)
        print len(recommended_list)
        return recommended_list
    

def read_recommendations():
    with open('movie.json', 'r') as movie_recom:
        movies = json.load(movie_recom)
    print movies
    return movies

############################################# app.route ###########################################
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    
    
@app.route('/loading', methods = ["POST"])
def value():
    movie_input = request.form['movie']
    cluster = looking_for_topic(movie_input)
    return render_template('loading.html', movie = movie_input)
    

@app.route('/loading')
def loading():
    return render_template('loading.html')
    
@app.route('/topics')
def topics():
    return render_template('lda.html')
    


@app.route('/results', methods = ["GET","POST"])
def results():
    recommended_m = read_recommendations()
    return render_template('results.html', recommendations1 = unicodedata.normalize('NFKD', recommended_m['list'][0]['name']).encode('ascii','ignore'),
    recommendations2 = unicodedata.normalize('NFKD', recommended_m['list'][1]['name']).encode('ascii','ignore'), 
    recommendations3 = unicodedata.normalize('NFKD', recommended_m['list'][2]['name']).encode('ascii','ignore'), original = recommended_m['original'],
    cinema_link1 = recommended_m['list'][0]['link'], cinema_link2 = recommended_m['list'][1]['link'], cinema_link3 = recommended_m['list'][2]['link'])




