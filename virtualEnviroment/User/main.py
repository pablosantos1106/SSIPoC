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

    ## Get the user data 
    data = getDatafromUser()
    privateKey = request.form.get('privateKey')

    #Validate Input Data
    if not validateUserInputData(provider=w3, wallet=data["wallet"], dni=data["dni"], phoneNumber=data["phoneNumber"], creditCard=data["creditCard"], gender=data["gender"]):
        return redirect(url_for('main.registerData'))

    # Set the path to the user contract
    path = 'User/contracts/output/' + data["wallet"]

    #Create the user output folder
    if not os.path.exists(path):
        os.makedirs(path)

    path += '/contract_output.json'

    session['output_path'] = path
    contract_path = 'User/contracts/RegisterData.sol'

    #Desploy contract in blockchain
    contractInfo = deployContract(w3, contract_path, session['output_path'], CHAIN_ID, data["wallet"], privateKey)
    session ['abi'] = contractInfo[0]
    session ['contractAddress'] = contractInfo[1]

    #Storage user data in contract created   
    registerUserData(w3Provider=w3, chain_id=CHAIN_ID, contractAddress=session ['contractAddress'], abi= session ['abi'], userData= data, privateKey=privateKey)

    return redirect(url_for('main.profile'))

@main.route('/profile')
def profile():
    #Get the blockchain provider 
    w3provider = getProvider(session['URL'])

    #Call contract function to get user data
    userData = mapBlockchainOutput(getData(w3provider,session ['contractAddress'], session ['abi'] ))

    #Call contract function to get webs info data
    webInfo = mapWebInfoOutput(getWebList(w3provider, session['contractAddress'], session['abi']))

    #Call contract function to get modified history data
    dataHistory = formatHistoryData(getDataHistory(w3provider, session['contractAddress'], session['abi']))

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
    w3 = getProvider(session['URL'])

    ## Get the new data 
    data = getDatafromUser()
    privateKey = request.form.get('privateKey')

    ## Validate input data 
    if not validateUserInputData(provider=w3, wallet=data["wallet"], dni=data["dni"], phoneNumber=data["phoneNumber"], creditCard=data["creditCard"], gender=data["gender"]):
        return redirect(url_for('main.modify'))

    #Register data in the history
    addDataHistory(w3Provider=w3, chain_id=CHAIN_ID, contractAddress=session ['contractAddress'], abi= session ['abi'], userData= data, privateKey=privateKey)

    #Update new data 
    registerUserData(w3Provider=w3, chain_id=CHAIN_ID, contractAddress=session ['contractAddress'], abi= session ['abi'], userData= data, privateKey=privateKey)

    return redirect(url_for('main.profile'))


@main.route('/disconnect')
def disconnect():
    session['URL'] = ''
    session['abi'] = ''
    session['contractAddress'] = ""
    session['output_path'] = ""
    return redirect(url_for('main.index'))

