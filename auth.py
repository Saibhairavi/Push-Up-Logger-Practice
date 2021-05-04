from flask import Blueprint,render_template,url_for,request,redirect

from werkzeug.security import generate_password_hash,check_password_hash

#add user data into user table
from .models import User

#we need db
from . import db

from flask_login import login_user,logout_user,login_required

auth=Blueprint('auth',__name__)


@auth.route('/signup')
def signup():
    # return 'This page will be used to sign up users'
    return render_template('signup.html')

@auth.route('/signup',methods=['POST'])
def signup_post():
    email=request.form.get('email')
    name=request.form.get('name')
    password=request.form.get('password')    

    # print(email,name,password)
    user=User.query.filter_by(email=email).first()
    if user:
        # print('user already exists')
        return redirect(url_for('auth.signup'))

    new_user=User(email=email,name=name,password=generate_password_hash(password,method='sha256'))

    #add new user to db
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login',methods=['POST'])
def login_post():
    email=request.form.get('email')
    password=request.form.get('password')
    # print(email,password)
    remember=True  if request.form.get('remembber') else False

    user=User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password,password):
        return redirect(auth.login)

    #set login session inside login post
    login_user(user,remember=remember)

    return redirect(url_for('main.profile'))

@auth.route('/logout')
@login_required
#to access logout page 
def logout():
    # return 'Use this to log out'
    logout_user()
    return  redirect(url_for('main.index'))
