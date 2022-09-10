:: Run user SGIDU flask app 
SET FLASK_APP=Web1
SET FLASK_DEBUG=0

.\Scripts\python.exe .\Web1/createDataBase.py
.\Scripts\flask.exe run -p 5001