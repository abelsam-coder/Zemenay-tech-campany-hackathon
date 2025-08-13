from flask import make_response,Flask,render_template,request,Blueprint,flash,current_app,redirect,session,url_for
from flask_bcrypt import Bcrypt,generate_password_hash,check_password_hash
from datetime import datetime
import sqlite3,mimetypes,base64,os
signup = Blueprint("signup",__name__)
@signup.route('/signup',methods=["POST","GET"])
@signup.route('/registeration')
def registeration():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        device = request.form["device"]
        date = datetime.now().strftime("%B %A %y")
        bcrypt = current_app.extensions["bcrypt"]
        hashed_password = bcrypt.generate_password_hash(password).decode()
        db = sqlite3.connect("../database/database.db")
        c = db.cursor()
        try:
            with open("../t.txt","r") as m:
                q = m.read()
            c.execute("INSERT INTO authentication (username , email, password, date, device ) VALUES(?,?,?,?,?)",(username,email,hashed_password,date,device))
            c.execute("INSERT INTO setting (content,like,comment,chat,username) VALUES(?,?,?,?,?)",('public','public','public','public',username))
            c.execute("INSERT INTO profile (name,image) VALUES(?,?)",(username,q))
            c.execute("INSERT INTO like (username,postid) VALUES(?,?)",(username,"none"))
            db.commit()
            session["username"] = username
            let = make_response(redirect('/dashboard'))
            let.set_cookie("new","true",max_age=60)
            return let
        except sqlite3.IntegrityError:
            flash("username is taken please use another username","error")
    return render_template("signup.html")        