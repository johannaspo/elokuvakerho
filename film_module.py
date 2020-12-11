from db import db

def add_film(name, release_year, description):
        sql = "INSERT INTO films (name, release_year, description) " \
              "VALUES (:name, :release_year, :description)" \
              "RETURNING id"
        result = db.session.execute(sql, {"name":name, "release_year":release_year, "description":description})
        db.session.commit()
        return result.fetchone()[0]

def add_film_genre(film_id, genre_id):
    sql = "INSERT INTO films_genres (film_id, genre_id) " \
              "VALUES (:film_id, :genre_id)"
    db.session.execute(sql, {"film_id":film_id, "genre_id":genre_id})
    db.session.commit()

def get_film_list():
    sql = "SELECT id, name, release_year FROM films ORDER BY name ASC"
    result = db.session.execute(sql)
    return result.fetchall()

def get_film_name(id):
    sql = "SELECT name FROM films WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def get_film_genre(film_id):
    sql = "SELECT genre FROM genres WHERE id = (SELECT genre_id FROM films_genres WHERE film_id=:film_id)"
    result = db.session.execute(sql, {"film_id":film_id})
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

def get_genres():
    sql = "SELECT id, genre FROM genres ORDER BY genre ASC"
    result = db.session.execute(sql)
    return result.fetchall()