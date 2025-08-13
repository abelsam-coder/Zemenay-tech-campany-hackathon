from flask import Flask,render_template,request,Blueprint,flash,current_app,redirect,session,jsonify
from datetime import datetime,timedelta
import sqlite3,time
users = Blueprint("users",__name__)
@users.route('/users',methods=["POST","GET"])
def user():
    username = session.get("username")
    if not username:
        return redirect('/signup')
    db = sqlite3.connect("database/database.db")
    c = db.cursor()
    c.execute("SELECT * FROM another WHERE username = ?",(username,))
    f = c.fetchall()
    return render_template("users.html",users=f)
@users.route('/users/kickout/<string:device>',methods=["POST","GET"])
def kickout(device):
    username = session.get("username")
    if not username:
        return redirect('/signup')
    db = sqlite3.connect("database/database.db")
    c = db.cursor()
    c.execute("INSERT INTO kickout (username,device) VALUES(?,?)",(username,device))
    db.commit()
    c.execute("SELECT * FROM another WHERE username = ?",(username,))
    f = c.fetchall()

    return render_template("users.html",users=f)    
