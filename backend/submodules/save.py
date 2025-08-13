from flask import Flask,render_template,request,Blueprint,flash,current_app,redirect,session,jsonify
from datetime import datetime,timedelta
import sqlite3,time
save = Blueprint("save",__name__)
@save.route('/save/<string:id>',methods=["GET"])
def sa(id):
    username = session.get("username")
    db = sqlite3.connect("../database/database.db")
    c = db.cursor()
    
    c.execute("SELECT * FROM save WHERE username = ? AND postid = ?",(username,id))
    f = c.fetchone()
    if f:
        c.execute("DELETE FROM save WHERE username = ? AND postid = ?",(username,id))
        db.commit()
    else:
        c.execute("INSERT INTO save (username,postid) VALUES(?,?)",(username,id))
        db.commit()
    return jsonify({"saved":id})
