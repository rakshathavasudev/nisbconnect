from flask import Flask, g, render_template, flash, redirect, url_for, abort
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from db import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/layout')
def layout_page():
    return render_template('layout.html')


@app.route('/login')
def login_page():
    result = user_login(email, password):
    if result:
        session["login"] = True
        session["user_id"] = result[0]
        session["username"] = result[1]
        session["email"] = result[3]
    return render_template('login.html')


@app.route('/members')
def member_page():
    conn = db.connectDB()
    query = ("SELECT username,email,bio,ieee_no,branch,sem FROM members")
    cursor = connection.cursor()
    cursor.execute(query)

    for (username,email,bio,ieee_no,branch,sem) in cursor:
	       print('{} {} {} {} {} {}'.format(username,email,bio,ieee_no,branch,sem))

    connection.close()
    return render_template('members.html')


@app.route('/addpost',methods=["GET","POST"])
def add_post():
    if request.method=='POST':
        c=connectDB()
        id="69"
        words= request.form["addpost"]
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        query="insert into posts (user_id,article,date_time) values ({},{},{})".format(id,words,timestamp)
        executeDB(c,query)
        disconnectDB()

        return "Posted"
    else:
        return render_template('addpost.html')
    return render_template('addpost.html')


# @app.route('/logout')
# def layout_page():
#     return render_template('logout.html')
#
#
# @app.route('/register')
# def layout_page():
#     return render_template('register.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000, debug=True)
