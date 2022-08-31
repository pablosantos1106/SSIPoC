from Web1 import db, create_app, models
import os

path = os.getcwd() + "/WebExample/db.sqlite"

if os.path.exists(path):
  os.remove(path)
  print('"db.sqlite" file deleted ')

db.create_all(app=create_app()) # pass the create_app result so Flask-SQLAlchemy gets the configuration.
print('New "db.sqlite" file created')
