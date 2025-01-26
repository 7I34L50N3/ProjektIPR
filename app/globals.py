from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Table, ForeignKey

# Inicjalizacja aplikacji Flask i SQLAlchemy
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rootpassword@79.191.247.8:3307/app_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rootpassword@127.0.0.1:3307/app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

user_group_association = Table(
    'user_group', db.Model.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('group_id', Integer, ForeignKey('groups.id'), primary_key=True)
)
