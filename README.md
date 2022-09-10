# SignUpBlockchain
Decentralized Digital Identity proof of concept implemented for degree thesis. 

# Requisites
---------------------------------------------------------------------
* Python 3.9.13 or higher
* Windows OS
* Ganache UI installed

# Running the project example
---------------------------------------------------------------------
IMPORTANT: Set the current directory inside virtualEnviroment folder to run the apps

	git clone https://github.com/pablosantos1106/SignUpBlockchain.git    
	cd virtualEnviroment                                                  #Access to virtual enviroment folder
	.\Scripts\activate.bat                                                #Run activate file inside Scripts folder

## Running the User digital identity management system

	.\runSSI.bat					# Runs User SSI app in 127.0.0.1:5000
    
## Running the External User Registration System 
       
	.\runPcShop.bat					# Runs Pc Shop flask app 127.0.0.1:5001
	.\runBiblioteca.bat				# Runs Biblioteca flask app in 127.0.0.1:5002

