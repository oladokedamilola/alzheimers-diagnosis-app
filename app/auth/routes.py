from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import RegistrationForm, LoginForm
from ..models import User, db

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', category='success')
        return redirect(url_for('auth.login'))
    elif form.is_submitted() and not form.validate():
        # Only flash the error message if the form has been submitted
        flash('Registration unsuccessful. Please try again.', category='danger')
    return render_template('auth/register.html', form=form)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful.', category='success')
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', category='danger')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.home'))
