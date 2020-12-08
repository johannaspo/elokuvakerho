from app import app
import login_module, film_module, member_module, loan_module, review_module
from flask import redirect, render_template, request, session, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from forms import LoginForm, AddFilmForm, ReviewForm, AddMemberForm

@app.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form["username"]
        password = request.form["password"]
    
        if login_module.login(username, password):
            return redirect("/")
        else:
            return render_template("index.html", form=form, message="Väärä käyttäjä tai salasana")
    return render_template("index.html", form=form)

@app.route("/logout")
def logout():
    login_module.logout()
    return redirect("/")

@app.route("/films/add_film", methods=["GET", "POST"])
def add_film():
    form = AddFilmForm()
    if form.validate_on_submit():
        name = request.form["name"]
        genre = request.form["genre"]
        release_year = request.form["release_year"]
        description = request.form["description"]
        film_module.add_film(name, genre, release_year, description)
        return render_template("success.html", message="Elokuva lisätty!")
    return render_template("add_film.html", form=form)

@app.route("/films")
def films():
    film_list = film_module.get_film_list()
    return render_template("films.html", films=film_list)

@app.route("/film/<int:id>")
def film(id):
    name = film_module.get_film_name(id)
    genre = film_module.get_film_genre(id)
    release_year = film_module.get_film_release_year(id)
    description = film_module.get_film_description(id)
    checked_out = film_module.get_film_loaned(id)
    return render_template("film.html", id=id, name=name, genre=genre, 
           release_year=release_year, description=description, checked_out=checked_out)
    
@app.route("/films/loan", methods=["POST"])
def loan():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if request.method == "POST":
        id = request.form["loan_film"]
        username = session["username"]
        loan_module.loan(id, username)
        message = "Elokuva varattu! Voit hakea elokuvan kerhotilasta aikaisintaan huomenna klo 12."
        return render_template("success.html", message=message)

@app.route("/film/<int:id>/reviews", methods=["GET", "POST"])
def reviews(id):
    film_name = review_module.get_reviews_film_name(id)
    reviews = review_module.get_reviews(id)
    stats = review_module.get_reviews_stats_message(id)
    form = ReviewForm(film_id = id)
    message = None
    if form.validate_on_submit():
        film_id = request.form["film_id"]
        username = session["username"]
        stars = request.form["stars"]
        text = request.form["text"]
        review_module.post_review(film_id, username, stars, text)
        flash("Arvostelu lähetetty!")
        return redirect(url_for("reviews", id=id))
    return render_template("reviews.html", film_name=film_name, reviews=reviews, id=id, 
           stats=stats, form=form, message=message)
    
@app.route("/member/<username>")
def member(username):
    id = member_module.get_member_id(username)
    name = member_module.get_member_name(username)
    email = member_module.get_member_email(username)
    loans = member_module.get_member_loans(username)
    reviews = member_module.get_member_reviews(username)
    return render_template("member.html", id=id, name=name, username=username, 
           email=email, films=loans, reviews=reviews)

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/members")
def members():
    members = member_module.get_member_list()
    return render_template("members.html", members=members)

@app.route("/members/add_member", methods=["GET", "POST"])
def add_member():
    form = AddMemberForm()
    if form.validate_on_submit():
        name = request.form["name"]
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        email = request.form["email"]
        role = request.form["role"]
        member_module.submit_member(name, username, password, email, role)
        return render_template("success.html", message="Jäsen lisätty!")
    return render_template("add_member.html", form=form)

@app.route("/loans")
def loans():
    films = loan_module.get_loaned_films()
    return render_template("loans.html", films=films)

@app.route("/loans/return_loan", methods=["POST"])
def return_loan():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if request.method == "POST":
        id = request.form["id"]
        loan_module.return_loan(id)
        return redirect(url_for("loans"))