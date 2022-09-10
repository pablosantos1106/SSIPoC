from Web2 import db, create_app
import os

path = os.getcwd() + "/Web2/db.sqlite"

if os.path.exists(path):
  os.remove(path)
  print('Eliminado el archivo db.sqlite')

db.create_all(app=create_app()) # pass the create_app result so Flask-SQLAlchemy gets the configuration.
print('Creado nuevo archivo "db.sqlite"')
