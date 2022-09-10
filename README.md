# SignUpBlockchain
Prototipo de método de registro basado en blockchain.

# Running the project example
---------------------------------------------------------------------

## Clone the repository and run python virtual enviroment 
	git clone https://github.com/pablosantos1106/SignUpBlockchain.git     #Clone the repository
	cd virtualEnviroment                                                  #Access to virtual enviroment folder
    Scripts/activate                                                      #Run activate file inside Scripts folder
  
## Deploy blockchain with Ganache tool
Install the ganache UI and deploy a new ethereum blockchain with Ganache.

## Running the User digital identity management system
  ### Run flask app
    cd virtualEnviroment                                # Its important to execute de next commands inside this folder               
    SET FLASK_APP=User|| export FLASK_APP=User          # Set the flask app enviroment variable
    SET FLASK_DEBUG=0 ||export FLASK_APP=0              # Set the production mode variable
    .\Scripts\flask.exe -p <port>                       # Run the app in the input port
    
## Running the External User Registration System 
	### Run Pc Shop system 
     cd virtualEnviroment                               # Its important to execute de next commands inside this folder 
    .\Scripts\python.exe .\Web1/createDataBase.py       # Create the Pc Shop database db.sqlite file
    SET FLASK_APP=Web1                                  # Set the flask app enviroment variable
    SET FLASK_DEBUG=0                                   # Set the flask production mode variable
    .\Scripts\flask.exe -p run <another port>           # Run the app in the input port


  ### Run Biblioteca system 
     cd virtualEnviroment                                # Important to set the route in thsi folder before run flask app
    .\Scripts\python.exe .\Web2/createDataBase.py       # Create the Biblioteca database db.sqlite file
    SET FLASK_APP=Web2                                  # Set the flask app enviroment variable
    SET FLASK_DEBUG=0                                   # Set the flask production mode variable
    .\Scripts\flask.exe -p run <another port>           # Run the app in the input port


In Unix use the "export" to set the FLASK_APP and FLASK_DEBUG enviroment variables. Example: export FLASK_APP=User
