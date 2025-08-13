from flask import Flask,render_template,request,Blueprint,flash,current_app,redirect,session,jsonify
from datetime import datetime,timedelta
import sqlite3,time
follow = Blueprint("follow",__name__)
@follow.route('/follow/<string:username>')
def fol(username):
    name = session.get("username")
    db = sqlite3.connect("../database/database.db")
    c = db.cursor()
    c.execute("INSERT INTO follow (username,follower) VALUES(?,?)",(username,name))
    db.commit()
    return redirect('/')
@follow.route('/unfollow/<string:username>')
def unfollow(username):
    name = session.get("username")
    db = sqlite3.connect("../database/database.db")
    c = db.cursor()
    c.execute("DELETE FROM follow WHERE username = ? AND follower = ?",(username,name))   
    db.commit() 
    return redirect('/')