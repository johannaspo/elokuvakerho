from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new():
    return render_template('new.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        genre = request.form['genre']
        release_year = request.form['release_year']
        description = request.form['description']
        
        if name == '' or genre == '' or release_year == '' or description == '':
            return render_template('new.html', message='Täytä kaikki kentät')
        
        sql = 'INSERT INTO film (name, genre, release_year, description) ' \
              'VALUES (:name, :genre, :release_year, :description)'
        
        db.session.execute(sql, {'name':name, 'genre':genre, 'release_year':release_year, 'description':description})
        db.session.commit()
        return render_template('success.html')