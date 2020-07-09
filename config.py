from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'brian@2020kituorder'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///kituorder'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)