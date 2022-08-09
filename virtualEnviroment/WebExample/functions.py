from .models import User
from flask import flash
from web3 import Web3

def usernameAlreadyExists(username):
    
    #checks if username already exists
    user = User.query.filter_by(username=username).first() 

    if user:
        flash('Username already exists')
        print('Uername')
        return True
    return False


def blockchainUrlUsed (url, port):

    #Check if the input url is already registered by another user
    databaseUrl =  User.query.filter_by(url=url).first()

    #If exists, check the port on which the blockchain is deployed
    if databaseUrl:
        databasePort = User.query.filter_by(port=port).first() 
        if databasePort:
            flash('This url and port combination is currently in use, please select another')
            return True
    return False

def getProvider (url, port):
    return Web3(Web3.HTTPProvider(url + ':' + port))

def checkBlockchainConnection(provider):

    if not provider.isConnected():
        flash('Blockchain connection is not posible, please check the url and port input')


    return provider.isConnected()

