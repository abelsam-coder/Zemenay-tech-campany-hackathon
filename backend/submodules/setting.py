from flask import Flask,render_template,request,Blueprint,flash,current_app,redirect,session,jsonify
from datetime import datetime,timedelta
import sqlite3,time
conset = Blueprint("conset",__name__)
@conset.route('/setting/content/privacy',methods=["POST","GET"])
def config():
    username = session.get("username")
    if request.method == "POST":
        content = request.form["privacy"]
        db = sqlite3.connect("database/database.db")
        c = db.cursor()
        c.execute("UPDATE setting SET content = ? WHERE username = ?",(content,username))
        db.commit()
    return render_template("setting.html")    
@conset.route('/setting/content/like',methods=["POST","GET"])
def confi():
    username = session.get("username")
    if request.method == "POST":
        content = request.form["privacy"]
        db = sqlite3.connect("database/database.db")
        c = db.cursor()
        c.execute("UPDATE setting SET like = ? WHERE username = ?",(content,username))
        db.commit()
    return render_template("settinglike.html")  
@conset.route('/setting/content/comment',methods=["POST","GET"])
def conf():
    username = session.get("username")
    if request.method == "POST":
        content = request.form["privacy"]
        db = sqlite3.connect("database/database.db")
        c = db.cursor()
        c.execute("UPDATE setting SET comment = ? WHERE username = ?",(content,username))
        db.commit()
    return render_template("settingcomment.html")  
@conset.route('/setting/chat/privacy',methods=["POST","GET"])
def con():
    username = session.get("username")
    if request.method == "POST":
        content = request.form["privacy"]
        db = sqlite3.connect("database/database.db")
        c = db.cursor()
        c.execute("UPDATE setting SET chat = ? WHERE username = ?",(content,username))
        db.commit()

    return render_template("settingchat.html")  
