from flask import Flask,render_template,request,Blueprint,flash,current_app,redirect,session,jsonify,url_for
from datetime import datetime,timedelta
import sqlite3,time,uuid,mimetypes,base64
post = Blueprint("post",__name__)
@post.route('/post',methods=["POST","GET"])
def send():
    db = sqlite3.connect("database/database.db")
    c = db.cursor()
    username = session.get("username")
    c.execute("SELECT image FROM profile WHERE name = ?",(username,))
    im = c.fetchone()
    c.execute("SELECT COUNT(*) FROM follow WHERE username = ?",(username,))
    followers = c.fetchone()
    print(f"followers {followers}")
    for followers in followers:
        follow = followers
    if im:
        pro = im[0]
    else:
        pro = url_for("static",filename="image/alexander-shatov-PEJtZfT6C1Q-unsplash.jpg")    
    if request.method == "POST":
        name = request.form["name"]
        file = request.files["file"]
        hashtag = request.form["key"]
        caption = request.form["caption"]
        id = str(uuid.uuid4())
        filetype,_ = mimetypes.guess_type(file.filename)
        encode = base64.b64encode(file.read()).decode()
        encode = f"data:{filetype};base64,{encode}"
        date = datetime.now().strftime("%B %A %y")
        db = sqlite3.connect("database/database.db")
        c = db.cursor()
        c.execute("INSERT INTO post (username,name,file,key,caption,id,date) VALUES(?,?,?,?,?,?,?)",(username,name,encode,hashtag,caption,id,date))
        db.commit()
    return render_template("post.html",username=username,profile=pro,followers=follow)    
@post.route('/post/edit/<string:id>', methods=["GET", "POST"])
def edit_post(id):
    db = sqlite3.connect("database/database.db")
    c = db.cursor()

    # Fetch existing post data
    c.execute("SELECT username, name, file, key, caption FROM post WHERE id = ?", (id,))
    post_data = c.fetchone()

    if not post_data:
        return "Post not found", 404

    username, old_name, old_file, old_key, old_caption = post_data

    if request.method == "POST":
        new_name = request.form.get("name", old_name)
        new_key = request.form.get("key", old_key)
        new_caption = request.form.get("caption", old_caption)
        new_file = request.files.get("file")

        file_changed = False
        if new_file and new_file.filename:
            filetype, _ = mimetypes.guess_type(new_file.filename)
            encoded = base64.b64encode(new_file.read()).decode()
            new_file_data = f"data:{filetype};base64,{encoded}"
            file_changed = new_file_data != old_file
        else:
            new_file_data = old_file

        # Check if any field has changed
        if (
            new_name != old_name or
            new_key != old_key or
            new_caption != old_caption or
            file_changed
        ):
            c.execute("""
                UPDATE post SET name = ?, key = ?, caption = ?, file = ? WHERE id = ?
            """, (new_name, new_key, new_caption, new_file_data, id))
            db.commit()

        return redirect(f"/post/view/{id}")

    return render_template("editpost.html", name=old_name, key=old_key, caption=old_caption, file=old_file)

@post.route('/post/delete/<string:id>',methods=["POST","GET"])
def delete(id):
    db = sqlite3.connect("database/database.db")
    c = db.cursor()
    c.execute("DELETE FROM post WHERE id = ?",(id,))
    db.commit()

    return redirect('/profile')         

