from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)


DATABSE_URI = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='Yura', password='1111', server='localhost', database='python_project_db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABSE_URI
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

import application.views
