from flask import Flask,render_template,abort,request,Blueprint,flash,current_app,redirect,session,jsonify,url_for
from datetime import datetime,timedelta
import sqlite3,time
dash = Blueprint("dash",__name__)
l = 0
@dash.route('/dashboard')
def hom():
    global l
    a = []
    usernam = session.get("username")
    if not usernam:
        return redirect('/login')
    comment = ''
    like = ''
    db = sqlite3.connect("database/database.db")
    c = db.cursor()
    new = request.cookies.get("new")
    if new:
        n = "true"
    else:
        n = "false"  
    c.execute("SELECT image FROM profile WHERE name = ?",(usernam,))
    image = c.fetchone()
    if image:
        profil = image[0]
    else:
       profil =  url_for("static",filename="image/alexander-shatov-PEJtZfT6C1Q-unsplash.jpg")
    c.execute("SELECT COUNT(*) FROM follow WHERE username = ?",(usernam,))
    followers = c.fetchone()
    for followers in followers:
        follow = followers   
    c.execute("SELECT username,name,file,caption,id,date FROM post WHERE username != ? ORDER BY RANDOM()", (usernam,))
    f = c.fetchall()
    followerr = ''
    l += 1
    for username,name,file,caption,id,date in f:
        print(username,name,caption)
        c.execute("SELECT follower FROM follow WHERE follower = ? AND username = ?",(usernam,username))
        fol = c.fetchone()
        print(f"n {fol}")
        if fol:
            followerr = "followed"
        else:
            followerr = "follow"    
        c.execute("SELECT comment,like,content FROM setting WHERE username = ?",(username,))
        r = c.fetchone()
        c.execute("SELECT image FROM profile WHERE name = ?",(username,))
        image = c.fetchone()
        if image:
            p = image[0]
        else:    
            p=  url_for("static",filename="image/alexander-shatov-PEJtZfT6C1Q-unsplash.jpg")
        c.execute("SELECT postid FROM like WHERE username = ?",(usernam,))
        lik = c.fetchall()
        print(f"iuviucvigcy {lik}")
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
        print(comment)
        print(like)        
        if lik or sa:
            liked_ids = [row[0] for row in lik] if lik else []
            saved_ids = [row[0] for row in sa] if sa else []

            if id in liked_ids or id in saved_ids:
                pass
            else:
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
                    "comment": comment ,
                    "date":date
                })
   
    return render_template("dashboard.html",f=a,profile=profil,username=usernam,followers=follow,ff=followerr,new=n)     












