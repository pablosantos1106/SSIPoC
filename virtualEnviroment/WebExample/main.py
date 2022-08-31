from contextlib import redirect_stderr
from getpass import getuser
from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_login import login_required, current_user
from .functions import *
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

WEBNAME= "PC SHOP"
PARAMSCONSENT = ["Email","Name", "Surname","Birthday","Address", "City","PostalCode", "Country", "PhoneNumber", "CreditCard"]

CHAIN_ID = 1337
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
    #Get the user's blockchain provider
    provider = getProvider(current_user.url, current_user.port)

    #Add web access to user web register
    addWebAcess(provider, CHAIN_ID, session['contractAddress'], session['abi'], WEBNAME, current_user.wallet, session['pk'] )

    #Call getData contract funcion to get User's data
    userData = mapUserData(functionParamsCall(PARAMSCONSENT,provider, session['contractAddress'], session['abi'], WEBNAME))

    return render_template('profile.html', user=current_user, userData=userData)


@main.route('/profile', methods=['POST'])
@login_required
def profile_post():
    return redirect(url_for('auth.changePassword'))




