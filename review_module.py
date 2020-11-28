from db import db

def get_reviews_film_name(id):
    sql = "SELECT name FROM films WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def get_reviews(id):
    sql = "SELECT TO_CHAR(timestamp, 'DD/MM/YYYY') as date, username, stars, text " \
          "FROM reviews WHERE film_id=:id ORDER BY timestamp DESC"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def get_reviews_stats_message(id):
    sql = "SELECT COUNT(stars) FROM reviews WHERE film_id=:id"
    result = db.session.execute(sql, {"id":id})
    reviews_count = result.fetchone()[0]
    if reviews_count == 0:
        return "Ei arvosteluita"
    else:
        sql = "SELECT AVG(stars)::numeric(10,2) FROM reviews WHERE film_id=:id"
        result = db.session.execute(sql, {"id":id})
        reviews_average = result.fetchone()[0]
        return str(reviews_count) + " arvostelua, joiden keskiarvo on " + str(reviews_average)

def post_review(film_id, username, stars, text):
    sql = "INSERT INTO reviews (film_id, username, stars, text) " \
              "VALUES (:film_id, :username, :stars, :text)"
        
    db.session.execute(sql, {"film_id":film_id, "username":username, "stars":stars, "text":text})
    db.session.commit()
