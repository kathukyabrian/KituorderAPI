from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# app instantiation
app = Flask(__name__)

cors = CORS(app)

# app configs
app.config['SECRET_KEY'] = 'brian@2020kituorder'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///kituorder'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['CORS_HEADERS'] = 'Content-Type'

# database instantiation
db = SQLAlchemy(app)