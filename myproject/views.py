from myproject import app
from flask import render_template
from flask import request

movie_input = ''

@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html')
    
    
@app.route('/', methods = ["POST"])
def value():
    list_of_movies = ['Start Wars', 'Rocky', 'Lord of The Rings']
    movie_input = request.form['movie']
    return render_template('loading.html')
    #return render_template('index.html', movie = 'Rocky', ls = list_of_movies, test = request.form['movie'])
    

@app.route('/loading')
def loading():
    return render_template('loading.html')


    
    


    