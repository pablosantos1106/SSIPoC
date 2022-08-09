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

def getUserWallet(provider):
    return provider.eth.accounts[0]

def mapUserData(input):

    outputMapped = {"wallet":input[0], "email":input[1], "dni":input[2], "name":input[3], "surname":input[4], 
            "gender":input[5], "birthday": datetime.fromtimestamp(input[6]).date(), "address": input[7], "city":input[8], "postalCode": input[9], "country": input[10], 
            "phoneNumber":input[11], "igUsername":input[12], "twUsername":input[13], "creditCard":input[14]}
    return outputMapped
