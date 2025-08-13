from flask import Flask,render_template,url_for,request,Blueprint,flash,current_app,redirect,session,jsonify
from datetime import datetime,timedelta
import sqlite3,time,uuid,mimetypes,base64

comment = Blueprint("comment",__name__)
aa = []

# comment

@comment.route('/comment/<string:id>', methods=["POST", "GET"])
def commentfunction(id):
    
    database = sqlite3.connect("database/database.db")
    cursor = database.cursor()
    username = session.get("username")

    # Get post details
    
    cursor.execute("SELECT username, name, file, caption, id FROM post WHERE id = ?", (id,))
    list = cursor.fetchone()
    cursor.execute("SELECT image FROM profile WHERE name = ?",(list[0],))
    im = cursor.fetchone()
    if im:
        imagg = im[0]
    else:
        imagg = url_for("static",filename="image/alexander-shatov-PEJtZfT6C1Q-unsplash.jpg")    
    # Get all comments related to the post
    cursor.execute("SELECT name, comment,messageid,date FROM comment WHERE postid = ?", (id,))
    comments = cursor.fetchall()

    # Clear aa list before repopulating
    aa.clear()

    for commenter, comment_text,messageid,date in comments:
        print(commenter)
        cursor.execute("SELECT image FROM profile WHERE name = ?", (commenter,))
        t = cursor.fetchone()
        print(username)
        profile_img = t[0] if t else url_for("static",filename="image/Copilot_20250804_013440.png")
        if commenter == username:
            aa.append({
                "commenter":username,
                "comment":comment_text,
                "messageid":messageid,
                "im":t[0],
                "date":date,
                "edit":True,
                "delete":True
            })  
        else:
            aa.append({
                "commenter":commenter,
                "date":date,
                "im":t[0],
                "messageid":messageid,
                "comment":comment_text
            })        

    # Handle comment submission
    if request.method == "POST":
        message = request.form["message"]
        
        idd = str(uuid.uuid4())
        cursor.execute("SELECT username FROM post WHERE id = ?", (id,))
        f = cursor.fetchone()[0]
        date = datetime.now().strftime("%B %A %y")
        cursor.execute("INSERT INTO comment (postid, username, name, comment, messageid,date) VALUES (?, ?, ?, ?, ?,?)",
                  (id, f, username, message, idd,date))
        database.commit()
        return redirect(f"/comment/{id}") 

    return render_template("comment.html",op=imagg, username=list[0],name=list[1],file=list[2],caption=list[3],comment=aa)
   
@comment.route('/comment/edit/<string:id>',methods=["POST","GET"]) 
def uytf(id):
    username = session.get("username")
    database = sqlite3.connect("database/database.db")
    cursor = database.cursor()
    cursor.execute("SELECT postid FROM comment WHERE messageid = ?",(id,))
    f = cursor.fetchone()[0]
    if request.method == "POST":
        message = request.form["message"]       
        cursor.execute("UPDATE comment SET comment = ? WHERE messageid = ? and name = ?",(message,id,username))
        database.commit()
        flash("edited")
    return render_template("edit.html",f=f)    
@comment.route('/comment/delete/<string:id>',methods=["POST","GET"]) 
def delete(id):
    print("will")
    username = session.get("username")
    database = sqlite3.connect("database/database.db")
    cursor = database.cursor()
    cursor.execute("SELECT postid FROM comment WHERE messageid = ?",(id,))
    f = cursor.fetchone()[0]
    print(f)
    cursor.execute("DELETE FROM comment WHERE name = ? AND messageid = ?",(username,id))
    database.commit()       

    return redirect(f'/comment/{f}')
