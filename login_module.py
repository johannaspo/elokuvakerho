from db import db
from werkzeug.security import check_password_hash
from flask import session
import os

def login(username, password):
    sql = "SELECT password FROM members WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if user == None:
        return False
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            session["show_admin"] = False
            session["username"] = username
            session["csrf_token"] = os.urandom(16).hex()
            sql = "SELECT role FROM members WHERE username=:username"
            result = db.session.execute(sql, {"username":username})
            role = result.fetchone()[0]
            if role == "admin":
                session["show_admin"] = True
            return True
        else:
            return False

def logout():
    del session["username"]
    session["show_admin"] = False