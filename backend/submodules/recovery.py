from flask import Flask,render_template,request,Blueprint,flash,current_app,redirect,session,jsonify
from datetime import datetime,timedelta
import sqlite3,time
recovery = Blueprint("recovery",__name__)
@recovery.route('/recovery/email',methods=["POST","GET"])
def reco():
    username = session.get("username")
    if not username:
        return redirect('/signup')
    if request.method == "POST":
        email = request.form["email"]
        db = sqlite3.connect("database/database.db")
        c = db.cursor()
        c.execute("INSERT INTO recovery (username,email) VALUES(?,?)",(username,email))
        db.commit()
        flash("stored successfully")
    return render_template("email.html")    
@recovery.route('/recovery/word',methods=["POST","GET"])
def reco():
    username = session.get("username")
    if not username:
        return redirect('/signup')
    if request.method == "POST":
        word = request.form["word"]
        db = sqlite3.connect("database/database.db")
        c = db.cursor()
        c.execute("INSERT INTO recovery (username,email) VALUES(?,?)",(username,word))
        db.commit()
        flash("stored successfully")        

    return render_template("word.html")    
