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

@app.route('/movies')
def movies():
    sql = "SELECT id, name, release_year FROM film ORDER BY name ASC"
    result = db.session.execute(sql)
    movies = result.fetchall()
    return render_template("movies.html", movies=movies)

@app.route("/movie/<int:id>")
def movie(id):
    sql = "SELECT name FROM film WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    name = result.fetchone()[0]
    sql = "SELECT genre FROM film WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    genre = result.fetchone()[0]
    sql = "SELECT release_year FROM film WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    release_year = result.fetchone()[0]
    sql = "SELECT description FROM film WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    description = result.fetchone()[0]
    sql = "SELECT member_id FROM film WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    if result.fetchone()[0] == None:
        available = 'Ei'
        button = 'yes'
        return render_template("movie.html", id=id, name=name, genre=genre, release_year=release_year, description=description, available=available, button=button)
    else:
        available = 'Kyllä'
        return render_template("movie.html", id=id, name=name, genre=genre, release_year=release_year, description=description, available=available)

@app.route('/movie/<int:id>/loan', methods=['POST'])
def loan(id):
    if request.method == 'POST':
        
        username = session['username']
        sql = 'UPDATE film SET (member_id) = (SELECT id FROM member WHERE username =:username) WHERE id =:id'
        db.session.execute(sql, {"username":username, "id":id})
        db.session.commit()
        return render_template('reservation.html')
    
@app.route("/member/<username>")
def member(username):
    sql = "SELECT name FROM member WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    name = result.fetchone()[0]
    sql = "SELECT email FROM member WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    email = result.fetchone()[0]
    sql = "SELECT id FROM member WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    id = result.fetchone()[0]
    sql = "SELECT name FROM film WHERE member_id=:id "
    result = db.session.execute(sql, {"id":id})
    movies = result.fetchall()
    return render_template("member.html", id=id, name=name, username=username, email=email, movies=movies)