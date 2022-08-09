from getpass import getuser
from User.functions import getUserData
from flask import Blueprint, render_template, session, redirect, url_for
from flask_login import login_required, current_user
from .functions import *

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('login.html')

@main.route('/profile')
@login_required
def profile():

    user =  current_user
    provider = getProvider(user.url, user.port)

    #Search the contract address in user blockchain transactions
    contractAddress = getContractAddress(provider)

    session['contractAddress'] = contractAddress
    session['abi'] = getAbi(getUserWallet(provider))
    
    #Call getData contract funcion
    userData = mapUserData(getUserData(provider, session['contractAddress'], session['abi']))
    
    return render_template('profile.html', user=user, userData=userData)

