from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from .functions import *
from datetime import datetime
import time

main = Blueprint('main', __name__)

CHAIN_ID = 1337

@main.route('/')
def index():
    return render_template("index.html")

@main.route('/', methods=['POST'])
def test_post():

    #Save the blockchain info in session parameters
    session['URL'] = request.form.get('url') + ':' + request.form.get('port')
    w3 = getProvider(session['URL'])
    wallet = request.form.get('wallet')

    #Check blockchain conection
    if not (w3.isConnected()):
        flash( 'Cannot connect: Invalid parameters')
        return redirect(url_for('main.index'))
    else:
        #Check if user has already set his data
        if not isContractDeployed(w3):
             return redirect(url_for('main.registerData'))
        else:
            output_path = 'User/contracts/output/' + wallet + '/contract_output.json'
            output = getContractRequiredInfo(output_path)
            session['contractAddress'] = output[0]
            session['abi'] = output[1]
            return redirect(url_for('main.profile'))


@main.route('/registerData')
def registerData():
   return render_template("register.html")

@main.route('/registerData', methods=['POST'])
def registerData_post():

    #Get de blockchain provider
    w3 = getProvider(session['URL'])

    #Select the input data
    wallet = request.form.get('wallet')
    email = request.form.get('email')
    dni= request.form.get('dni')
    name = request.form.get('name')
    surname = request.form.get('surname')
    genderValues = ['Male', 'Female', 'Transgender']
    gender = getCheckboardValues(genderValues)
    birthday = datetime.strptime(request.form.get('birthday'), '%Y-%m-%d')
    birthday_unix = int(time.mktime(birthday.date().timetuple()))
    address = request.form.get('address')
    city = request.form.get('city')
    postalCode = request.form.get('postalCode')
    country = request.form.get('country')
    phoneNumber = request.form.get('phoneNumber')
    igUsername = request.form.get('igUsername')
    twUsername = request.form.get('twUsername')
    creditCard = request.form.get('creditCard')
    privateKey = request.form.get('privateKey')


    #Validate Input Data
    if not validateUserInputData(provider=w3, wallet=wallet, dni=dni, phoneNumber=phoneNumber, creditCard=creditCard, gender= gender):
        return redirect(url_for('main.registerData'))

    data = {"wallet":wallet, "email":email, "dni":dni, "name":name, "surname":surname, 
            "gender":gender[0], "birthday": birthday_unix, "addr": address, "city":city, "postalCode": postalCode, "country": country, 
            "phoneNumber":phoneNumber, "igUsername":igUsername, "twUsername":twUsername, "creditCard":creditCard}

    path = 'User/contracts/output/' + wallet  

    #Create the user output folder
    if not os.path.exists(path):
        os.makedirs(path)

    path += '/contract_output.json'

    session['output_path'] = path
    contract_path = 'User/contracts/RegisterData.sol'

    #Desploy contract in blockchain
    contractInfo = deployContract(w3, contract_path, session['output_path'], CHAIN_ID, wallet, privateKey)
    session ['abi'] = contractInfo[0]
    session ['contractAddress'] = contractInfo[1]

    #Storage user data in contract created   
    storeContract(w3Provider=w3, chain_id=CHAIN_ID, contractAddress=session ['contractAddress'], abi= session ['abi'], userData= data, privateKey=privateKey)

    return redirect(url_for('main.profile'))

@main.route('/profile')
def profile():
    #Get the blockchain provider 
    w3 = getProvider(session['URL'])

    #Call contract function to get user data
    userData = mapBlockchainOutput(getData(w3,session ['contractAddress'], session ['abi'] ))

    return render_template("profile.html", userData = userData)

@main.route('/disconnect')
def disconnect():
    session['URL'] = ''
    session['abi'] = ''
    session['contractAddress'] = ""
    session['output_path'] = ""
    return redirect(url_for('main.index'))

