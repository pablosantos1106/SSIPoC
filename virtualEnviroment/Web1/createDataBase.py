from Web1 import db, create_app, models
import os

path = os.getcwd() + "/Web1/db.sqlite"

if not os.path.exists(os.getcwd() + "/Web1/db.sqlite"):
  db.create_all(app=create_app()) # pass the create_app result so Flask-SQLAlchemy gets the configuration.
  print('New "db.sqlite" file created')