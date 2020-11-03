from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

""" hash_value = generate_password_hash('password')
sql = "INSERT INTO member (username, password) VALUES (:username, :password)"
db.session.execute(sql, {"username":'username', "password":hash_value})
db.session.commit() """

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
   
    sql = "SELECT password FROM member WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if user == None:
        return render_template('index.html', message='Käyttäjää ei löydy')
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            session["username"] = username
            return redirect('/')
        else:
            return render_template('index.html', message='Väärä salasana')

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

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