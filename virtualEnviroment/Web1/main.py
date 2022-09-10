from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_login import login_required, current_user
from .functions import *

WEBNAME= "PcShop"
PARAMSCONSENT = ["Email","Name", "Surname", "Gender", "Birthday","Address", "City","PostalCode", "Country", "PhoneNumber", "CreditCard"]
CHAIN_ID = 1337

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('auth.login'))

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
    
    #Check Blockchain connection
    if not provider.isConnected():
        error = "Unable to connect to the user's blockchain"
        return render_template("lostConnection.html", error=error)

    #Add web access to user web register
    try:
        addWebAcess(provider, CHAIN_ID, session['contractAddress'], session['abi'], WEBNAME, current_user.wallet, session['pk'] )
    except Exception as e:
        error = "An error has occurred while registering web access in the user's blockchain."
        d = parsePkError(e)
        return render_template("error.html", error=error, details=d)

    #Call getData contract funcion to get User's data
    try:
        userData = mapUserData(functionParamsCall(PARAMSCONSENT,provider, session['contractAddress'], session['abi'], WEBNAME))
    except Exception as e:
        error = "An error occurred while getting user data"
        return render_template("error.html", error=error, details=e)

    return render_template('profile.html', user=current_user, userData=userData)

@main.route('/profile', methods=['POST'])
@login_required
def profile_post():
    return redirect(url_for('auth.changePassword'))
