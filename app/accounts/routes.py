from flask import render_template
from . import accounts

@accounts.route('/profile')
def profile():
    return render_template('accounts/profile.html')

@accounts.route('/edit-profile')
def edit_profile():
    return render_template('accounts/edit_profile.html')
