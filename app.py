from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
   
    sql = "SELECT password FROM members WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if user == None:
        return render_template("index.html", message="Käyttäjää ei löydy")
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            session["show_admin"] = False
            session["username"] = username
            sql = "SELECT role FROM members WHERE username=:username"
            result = db.session.execute(sql, {"username":username})
            role = result.fetchone()[0]
            
            if role == "admin":
                session["show_admin"] = True
            return redirect("/")
        else:
            return render_template("index.html", message="Väärä salasana")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/add_film")
def add_film():
    return render_template("add_film.html")

@app.route("/submit_film", methods=["POST"])
def submit_film():
    if request.method == "POST":
        name = request.form["name"]
        genre = request.form["genre"]
        release_year = request.form["release_year"]
        description = request.form["description"]
        
        if name == "" or genre == "" or release_year == "" or description == "":
            return render_template("add_film.html", message="Täytä kaikki kentät")
        
        sql = "INSERT INTO films (name, genre, release_year, description) " \
              "VALUES (:name, :genre, :release_year, :description)"
        
        db.session.execute(sql, {"name":name, "genre":genre, "release_year":release_year, "description":description})
        db.session.commit()
        message = "Elokuva lisätty!"
        return render_template("success.html", message=message)

@app.route("/films")
def films():
    sql = "SELECT id, name, release_year FROM films ORDER BY name ASC"
    result = db.session.execute(sql)
    films = result.fetchall()
    return render_template("films.html", films=films)

@app.route("/film/<int:id>")
def film(id):
    sql = "SELECT name FROM films WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    name = result.fetchone()[0]
    sql = "SELECT genre FROM films WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    genre = result.fetchone()[0]
    sql = "SELECT release_year FROM films WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    release_year = result.fetchone()[0]
    sql = "SELECT description FROM films WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    description = result.fetchone()[0]
    sql = "SELECT member_id FROM films WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    if result.fetchone()[0] == None:
        checked_out = "Ei"
        return render_template("film.html", id=id, name=name, genre=genre, release_year=release_year, description=description, checked_out=checked_out)
    else:
        checked_out = "Kyllä"
        return render_template("film.html", id=id, name=name, genre=genre, release_year=release_year, description=description, checked_out=checked_out)

@app.route("/loan", methods=["POST"])
def loan():
    if request.method == "POST":
        id = request.form["loan_film"]
        username = session["username"]
        sql = "UPDATE films SET (member_id) = (SELECT id FROM members WHERE username =:username) WHERE id=:id"
        db.session.execute(sql, {"username":username, "id":id})
        db.session.commit()
        message = "Elokuva varattu! Voit hakea elokuvan kerhotilasta aikaisintaan huomenna klo 12."
        return render_template("success.html", message=message)

@app.route("/film/<int:id>/reviews")
def reviews(id):
    sql = "SELECT name FROM films WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    name = result.fetchone()[0]
    sql = "SELECT TO_CHAR(timestamp, 'DD/MM/YYYY HH24.MI') as date, username, stars, text FROM reviews WHERE film_id=:id ORDER BY timestamp DESC"
    result = db.session.execute(sql, {"id":id})
    reviews = result.fetchall()
    sql = "SELECT COUNT(stars) FROM reviews WHERE film_id=:id"
    result = db.session.execute(sql, {"id":id})
    reviews_count = result.fetchone()[0]
    if reviews_count == 0:
        message = "Ei arvosteluita"
    else:
        sql = "SELECT AVG(stars)::numeric(10,2) FROM reviews WHERE film_id=:id"
        result = db.session.execute(sql, {"id":id})
        reviews_average = result.fetchone()[0]
        message = str(reviews_count) + " arvostelua, joiden keskiarvo on " + str(reviews_average)
    return render_template("reviews.html", name=name, reviews=reviews, id=id, message=message)

@app.route("/review_film", methods=["POST"])
def review_film():
    if request.method == "POST":
        film_id = request.form["film_id"]
        username = session["username"]
        stars = request.form["stars"]
        text = request.form["text"]
         
        sql = "INSERT INTO reviews (film_id, username, stars, text) " \
              "VALUES (:film_id, :username, :stars, :text)"
        
        db.session.execute(sql, {"film_id":film_id, "username":username, "stars":stars, "text":text})
        db.session.commit()
        return redirect(url_for("reviews",id=film_id))
    
@app.route("/member/<username>")
def member(username):
    sql = "SELECT name FROM members WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    name = result.fetchone()[0]
    sql = "SELECT email FROM members WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    email = result.fetchone()[0]
    sql = "SELECT id FROM members WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    id = result.fetchone()[0]
    sql = "SELECT name, release_year FROM films WHERE member_id=:id "
    result = db.session.execute(sql, {"id":id})
    films = result.fetchall()
    return render_template("member.html", id=id, name=name, username=username, email=email, films=films)

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/members")
def members():
    sql = "SELECT username FROM members ORDER BY name ASC"
    result = db.session.execute(sql)
    members = result.fetchall()
    return render_template("members.html", members=members)

@app.route("/add_member")
def add():
    return render_template("add_member.html")

@app.route("/submit_member", methods=["POST"])
def submit_member():
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        email = request.form["email"]
        role = request.form["role"]
        
        if name == "" or username == "" or password == "" or email == "" or role == "":
            return render_template("add_member.html", message="Täytä kaikki kentät")
        
        sql = "INSERT INTO members (name, username, password, email, role) " \
              "VALUES (:name, :username, :password, :email, :role)"
        
        db.session.execute(sql, {"name":name, "username":username, "password":password, "email":email, "role":role})
        db.session.commit()
        message = "Jäsen lisätty!"
        return render_template("success.html", message=message)

@app.route("/loans")
def loans():
    sql = "SELECT id, name, release_year FROM films WHERE member_id IS NOT NULL ORDER BY name ASC"
    result = db.session.execute(sql)
    films = result.fetchall()
    return render_template("loans.html", films=films)

@app.route("/return_loan", methods=["POST"])
def return_loan():
    if request.method == "POST":
        id = request.form["id"]
        sql = "UPDATE films SET member_id = NULL WHERE id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
        return redirect("loans")