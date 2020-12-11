from flask_wtf import FlaskForm
import member_module
from db import db
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, SubmitField, RadioField, HiddenField, SelectField
from wtforms.validators import DataRequired, NumberRange, EqualTo, Email, Length, ValidationError

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(message="Tunnus vaaditaan")])
    password = PasswordField("password", validators=[DataRequired(message="Salasana vaaditaan")])
    submit = SubmitField("Kirjaudu")

class AddFilmForm(FlaskForm):
    name = StringField("name", validators=[DataRequired(message="Nimi vaaditaan")])
    genre = SelectField("genre", choices=[], validators=[DataRequired(message="Genre vaaditaan")])
    release_year = IntegerField("release_year", validators=[DataRequired(message="Julkaisuvuosi vaaditaan numerona"), 
        NumberRange(min=0, message="Vuosiluvuon on oltava positiivinen")])
    description = TextAreaField("description", validators=[DataRequired(message="Kuvaus vaaditaan")])
    submit = SubmitField("Lisää elokuva")

def validate_stars(form, stars):
    stars = int(form.stars.data)
    if stars < 1 or stars > 5:
        raise ValidationError()

class ReviewForm(FlaskForm):
    stars = RadioField("stars", choices=[(1,1),(2,2),(3,3),(4,4),(5,5)], default=1, validators=[DataRequired(),
        validate_stars])
    text = TextAreaField("text")
    film_id = HiddenField("film_id")
    submit = SubmitField("Lähetä")

def validate_username(form, member):
    username = form.username.data 
    sql = "SELECT id FROM members WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user != None:
        raise ValidationError("Käyttäjänimi on jo käytössä")

class AddMemberForm(FlaskForm):
    name = StringField("name", validators=[DataRequired(message="Nimi vaaditaan")])
    username = StringField("username", validators=[DataRequired(message="Käyttäjänimi vaaditaan"),
        Length(min=4, message="Käyttäjänimen on oltava vähintään 4 merkkiä pitkä"),
        validate_username]) 
    password = PasswordField("password", validators=[
        DataRequired(message="Salasana vaaditaan"), 
        Length(min=5, message="Salasanan on oltava vähintään 5 merkkiä pitkä"),
        EqualTo("confirm_password", message="Salasanat eivät täsmää")])
    confirm_password = PasswordField("confirmPassword", validators=[DataRequired(message="Salasanojen on täsmättävä")])
    email = StringField("email", validators=[DataRequired(message="Sähköposti vaaditaan"), Email("Anna sähköposti oikeassa muodossa")])
    role = RadioField("admin", choices=[("user","Ei"),("admin","Kyllä")], default="user", validators=[DataRequired()])
    submit = SubmitField("Lisää jäsen")

    