from flask import Blueprint, render_template, request, flash, get_flashed_messages, redirect, url_for
from .models import User, Employee
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

# our login endpoint... has both a get and post method
@auth.route('/login', methods=['GET','POST'])
#what happens when we arrive at /login
def login():
    #check the request type
    if request.method == 'POST':
        #return the variables filled out in our user forms in the login page
        email = request.form.get('email')
        password = request.form.get('password')
        #query the user's email and return the first result... there is built in validation to only allow unique emails
        user = User.query.filter_by(email=email).first()
        #if we find a user with this email, check password
        if user:
            #check the user password matches whats in our database
            if password == user.password:
                flash('Logged in!', category='success')
                #keeps the user logged in unless something like clearing cache
                login_user(user, remember=True)
                #redirect our user to the "home.html" page... we use redirect(url_for()) because this is dynamic to whatever we want to specify the enpoint as, rather than just returning "/home.html"
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password', category='error')
        else: 
            flash('Email does not exist', category='error')
    return render_template("login.html", user=current_user)

#logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!', category='error')
        elif (len(email) < 4):
            flash('Email must be > 4 characters', category = 'error')
            pass
        elif (len(firstName) < 2):
            flash('First name must be > 2 cahracters', category = 'error')
            pass
        elif (len(password1) < 7):
            flash('Password must be > 7 characters', category = 'error')
            pass
        elif(password1 != password2):
            flash('Password do not match', category = 'error')
            pass
        else:
            if request.form.getlist('employee') == ['on']:
                new_employee = Employee(email = email, firstName = firstName, password=password1)
                db.session.add(new_employee)
                db.session.commit()
            else:
                new_user = User(email = email, firstName = firstName, password=password1)
                db.session.add(new_user)
                db.session.commit()
            flash('Account Created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home', user=current_user))    
    return render_template("signup.html")