from contextlib import redirect_stderr
from getpass import getuser
from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_login import login_required, current_user
from .functions import *

WEBNAME= "PC SHOP"

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/access')
@login_required
def access():
    return render_template('access.html')


@main.route('/access', methods=['POST'])
@login_required
def access_post():

    session['pk'] = request.form.get('privateKey')
    return redirect(url_for('main.profile'))


@main.route('/profile')
@login_required
def profile():

    provider = getProvider(current_user.url, current_user.port)

    #Add data access to user register
    addWebAcess(provider, session['contractAddress'], session['abi'], WEBNAME, current_user.wallet, session['pk'] )

    #Call getData contract funcion
    userData = mapUserData(getUserData(provider, session['contractAddress'], session['abi']))

    return render_template('profile.html', user=current_user, userData=userData)


