# SSIPoC
Decentralized Digital Identity proof of concept implemented for degree thesis. 

# Requisites
---------------------------------------------------------------------
* Python 3.9.13 version installed
* Windows OS
* Ganache UI installed

# Running the project example
---------------------------------------------------------------------
IMPORTANT: Set the current directory inside virtualEnviroment folder to run the apps

	git clone https://github.com/pablosantos1106/SignUpBlockchain.git    
	cd SignUpBlockchain/virtualEnviroment                                 #Access to virtual enviroment folder
	pip install -r requirements.txt                                       #Install the necessary python packages

## Running the User Digital Identity Management System (UDIMS)

	.\runSSI.bat					# Runs User SSI app in 127.0.0.1:5000
 
Deploy a **one-node blockchain** with Ganache UI tool and connect it to UDIMS. 

## Running the External User Registration System 
       
	.\runPcShop.bat					# Runs Pc Shop flask app 127.0.0.1:5001
	.\runBiblioteca.bat				# Runs Biblioteca flask app in 127.0.0.1:5002
