from flask import Flask,render_template,url_for,request,Blueprint,flash,current_app,redirect,session,jsonify
from datetime import datetime,timedelta
import sqlite3,time,base64,mimetypes
profile = Blueprint("profile",__name__)
@profile.route('/profile',methods=["POST","GET"])
def p():
    lis = []
    db = sqlite3.connect("../database/database.db")
    c = db.cursor()
    username = session.get("username")
    c.execute("SELECT image FROM profile WHERE name = ?",(username,))
    image = c.fetchone()
    c.execute("SELECT COUNT(*) FROM post WHERE username = ?",(username,))
    imag = c.fetchone()
    c.execute("SELECT file,name,caption,id FROM post WHERE username = ?",(username,))
    pos = c.fetchall()
    for file,name,caption,id in pos:
        print(name)
        c.execute("SELECT COUNT(*) FROM like WHERE postid = ?",(id,))
        li = c.fetchone()
        if li:
            like = li[0]
        else:
            like = 0    
        c.execute("SELECT COUNT(*) FROM comment WHERE postid = ?",(id,))
        co = c.fetchone()
        tr = "true"
        if co:
            comment = co[0]
        else:
            comment = 0    
        lis.append({
                "file":file,
                "name":name,
                "id":id,
                "caption":caption,
                "like":like,
                "comment":comment,
                "tr":tr
            })       
    if imag:
        for imag in imag:
            n = imag
            
    c.execute("SELECT COUNT(*) FROM follow WHERE username = ?",(username,))
    fol = c.fetchone()
    c.execute("SELECT COUNT(*) FROM follow WHERE follower = ?",(username,))
    foll = c.fetchone()
    if foll:
        for foll in foll:
            tt = foll
    if image:
        pro = image[0]
    if fol:
        for foll in fol:
            t = foll
    if image:
        pro = image[0]
    else:
        pro = url_for("static",filename="image/alexander-shatov-PEJtZfT6C1Q-unsplash.jpg")    
    if not username:
        return redirect('/login')
    if request.method == "POST":
        image = request.files["image"]
        filetype,_ = mimetypes.guess_type(image.filename)
        encode = base64.b64encode(image.read()).decode()
        image = f"data:{filetype};base64,{encode}"
        
        c.execute("UPDATE profile SET image = ? WHERE name = ?",(username,image))
    return render_template("profile.html",username=username,profile=pro,followers=t,following=tt,post=n,list=lis)  
@profile.route('/edit/profile',methods=["POST","GET"])
def edi():
    username = session.get("username")
    db = sqlite3.connect("../database/database.db")
    c = db.cursor()
    if request.method == "POST":
        image = request.files["image"]
        f,_ = mimetypes.guess_type(image.filename)
        encode = base64.b64encode(image.read()).decode()
        t = f"data:{f};base64,{encode}"
        c.execute("UPDATE profile SET image = ? WHERE name = ?",(t,username))
        db.commit()
        
    c.execute("SELECT image FROM profile WHERE name = ?", (username,))
    result = c.fetchone()
    profile_image = result[0] if result else None

    return render_template("editprofile.html", profile_image=profile_image)
