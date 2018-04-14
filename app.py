from flask import Flask, g, render_template, flash, redirect, url_for, abort, session, request
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from db import *

app = Flask(__name__)
app.secret_key = 'DevangIsTheGreatest'



@app.route('/')
def index():
    if session.get("login"):
        return render_template('index.html',allposts = post_list(),fposts=post_list_follow(str(session["user_id"])))
    else:
        return redirect('/login')

@app.route('/post/single/<post_id>')
def single(post_id):
    return render_template('single.html',post = get_post(post_id)[0])

@app.route('/register', methods=["POST","GET"])
def register_page():
    if request.method=='POST':
        username=request.form["username"]
        password=request.form["password"]
        email=request.form["email"]
        bio=request.form["bio"]
        dob=request.form["dob"]
        ieee_no=request.form["ieee_no"]
        branch=request.form["branch"]
        sem=request.form["sem"]
        user_register(username,password,email,bio,dob,ieee_no,branch,sem)
        return "Registered Successfully"
    else:
        return render_template('register.html')

@app.route('/login', methods=["POST","GET"])
def login_page():
    if request.method=='POST':
        result = user_login(request.form["email"],request.form["password"])
        if result:
            session["login"] = True
            session["user_id"] = result[0]
            session["username"] = result[1]
            session["email"] = result[3]
            return redirect('/')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session["login"] = False
    session["user_id"] = ""
    session["username"] = ""
    session["email"] = ""
    return render_template('login.html')



@app.route('/members/all')
def member_page():
    result = members_list()
    return render_template('members.html', members=result)

@app.route('/members/followers')
def member_followers_page():
    result = follower_list(str(session['user_id']))
    return render_template('members.html', members=result)

@app.route('/members/following')
def member_following_page():
    result = following_list(str(session['user_id']))
    return render_template('members.html', members=result)


@app.route('/addpost',methods=["GET","POST"])
def add_user_post():
    if request.method=='POST':
        id=str(session["user_id"])
        post_data= request.form["post_data"]
        add_post(id,post_data,'0')
        return "Posted"
    else:
        return render_template('addpost.html')
    return render_template('addpost.html')

@app.route('/follow/<user_id>')
def follow_page(user_id):
    to_id= user_id
    from_id=session["user_id"]
    follow(from_id,to_id)
    return redirect( request.referrer)

@app.route('/unfollow/<user_id>')
def unfollow_page(user_id):
    to_id= user_id
    from_id=session["user_id"]
    unfollow(from_id,to_id)
    return redirect( request.referrer)

@app.route('/like/<post_id>')
def like(post_id):
    user_id=str(session["user_id"])
    like_post(user_id,post_id)
    return redirect( request.referrer)

@app.route('/unlike/<post_id>')
def unlike(post_id):
    user_id=session["user_id"]
    unlike_post(user_id,post_id)
    return redirect( request.referrer)


# @app.route('/logout')
# def layout_page():
#     return render_template('logout.html')
#
#
# @app.route('/register')
# def layout_page():
#     return render_template('register.html')


if __name__ == '__main__':
    # session["login"] = False
    app.jinja_env.globals.update(is_liked=is_liked)
    app.jinja_env.globals.update(get_likes=get_likes)
    app.jinja_env.globals.update(is_following=is_following)
    app.run(host='0.0.0.0', port=8000, debug=True)
