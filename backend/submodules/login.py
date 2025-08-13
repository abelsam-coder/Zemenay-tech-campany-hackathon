from flask import Flask,render_template,request,Blueprint,flash,current_app,redirect,session,jsonify
from datetime import datetime,timedelta
import sqlite3,time
login = Blueprint("login",__name__)
@login.route('/login',methods=["POST","GET"])
def signin():
    db = sqlite3.connect("../database/database.db")
    c = db.cursor()
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        device = request.form["device"]
        print(device)
        delta = timedelta(minutes=5)
        
        date = datetime.now().strftime("%B %A %y")
        bcrypt = current_app.extensions["bcrypt"]

        c.execute("SELECT password,device FROM authentication WHERE username = ?",(username,))
        f = c.fetchone()
        c.execute("SELECT device FROM another WHERE username = ?",(username,))
        rr = c.fetchone()
        c.execute("SELECT * FROM kickout WHERE username = ?",(username,))
        o = c.fetchone()
        if f and f[0]:
            check = bcrypt.check_password_hash(f[0],password)
            if check:
                if o:
                    flash("you can not enternin this account")
                if rr:    
                    for devic in rr:   
                        if f[1] == device or devic == device:
                            session["username"] = username
                            c.execute("DELETE FROM attempt WHERE device = ?",(device,))
                            db.commit()
                            return redirect('/dashboard')
                        else:
                            c.execute("INSERT INTO another (username,device,date) VALUES(?,?,?)",(username,device,date))
                            session["username"] = username 
                            return redirect('/dashboard')    
                else:
                    print('ayufuydyu')
                    if f[1] == device:
                        session["username"] = username
                        c.execute("DELETE FROM attempt WHERE device = ?",(device,))
                        db.commit()
                        return redirect('/dashboard') 
                    else:
                        c.execute("INSERT INTO another (username,device,date) VALUES(?,?,?)",(username,device,date))
                        c.execute("DELETE FROM attempt WHERE device = ?",(device,))
                        db.commit()
                        session["username"] = username 
                        return redirect('/dashboard')      
            else:
                c.execute("INSERT INTO attempt (device,username,date) VALUES (?,?,?)",(device,username,date))
                db.commit()
                c.execute("INSERT INTO attempttwo (device,username,date) VALUES (?,?,?)",(device,username,date))
                db.commit()
                flash("Incorrect credential")
        else:
            c.execute("INSERT INTO attempt (device,username,date) VALUES (?,?,?)",(device,username,date))
            db.commit()
            c.execute("INSERT INTO attempttwo (device,username,date) VALUES (?,?,?)",(device,username,date))
            db.commit()
            flash("No account found make sure you fill the correct credential","warning") 
        c.execute("SELECT COUNT(*) FROM attempt WHERE device = ?",(device,))
        attempt = c.fetchone()[0]          
        if int(attempt) >= 4:
                print("op")
                flash("Too many attempt please try after 5 minute")
                return render_template("login.html",time="timeslap")
        elif int(attempt) < 4:
            print("a")        
    return render_template("login.html")    
@login.route('/login/delete',methods=["GET"])
def delete():
    flash("a")
    device = request.args.get("device")
    print(device)
    db = sqlite3.connect("../database/database.db")
    c = db.cursor()
    c.execute("DELETE FROM attempt WHERE device = ?",(device,))
    db.commit()          
    return jsonify({"device":device})