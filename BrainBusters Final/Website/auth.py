from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Questions, Variants
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Remove hardcoded admin check and instead query the user by email
        user = User.query.filter_by(email=email).first()
        if user:
            # Check the user's password and whether they are privileged
            if check_password_hash(user.password, password):
                if user.privilaged == 1:  # Check if the user is privileged
                    flash('Welcome, privileged user!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.admin'))  # Render the admin panel for privileged users
                else:
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.game'))  # Redirect to the desired page after login
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    # If it's a GET request or if there's any failure, render the login page
    return render_template("Login.html", user=current_user)

    

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')  # Adjusted from 'password1' to 'password'

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        else:
            # Here the password variable is used directly as it is the corrected form data name
            user = User(email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            print("Success")  # Consider removing or changing to logging for production
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))

    return render_template("Register.html", user=current_user)

