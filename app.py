from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

from models import Conta, ContaCorrente, ContaPoupanca, Extrato
from routes import *


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

