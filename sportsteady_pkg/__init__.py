from flask import Flask 
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sportsteady_pkg import config

app = Flask(__name__,instance_relative_config=True)
app.config.from_pyfile("config.py")
app.config.from_object(config.LiveConfig)
csrf = CSRFProtect(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from sportsteady_pkg import routes, models
from sportsteady_pkg.routes import journalist_routes, user_routes, admin_routes

#import any other variable, object, module you would need in this app 

"""Things required here:
1.) instantiate an object of flask

2.) import your route

3.) load your config file if you wish to or load it on your server file(myapp.py)
"""