from db import db

def get_member_name(username):
    sql = "SELECT name FROM members WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    return result.fetchone()[0]

def get_member_email(username):
    sql = "SELECT email FROM members WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    return result.fetchone()[0]

def get_member_id(username):
    sql = "SELECT id FROM members WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    return result.fetchone()[0]

def get_member_loans(username):
    member_id = get_member_id(username)
    sql = "SELECT name, release_year FROM films WHERE member_id=:member_id "
    result = db.session.execute(sql, {"member_id":member_id})
    return result.fetchall()

def get_member_list():
    sql = "SELECT username FROM members ORDER BY name ASC"
    result = db.session.execute(sql)
    return result.fetchall()

def submit_member(name, username, password, email, role):
    sql = "INSERT INTO members (name, username, password, email, role) " \
              "VALUES (:name, :username, :password, :email, :role)"
    db.session.execute(sql, {"name":name, "username":username, "password":password, "email":email, "role":role})
    db.session.commit()

def duplicate_member(username):
    sql = "SELECT username FROM members"
    result = db.session.execute(sql)
    if (result.fetchone[0] == None):
        return false