from flask import Flask,render_template,url_for,request,Blueprint,flash,current_app,redirect,session,jsonify
from datetime import datetime,timedelta
import sqlite3,time,uuid,mimetypes,base64
search = Blueprint("search",__name__)
@search.route("/search",methods=["POST","GET"])
def sea():
    a = []
    like = ''
    comment = ''
    usernam = session.get("username")
    if not usernam:
        return redirect("/login")
    search = request.args.get("q")
    db = sqlite3.connect("../database/database.db")
    c = db.cursor()
    c.execute(
    "SELECT username, name, file, caption, id, date FROM post WHERE (key LIKE ? OR name LIKE ? OR caption LIKE ?) AND username != ?",
    (f"%{search}%", f"%{search}%", f"%{search}%", usernam)
)

    f = c.fetchall()
    print(f)
    followerr = ''
    for username,name,file,caption,id,date in f:
        print(date)
        c.execute("SELECT follower FROM follow WHERE follower = ? AND username = ?",(usernam,username))
        fol = c.fetchone()
        if fol:
            followerr = "followed"
        else:
            followerr = "follow"    
        c.execute("SELECT comment,like,content FROM setting WHERE username = ?",(username,))
        r = c.fetchone()
        c.execute("SELECT image FROM profile WHERE name = ?",(username,))
        p = c.fetchone()[0]
        c.execute("SELECT postid FROM like WHERE username = ?",(usernam,))
        lik = c.fetchall()
        c.execute("SELECT postid FROM save WHERE username = ?",(usernam,))
        
        sa = c.fetchall()
        if r[2] != "public":
            continue
        if r[0] != "public":
            comment = "hidden"
        
        elif r[0] == "public":    
            c.execute("SELECT COUNT(*) FROM like WHERE postid = ?",(id,))  
            f = c.fetchone()
            if f and f[0]:
                like = int(f[0])
            else:
                like = 0    
        if r[1] == "public":   
            c.execute("SELECT COUNT(*) FROM comment WHERE postid = ?",(id,))
            f = c.fetchone()
            if f and f[0]:
                comment = int(f[0])
            else:
                comment = 0  
        elif r[1] != "public":
            like = "hidden"        
        if lik or sa:
            liked_ids = [row[0] for row in lik] if lik else []
            saved_ids = [row[0] for row in sa] if sa else []

            if id in liked_ids or id in saved_ids:
                pass
            else:
                print(f"date {date}")
                print(id)
                print(username)
                a.append({
                    "profi": p,
                    "username": username,
                    "name": name,
                    "file": file,
                    "caption": caption,
                    "id": id,
                    "like": like,
                    "comment": comment,
                    "date":date 
                })
    c.execute("SELECT image FROM profile WHERE name = ?",(usernam,))
    image = c.fetchone()
    c.execute("SELECT COUNT(*) FROM follow WHERE username = ?",(usernam,))
    followers = c.fetchone()
    for followers in followers:
        follow = followers   
    if image:
        profile = image[0]
    else:
        profile = url_for("static",filename="image/alexander-shatov-PEJtZfT6C1Q-unsplash.jpg")    
    return render_template("dashboard.html",ff=followerr,username=usernam,profile=profile,followers=follow,f=a)