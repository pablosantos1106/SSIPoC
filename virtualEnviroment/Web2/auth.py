from flask import Blueprint, redirect, url_for, render_template, request, flash, session
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .functions import *
from .main import PARAMSCONSENT, WEBNAME

auth = Blueprint('auth', __name__)

@auth.route('/consent')
def consent():
    return render_template('consent.html', UserParams = PARAMSCONSENT)

@auth.route('/consent', methods=['POST'])
def consent_post():

    if request.form["btn"]=="Accept":

        provider = getProvider(current_user.url, current_user.port)
        privateKey = request.form.get('privateKey')
        session['pk'] = privateKey
        if (len(privateKey) == 0):
            flash ("Clave privada inválida, revise este valor")
            return redirect(url_for('auth.consent'))
        
        #Register consent in user blockchain.
        addWeb(provider, session['contractAddress'], session['abi'], WEBNAME, PARAMSCONSENT, 1337, current_user.wallet, privateKey)

        return redirect(url_for('main.profile'))      
    else:
        return redirect(url_for('auth.logout'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    # Code to validate and add user to database goes here
    username = request.form.get('username').lower()
    password = request.form.get('password')
    url = request.form.get('url').lower()
    port = request.form.get('port')
    wallet = request.form.get('wallet')

    #Check input data
    if (usernameAlreadyExists(username) or blockchainUrlUsed(url, port) or checkBlockchainConnection(getProvider(url, port)) or walletAlreadyExists(wallet)):
        return redirect(url_for('auth.signup'))

    #Check if user has already registered his personal data, if not cannot create an account
    if (getContractAddress(getProvider(url, port)) == " "):
        flash("No existen información registrada en su blockchain. Por favor, añada sus datos primero para poder registrarse")
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(username=username, password=generate_password_hash(password, method='sha256'), url=url, port=port, wallet=wallet)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
   
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password): 
        flash('Login incorrecto. Por favor compruebe de nuevo los datos introducido.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page
    
    provider= getProvider(user.url, user.port)

    contractAddress = getContractAddress(provider)
    session['contractAddress'] = contractAddress
    session['abi'] = getAbi(getWallet(provider))

    #Check if user has already deployed a contract 
    if not isContractDeployed(provider):
        flash("No existen información registrada en su blockchain. Por favor, añada sus datos primero.")
        redirect('auth.login')  

    # if the above check passes, then we know the user has the right credentials
    login_user(user)

    #Check if webapp has already regsitered in data consent
    if not (hasWebConsent(provider, session['contractAddress'],  session['abi'], WEBNAME)):
        return redirect(url_for('auth.consent'))
    elif (len(session['pk'])!=0):
        return redirect(url_for('main.profile'))
    else:
        return redirect(url_for('main.access'))

@auth.route('/changePassword')
@login_required
def changePassword():
    return render_template('changePassword.html')


@auth.route('/changePassword', methods=['POST'])
@login_required
def changePassword_post():

    actualPw = request.form.get('actualPassword')
    newPw = request.form.get('newPassword')
    repeatedPw = request.form.get('repeatedPassword')

    ## Validate Inputs
    if newPw != repeatedPw:
        flash('La contraseña repetida no coincide, por favor inténtelo de nuevo')
        return redirect(url_for('main.changePassword'))

    if (not check_password_hash(current_user.password, actualPw)):
        flash('Su contraseña actual no es válida, por favor inténtelo de nuevo')
        return redirect(url_for('main.changePassword'))

    ## Change the user password
    user = User.query.filter_by(username=current_user.username).first()

    if user:
        user.password = generate_password_hash(newPw, method='sha256')
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('main.profile'))


@auth.route('/logout')
@login_required
def logout():
    session['contractAddress'] = ''
    session['abi'] = ''
    session['pk'] = ''
    logout_user()
    return redirect(url_for('main.index'))