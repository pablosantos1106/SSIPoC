import string
from .models import User
from flask import flash
from web3 import Web3
import json
from datetime import datetime


def usernameAlreadyExists(username):
    
    #checks if username already exists
    user = User.query.filter_by(username=username).first() 
    if user:
        flash('Username already exists')
        return True
    return False


def blockchainUrlUsed (url, port):

    #Check if the input url is already registered by another user
    databaseUrl =  User.query.filter_by(url=url).first()

    #If exists, check the port on which the blockchain is deployed
    if databaseUrl:
        databasePort = User.query.filter_by(port=port).first() 
        if databasePort:
            flash('This url and port combination is currently in use by another user, please select another')
            return True
    return False

def getProvider (url, port):
    path = url + ":" + str(port)
    return Web3(Web3.HTTPProvider(path))

def checkBlockchainConnection(provider):

    if (provider.isConnected() == False):
        flash('Blockchain connection is not posible, please check the url and port input')
        
    return not provider.isConnected()

def getContractAddress (provider):
    output = " "
    transactionList = []
    for i in range(provider.eth.blockNumber+1):
        block = provider.eth.getBlock(i)
        if (i!=0):
            transactionList.append(block['transactions'][0])

    for i in range(len(transactionList)):
        transaction = json.loads(provider.toJSON(provider.eth.getTransaction(transactionList[i])))
        if (transaction['to'] is None):
            receipt = provider.eth.getTransactionReceipt(transaction['hash'])   
            output = receipt['contractAddress']
    return output

def getAbi (userWallet):
    PATH = 'User/contracts/output/' + userWallet + '/contract_output.json'
    with open(PATH) as jsonfile:
        data = json.load(jsonfile)

    return json.loads(data["contracts"]["RegisterData.sol"]["RegisterData"]["metadata"])["output"]["abi"]

def mapUserData(input):

    outputMapped = {"email":input[0], "name":input[1], "surname":input[2],  "birthday": datetime.fromtimestamp(input[3]).date() , 
                    "address": input[4], "city":input[5], "postalCode": input[6], "country": input[7], 
                    "phoneNumber":input[8], "creditCard":input[9]}
    return outputMapped


def isContractDeployed(w3Provider):
    output = False
    transactionList = []
    for i in range(w3Provider.eth.blockNumber+1):
        block = w3Provider.eth.getBlock(i)
        if (i!=0):
            transactionList.append(block['transactions'][0])

    for i in range(len(transactionList)):
        transaction = json.loads(w3Provider.toJSON(w3Provider.eth.getTransaction(transactionList[i])))
        if (transaction['to'] is None):
            output = True
    return output


def addWeb(w3Provider, contractAddress, abi, webName, params, chain_id, wallet, privateKey):
    nonce = w3Provider.eth.getTransactionCount(wallet)
    contact_list = w3Provider.eth.contract(address=contractAddress, abi=abi)
    addWeb = contact_list.functions.addWeb(webName, params).buildTransaction({"chainId": chain_id, "from": wallet, "gasPrice": w3Provider.eth.gas_price, "nonce": nonce})

    # Sign the transaction
    addWebTransaction = w3Provider.eth.account.sign_transaction(addWeb, private_key=privateKey)

    # Send the transaction
    w3Provider.eth.send_raw_transaction(addWebTransaction.rawTransaction)
    print("Add " + webName + "consent to user's blockchain")

def hasWebConsent (w3Provider, contractAddress, abi, webName):
    contact_list = w3Provider.eth.contract(address=contractAddress, abi=abi)
    return contact_list.functions.checkWebConsent(webName).call()

def addWebAcess(w3Provider, CHAIN_ID, contractAddress, abi, webName, wallet, privateKey):

    nonce = w3Provider.eth.getTransactionCount(wallet)
    contact_list = w3Provider.eth.contract(address=contractAddress, abi=abi)
    addWeb = contact_list.functions.addAccess(webName).buildTransaction({"chainId": CHAIN_ID, "from": wallet, "gasPrice": w3Provider.eth.gas_price, "nonce": nonce})

    # Sign the transaction
    addWebTransaction = w3Provider.eth.account.sign_transaction(addWeb, private_key=privateKey)

    # Send the transaction
    w3Provider.eth.send_raw_transaction(addWebTransaction.rawTransaction)
    print("Add " + webName + " access to user's blockchain")


def validateWallet(provider, wallet):
    if not provider.isAddress(wallet):
        flash('Invalid wallet address: '+ wallet)
        return False 
    return True

def walletAlreadyExists(wallet):
    
    #checks if username already exists
    user = User.query.filter_by(wallet=wallet).first() 
    if user:
        flash('Wallet already in use')
        return True
    return False

def getUserWallet(w3Provider, contractAddress, abi, webName):
    contact_list = w3Provider.eth.contract(address=contractAddress, abi=abi)
    return contact_list.functions.getWallet(webName).call()

def getUserEmail(w3Provider, contractAddress, abi, webName):
    contact_list = w3Provider.eth.contract(address=contractAddress, abi=abi)
    return contact_list.functions.getEmail(webName).call()

def getUserDni(w3Provider, contractAddress, abi, webName):
    contact_list = w3Provider.eth.contract(address=contractAddress, abi=abi)
    return contact_list.functions.getDni(webName).call()

def getUserName(w3Provider, contractAddress, abi, webName):
    contact_list = w3Provider.eth.contract(address=contractAddress, abi=abi)
    return contact_list.functions.getName(webName).call()

def getUserSurname(w3Provider, contractAddress, abi, webName):
    contact_list = w3Provider.eth.contract(address=contractAddress, abi=abi)
    return contact_list.functions.getSurname(webName).call()

def getUserGender(w3Provider, contractAddress, abi, webName):
    contact_list = w3Provider.eth.contract(address=contractAddress, abi=abi)
    return contact_list.functions.getGender(webName).call()

def getUserBirthday(w3Provider, contractAddress, abi, webName):
    contact_list = w3Provider.eth.contract(address=contractAddress, abi=abi)
    return contact_list.functions.getBirthday(webName).call()

def getUserAddress(w3Provider, contractAddress, abi, webName):
    contact_list = w3Provider.eth.contract(address=contractAddress, abi=abi)
    return contact_list.functions.getAddress(webName).call()

def getUserCity(w3Provider, contractAddress, abi, webName):
    contact_list = w3Provider.eth.contract(address=contractAddress, abi=abi)
    return contact_list.functions.getCity(webName).call()

def getUserPostalCode(w3Provider, contractAddress, abi, webName):
    contact_list = w3Provider.eth.contract(address=contractAddress, abi=abi)
    return contact_list.functions.getPostalCode(webName).call()

def getUserCountry(w3Provider, contractAddress, abi, webName):
    contact_list = w3Provider.eth.contract(address=contractAddress, abi=abi)
    return contact_list.functions.getCountry(webName).call()

def getUserPhoneNumber(w3Provider, contractAddress, abi, webName):
    contact_list = w3Provider.eth.contract(address=contractAddress, abi=abi)
    return contact_list.functions.getPhoneNumber(webName).call()

def getUserIG(w3Provider, contractAddress, abi, webName):
    contact_list = w3Provider.eth.contract(address=contractAddress, abi=abi)
    return contact_list.functions.getIgUsername(webName).call()

def getUserTw(w3Provider, contractAddress, abi, webName):
    contact_list = w3Provider.eth.contract(address=contractAddress, abi=abi)
    return contact_list.functions.getTwUsername(webName).call()

def getUserCreditCard(w3Provider, contractAddress, abi, webName):
    contact_list = w3Provider.eth.contract(address=contractAddress, abi=abi)
    return contact_list.functions.getCreditCard(webName).call()

def functionParamsCall(UserParams, w3Provider, contractAddress, abi, webName):    
    output = []
    paramList = []
    if UserParams:
        for x in UserParams:
            paramList.append('getUser'+ x)

    for x in paramList:
        param = globals() [x] (w3Provider,contractAddress,abi, webName)
        output.append(param)

    return output
