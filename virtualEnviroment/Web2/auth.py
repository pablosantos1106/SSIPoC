from flask import Blueprint, redirect, url_for, render_template, request, flash, session
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .functions import *
from .main import PARAMSCONSENT, WEBNAME, CHAIN_ID

auth = Blueprint('auth', __name__)

@auth.route('/consent')
def consent():
    return render_template('consent.html', UserParams = PARAMSCONSENT)

@auth.route('/consent', methods=['POST'])
def consent_post():

    if request.form["btn"]=="Accept":
        
        provider = getProvider(current_user.url, current_user.port)

        #Check Blockchain connection
        if not provider.isConnected():
            flash("No se ha podido conectar con la blockchain del usuario")
            return redirect(url_for('auth.login'))

        if (len(request.form.get('privateKey')) == 0):
            flash ("La clave privada no es válida, revise este valor")
            return redirect(url_for('auth.consent'))

        #Save the user privateKey this session to aprove each access to his profile while its loged
        #This avoids requesting the password every time you access your profile.
        session['pk'] = request.form.get('privateKey')
        
        #Register consent in user blockchain.
        try:
            addWeb(provider, session['contractAddress'], session['abi'], WEBNAME, PARAMSCONSENT, CHAIN_ID, current_user.wallet, session['pk'])
            return redirect(url_for('main.profile'))      
        except Exception as e:
            error = "Ocurrió un error al registrar el consentimiento de la web en la blockchain del usuario"
            d = parsePkError(e)
            return render_template("error.html", error=error, details=d)   
    else:
        #If the user denies consent, the user is unlogged.        
        return redirect(url_for('auth.logout'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    #Get user input
    username = request.form.get('username').lower()
    password = request.form.get('password')
    url = request.form.get('url').lower()
    port = request.form.get('port')
    wallet = request.form.get('wallet')

    #Check input data
    if (usernameAlreadyExists(username) or blockchainUrlUsed(url, port)  or walletAlreadyExists(wallet)):
        return redirect(url_for('auth.signup'))

    #Check blockchain connection
    provider = getProvider(url, port)
    if not provider.isConnected():
        flash('No se ha podido conectar la blockchain del usuario, revise la url y el puerto introducidos')
        return redirect(url_for('auth.signup'))

    #Check if user has already registered his personal data, if not cannot create an account
    try:
        if (getContractAddress(getProvider(url, port)) == " "):
            flash("No existe informacion personal en la blockchain del usuario. Por favor, registre su información personal para poder registrarse")
            return redirect(url_for('auth.signup'))
    except Exception as e:
        error = "Ha ocurrido un error al comprobar el contrato del usuario "
        return render_template("error.html", error=error, details=e)

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    try:
        #Creates new user object
        new_user = User(username=username, password=generate_password_hash(password, method='sha256'), url=url, port=port, wallet=wallet)
        
        # add the new user to the database
        db.session.add(new_user)

        #Commit the changes
        db.session.commit()

    except Exception as e:
        error = "Ha ocurrido un error al crear el usuario"
        return render_template("error.html", error=error, details=e)

    return redirect(url_for('auth.login'))

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():

    session['pk']=""
   
    username = request.form.get('username').lower()
    password = request.form.get('password')

    try:
        #Search if user exists in database
        user = User.query.filter_by(username=username).first()
    except Exception as e:
        error = "Ha ocurrido un error al buscar en la base de datos"
        return render_template("error.html", error=error, details=e)

    # Check if user actually exists
    # Take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password): 
        flash('Login incorrecto. Por favor, revisa los valores introducidos')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page
    
    provider = getProvider(user.url, user.port)

    if not provider.isConnected(): 
        flash("No se ha podido establecer conexión con la blockchain del usuario")
        return redirect(url_for('auth.login'))

    #Check if user has already deployed a contract 
    if not isContractDeployed(provider):
        flash("No existe informacion personal en la blockchain del usuario. Por favor, registre su información personal para poder registrarse")
        return redirect(url_for('auth.login'))

    #Get contract info to call the functions
    try:
        session['contractAddress'] = getContractAddress(provider)
        session['abi'] = getAbi(getWallet(provider))
    except Exception as e:
        error = "Ha ocurrido un error al obtener la información del contrato del usuario"
        return render_template("error.html", error=error, details=e)

    # If the above check passes, then we know the user has the right credentials
    login_user(user)

    #Check if webapp has already registered in data consent
    try:
        if not (hasWebConsent(provider, session['contractAddress'],  session['abi'], WEBNAME)):
            return redirect(url_for('auth.consent'))
        elif (len(session['pk'])!=0):
            return redirect(url_for('main.profile'))
        else:
            return redirect(url_for('main.access'))
    except Exception as e:
        error = "Ha ocurrido un error al comprobar el consentimiento de la web"
        return render_template("error.html", error=error, details=e)
    

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

    # Validate Inputs
    if newPw != repeatedPw:
        flash('La contraseña repetida no coincide, por favor inténtelo de nuevo')
        return redirect(url_for('auth.changePassword'))

    if (not check_password_hash(current_user.password, actualPw)):
        flash('Su contraseña actual no es válida, por favor inténtelo de nuevo')
        return redirect(url_for('auth.changePassword'))

    # Change the user password
    try:
        user = User.query.filter_by(username=current_user.username).first()
        if user:
            user.password = generate_password_hash(newPw, method='sha256')
            db.session.add(user)
            db.session.commit()
    except Exception as e:
        error = "Ha ocurrido un error al modificar la contraseña del usuario"
        return render_template("error.html", error=error, details=e)

    return redirect(url_for('main.profile'))


@auth.route('/logout')
@login_required
def logout():
    session['contractAddress'] = ''
    session['abi'] = ''
    session['pk'] = ''
    logout_user()
    return redirect(url_for('main.index'))