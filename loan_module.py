from db import db

def get_loaned_films():
    sql = "SELECT F.id, F.name, F.release_year, M.username " \
          "FROM films F, members M WHERE F.member_id = M.id ORDER BY F.name ASC"
    result = db.session.execute(sql)
    return result.fetchall()

def return_loan(id):
    sql = "UPDATE films SET member_id = NULL WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()


def loan(id, username):
    sql = "UPDATE films SET (member_id) = (SELECT id FROM members " \
          "WHERE username =:username) WHERE id=:id"
    db.session.execute(sql, {"username":username, "id":id})
    db.session.commit()