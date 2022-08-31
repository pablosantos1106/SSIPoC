from wsgiref import validate
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from .functions import *

main = Blueprint('main', __name__)
CHAIN_ID = 1337 #Ganache ChainID

@main.route('/')
def index():
    return render_template("index.html")

@main.route('/', methods=['POST'])
def index_post():

    #Save the blockchain info in session parameters
    session['URL'] = request.form.get('url') + ':' + request.form.get('port')
    wallet = request.form.get('wallet')
    provider = getProvider(session['URL'])

    #Check blockchain conection and wallet
    if not provider.isConnected():
        flash("Unable to connect user's blockchain")
        return redirect(url_for('main.index'))
    elif not validateWallet(provider, wallet):
        return redirect(url_for('main.index'))
    
    try:
        #Check if user has already set his data in blockchain
        if not isContractDeployed(provider):
            return redirect(url_for('main.registerData'))
        else:
            output_path = 'User/contracts/output/' + wallet + '/contract_output.json'
            output = getContractRequiredInfo(output_path)
            session['contractAddress'] = output[0]
            session['abi'] = output[1]
            return redirect(url_for('main.profile'))
    except Exception as e:
        error = "Unable to connect user's blockchain"
        return render_template("error.html", error = error, details= e)


@main.route('/registerData')
def registerData():
   return render_template("register.html")

@main.route('/registerData', methods=['POST'])
def registerData_post():

    #Check blockchain connection
    provider = getProvider(session['URL'])
    if not provider.isConnected():
        flash("Unable to connect user's blockchain")
        return redirect(url_for('main.registerData'))

    ## Get the user data 
    try:
        data = getDatafromUser()
        privateKey = request.form.get('privateKey')
    except Exception as e:
        flash (e)
        return redirect(url_for('main.registerData')) 

    #Validate Input Data
    if not validateUserInputData(provider=provider, wallet=data["wallet"], dni=data["dni"], phoneNumber=data["phoneNumber"], creditCard=data["creditCard"], gender=data["gender"]):
        return redirect(url_for('main.registerData'))

    # Set the path to the user contract
    path = 'User/contracts/output/' + data["wallet"]

    #Create the user output folder
    if not os.path.exists(path):
        os.makedirs(path)

    path += '/contract_output.json'

    session['output_path'] = path
    contract_path = 'User/contracts/RegisterData.sol'

    #Deploy user contract in blockchain
    try:
        contractInfo = deployContract(provider, contract_path, session['output_path'], CHAIN_ID, data["wallet"], privateKey)
        session ['abi'] = contractInfo[0]
        session ['contractAddress'] = contractInfo[1]
    except Exception as e:
        error = "Error deploying the contract in the blockchain"
        return render_template("error.html", error=error, details=e)

    #Storage user data in contract created   
    try:
        registerUserData(w3Provider=provider, chain_id=CHAIN_ID, contractAddress=session ['contractAddress'], abi= session ['abi'], userData= data, privateKey=privateKey)
    except Exception as e:
        error = "Error registering the user's data in the contract"
        return render_template("error.html", error=error, details=e)

    return redirect(url_for('main.profile'))

@main.route('/profile')
def profile():

    #Get the blockchain provider 
    provider = getProvider(session['URL'])

    #Check Blockchain connection
    if not provider.isConnected():
        error = "No se ha podido conectar con la blockchain del usuario"
        return render_template("lostConnection.html", error=error)
        
    #Call contract function to get user data
    try:
        userData = mapBlockchainOutput(getData(provider,session ['contractAddress'], session ['abi'] ))
    except Exception as e:
        error = "Error getting user data"
        return render_template("error.html", error=error, details=e)

    #Call contract function to get webs info data
    try:
        webInfo = mapWebInfoOutput(getWebList(provider, session['contractAddress'], session['abi']))
    except Exception as e:
        error = "Error getting webs info"
        return render_template("error.html", error=error, details=e)

    #Call contract function to get modified history data
    try:
        dataHistory = formatHistoryData(getDataHistory(provider, session['contractAddress'], session['abi']))
    except Exception as e:
        error = "Error getting modifications history"
        return render_template("error.html", error=error, details=e)

    return render_template("profile.html", userData=userData, webInfo=webInfo, dataHistory=dataHistory)


@main.route('/profile', methods=['POST'])
def profile_post():
    return redirect(url_for('main.modify'))

@main.route('/modify')
def modify():
    return render_template("modify.html")

@main.route('/modify', methods=['POST'])
def modify_post():

    #Get de blockchain provider
    provider = getProvider(session['URL'])

    #Check blockchain connection
    if not provider.isConnected():
        flash("Unable to connect user's blockchain")
        return redirect(url_for('main.modify'))

    ## Get the new data 
    data = getDatafromUser()
    privateKey = request.form.get('privateKey')

    ## Validate input data 
    if not validateUserInputData(provider=provider, wallet=data["wallet"], dni=data["dni"], phoneNumber=data["phoneNumber"], creditCard=data["creditCard"], gender=data["gender"]):
        return redirect(url_for('main.modify'))

    #Register data in the history
    try:
        addDataHistory(w3Provider=provider, chain_id=CHAIN_ID, contractAddress=session ['contractAddress'], abi= session ['abi'], userData= data, privateKey=privateKey)
    except Exception as e:
        error = "Error saving old user's data in blockchain history "
        return render_template("error.html", error=error, details=e)
    
    #Update new data 
    try:
        registerUserData(w3Provider=provider, chain_id=CHAIN_ID, contractAddress=session ['contractAddress'], abi= session ['abi'], userData= data, privateKey=privateKey)
    except Exception as e:
        error = "Error upadting new user's data"
        return render_template("error.html", error=error, details=e)

    return redirect(url_for('main.profile'))


@main.route('/disconnect')
def disconnect():
    session['URL'] = ''
    session['abi'] = ''
    session['contractAddress'] = ""
    session['output_path'] = ""
    return redirect(url_for('main.index'))

