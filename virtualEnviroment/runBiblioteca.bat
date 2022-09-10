:: Run user SGIDU flask app 
SET FLASK_APP=Web2
SET FLASK_DEBUG=0

.\Scripts\python.exe .\Web2/createDataBase.py
.\Scripts\flask.exe run -p 5002