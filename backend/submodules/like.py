from flask import Flask,render_template,request,Blueprint,flash,current_app,redirect,session,jsonify
from datetime import datetime,timedelta
import sqlite3,time
like = Blueprint("like",__name__)
@like.route('/like/<string:id>',methods=["GET"])
def sa(id):
    print(id)
    username = session.get("username")
    db = sqlite3.connect("../database/database.db")
    c = db.cursor()
    c.execute("SELECT * FROM like WHERE username = ? AND postid = ?",(username,id))
    f = c.fetchone()
    if f:
        c.execute("DELETE FROM like WHERE username = ? AND postid = ?",(username,id))
        db.commit()
    else:    
        c.execute("INSERT INTO like (username,postid) VALUES(?,?)",(username,id))
        db.commit()
    return jsonify({"liked":id})
