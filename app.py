from flask import Flask, g, render_template, flash, redirect, url_for, abort
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/layout')
def layout_page():
    return render_template('layout.html')


@app.route('/login')
def login_page():
    return render_template('login.html')


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
