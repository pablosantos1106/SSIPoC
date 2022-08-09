from web3 import Web3
import json
import os
import dni
import re
from solcx import compile_standard, install_solc
from flask import request, flash
import datetime

def validateWallet(provider, wallet):
    if not provider.isAddress(wallet):
        flash('Invalid wallet address: '+ wallet)
        return False 
    return True

def validateDni(value):
    if not dni.is_valid(value):
        flash('Invalid dni: '+ value)  
        return False
    return True

def validatePhoneNumber(phoneNumber):
    if (len(phoneNumber) != 9):
        flash('PhoneNumber is invalid: ' + phoneNumber )
        return False 
    return True

def validateCreditCard (creditCard):
    pattern = '[0-9]{16}|[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}$'
    if not re.match(pattern, creditCard):
        flash('Invalid credit card:' + creditCard)
        return False 
    return True

def atLeastOneChecked(valueList):
    if (len(valueList) == 0):
        flash('Please select at least one value')
        return False
    return True


def validateMultipleCheckboxOptions(valueList):
    if (len(valueList) > 1):
        flash('Please select only one option')
        return False
    return atLeastOneChecked(valueList)

def validateUserInputData (provider, wallet, dni, phoneNumber, creditCard, gender): 
    return validateDni(dni) and validatePhoneNumber(phoneNumber) and  validateCreditCard(creditCard) and validateMultipleCheckboxOptions(gender) and validateWallet (provider, wallet)

def getProvider (URL):
    return Web3(Web3.HTTPProvider(URL))

def getCheckboardValues(values):
    val = []
    for x in values:
        if (request.form.get(x) == 'on'):
            val.append(x)
    return val


def deployContract (w3Provider, contractPath, outputPath, chain_id, address, privateKey): 

    with open(contractPath, "r") as file:
        contract = file.read()

    install_solc("0.8.15")

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"RegisterData.sol": {"content": contract}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]  # output needed to interact with and deploy contract
                    }
                }
            },
        },
        solc_version="0.8.15",
    )

    with open(outputPath, "w") as file:
        json.dump(compiled_sol, file)

    # get bytecode
    bytecode = compiled_sol["contracts"]["RegisterData.sol"]["RegisterData"]["evm"]["bytecode"]["object"]

    # get abi
    abi = json.loads(compiled_sol["contracts"]["RegisterData.sol"]["RegisterData"]["metadata"])["output"]["abi"]

    # Create the contract in Python
    contract = w3Provider.eth.contract(abi=abi, bytecode=bytecode)
    # Get the number of latest transaction
    nonce = w3Provider.eth.getTransactionCount(address)

    # build transaction
    transaction = contract.constructor(address, address).buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": w3Provider.eth.gas_price,
            "from": address,
            "nonce": nonce,
        }
    )

    # Sign the transaction
    sign_transaction = w3Provider.eth.account.sign_transaction(transaction, private_key=privateKey)
    print("Deploying Contract!")

    # Send the transaction
    transaction_hash = w3Provider.eth.send_raw_transaction(sign_transaction.rawTransaction)

    # Wait for the transaction to be mined, and get the transaction receipt
    print("Waiting for transaction to finish...")
    transaction_receipt = w3Provider.eth.wait_for_transaction_receipt(transaction_hash)
    print(f"Done! Contract deployed to {transaction_receipt.contractAddress}")

    with open(outputPath, 'r') as f:
        data = json.load(f)
        data["contractAddress"] = transaction_receipt.contractAddress 

    os.remove(outputPath)

    with open(outputPath, 'w') as f:
        json.dump(data, f, indent=4)

    output = [abi, transaction_receipt.contractAddress]

    return output

def storeContract (w3Provider, chain_id, contractAddress, abi, userData, privateKey):
    wallet = userData['wallet']
    nonce = w3Provider.eth.getTransactionCount(wallet)
    contact_list = w3Provider.eth.contract(address=contractAddress, abi=abi)

    #Set the user data values
    #Create the data block
    setData1 = contact_list.functions.setData1(
        userData['wallet'],userData['email'],userData['dni'],userData['name'],userData['surname'],userData['gender'],
        userData['birthday'],userData['addr']
     ).buildTransaction({"chainId": chain_id, "from": wallet, "gasPrice": w3Provider.eth.gas_price, "nonce": nonce})
    
    # Sign the transaction
    sign_data1 = w3Provider.eth.account.sign_transaction(setData1, private_key=privateKey)

    # Send the transaction
    w3Provider.eth.send_raw_transaction(sign_data1.rawTransaction)

    #Create the data block
    setData2 = contact_list.functions.setData2(
        userData['city'],userData['postalCode'],userData['country'], userData['phoneNumber'],userData['igUsername'],userData['twUsername'],userData['creditCard']
        ).buildTransaction({"chainId": chain_id, "from": wallet, "gasPrice": w3Provider.eth.gas_price, "nonce": nonce+1})
    sign_data2 = w3Provider.eth.account.sign_transaction(setData2, private_key=privateKey)
    w3Provider.eth.send_raw_transaction(sign_data2.rawTransaction)


def getData(w3Provider, contractAddress, abi):
    contact_list = w3Provider.eth.contract(address=contractAddress, abi=abi)
    return contact_list.functions.getData().call()

def getContractRequiredInfo(PATH):
    with open(PATH) as jsonfile:
        data = json.load(jsonfile)
    output = []

    contractAddress = data["contractAddress"]
    abi= json.loads(data["contracts"]["RegisterData.sol"]["RegisterData"]["metadata"])["output"]["abi"]

    output.append(contractAddress)
    output.append(abi)
    return output

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

def mapBlockchainOutput(input):

    outputMapped = {"wallet":input[0], "email":input[1], "dni":input[2], "name":input[3], "surname":input[4], 
            "gender":input[5], "birthday": datetime.datetime.fromtimestamp(input[6]).date(), "address": input[7], "city":input[8], "postalCode": input[9], "country": input[10], 
            "phoneNumber":input[11], "igUsername":input[12], "twUsername":input[13], "creditCard":input[14]}
    return outputMapped

def getUserData(w3Provider, contractAddress, abi):
    contact_list = w3Provider.eth.contract(address=contractAddress, abi=abi)
    return contact_list.functions.getData().call()