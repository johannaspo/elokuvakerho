from db import db

def add_film(name, genre, release_year, description):
        sql = "INSERT INTO films (name, genre, release_year, description) " \
              "VALUES (:name, :genre, :release_year, :description)"
        db.session.execute(sql, {"name":name, "genre":genre, "release_year":release_year, "description":description})
        db.session.commit()

def get_film_list():
    sql = "SELECT id, name, release_year FROM films ORDER BY name ASC"
    result = db.session.execute(sql)
    return result.fetchall()

def get_film_name(id):
    sql = "SELECT name FROM films WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def get_film_genre(id):
    sql = "SELECT genre FROM films WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def get_film_release_year(id):
    sql = "SELECT release_year FROM films WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def get_film_description(id):
    sql = "SELECT description FROM films WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def get_film_loaned(id):
    sql = "SELECT member_id FROM films WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    if result.fetchone()[0] == None:
        return "Ei"
    else:
        return "Kyllä"