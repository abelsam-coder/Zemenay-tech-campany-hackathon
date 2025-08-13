from flask import Flask,current_app,redirect,session,render_template,url_for,request
from flask_socketio import SocketIO,emit,join_room
import sqlite3
from flask_bcrypt import Bcrypt,generate_password_hash,check_password_hash
from submodules.signup import signup
from submodules.dashboard import dash
from submodules.post import post
from submodules.setting import conset
from submodules.follow import follow
from submodules.comment import comment
from submodules.search import search
from submodules.login import login
from submodules.like import like
from submodules.save import save
from submodules.profile import profile
app = Flask(__name__,template_folder="../template",static_folder="../static")
app.secret_key = "secret"
app.debug = True
app.register_blueprint(signup)
app.register_blueprint(follow)
app.register_blueprint(comment)
app.register_blueprint(search)
app.register_blueprint(login)
app.register_blueprint(dash)
app.register_blueprint(profile)
app.register_blueprint(post)
app.register_blueprint(conset)
app.register_blueprint(like)
app.register_blueprint(save)
@app.route('/logout')
def logout():
    session.pop("username")
    return redirect("/login")
@app.route('/')
def home():
    username = session.get("username")
    if not username:
        return redirect("/login")
    return redirect("dashboard")
bcrypt = Bcrypt(app)
sock = SocketIO(app)
@app.route("/chat")
def chat():
    receiver = request.args.get("receiver")
    username = session.get("username")

    conn = sqlite3.connect("../database/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM authentication")
    f = cursor.fetchall()
    im = ''
    cursor.execute("SELECT image FROM profile WHERE name = ?",(username,))
    profile = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM follow WHERE username = ?",(username,))
    followers = cursor.fetchone()
    print(followers)
    for follower in followers:
        follow = follower
        print(follow)
    formatted_users = []
    for follower in f:
        if follower and follower[0]:
            cursor.execute("SELECT image FROM profile WHERE name = ?",(follower[0],))
            im = cursor.fetchone()
            if im:
                formatted_users.append({
                    "name":follower[0],
                    "image":im[0]
                })  
            else:
                formatted_users.append({
                    "name":follower[0],
                    "image":url_for("static",filename="image/alexander-shatov-PEJtZfT6C1Q-unsplash.jpg")
                })        
        else:
            pass    

    

    return render_template("p.html", users=formatted_users,username=username,profile=profile,ff=follow)
@app.route('/security')
def sec():
    username = session.get("username")
    conn = sqlite3.connect("../database/database.db")
    c = conn.cursor()
    c.execute("SELECT device FROM attempttwo WHERE username = ?",(username,))
    f = c.fetchall()
    return render_template("security.html",f=f)
@app.route('/security/kikcout/<string:device>')
def kick(device):
    username = session.get("username")
    conn = sqlite3.connect("../database/database.db")
    c = conn.cursor()
    c.execute("INSERT INTO kickout (username , device) VALUES(?,?)",(username,device))
    conn.commit()
    return redirect('/security')
@sock.on("connect")
def handle_connect():
    username = session.get("username")
    if username:
        join_room(username) 

@sock.on("private_message")
def handle_private_message(data):
    sender = session.get("username")
    receiver_name = data["receiver_name"]
    print(receiver_name)
    message = data["message"]
    timestamp = data["timestamp"]
    if not sender:
        print("Error: Sender username is missing!")
        return
    emit("private_message", {"sender": sender, "message": message, "timestamp": timestamp}, room=receiver_name)
@app.route('/post/like/<string:id>')
def li(id):
    conn = sqlite3.connect("../database/database.db")
    c = conn.cursor()
    c.execute("SELECT username FROM like WHERE postid = ?",(id,))
    f = c.fetchall()
    a = []
    for username in f:
        u = username[0]
        c.execute("SELECT image FROM profile WHERE name = ?",(u,))
        im = c.fetchone()[0]
        a.append({
            "username":username,
            "image":im
        })   
    return render_template("postlike.html",f=a)    
@app.route('/saved/<string:username>')
def saved(username):
    conn = sqlite3.connect("../database/database.db")
    c = conn.cursor()   
    c.execute("SELECT postid FROM save WHERE username = ?", (username,))
    f = c.fetchall()
    posts = []
    for postid in f:
        c.execute("SELECT username, file, caption FROM post WHERE id = ?", (postid[0],))
        result = c.fetchone()
        if result:
            posts.append({
                "username": result[0],
                "file": result[1],
                "caption": result[2]
            })
    return render_template("saved.html", posts=posts)
  
app.extensions["sock"] = sock
app.extensions["bcrypt"] = bcrypt
app.run(host="0.0.0.0",port=8080)