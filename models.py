from app import db
import datetime

class Conta(db.Model):
    __tablename__ = 'conta'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    titular = db.Column(db.String(100), nullable=False)
    # contas_corrente = db.relationship('ContaCorrente', backref='conta', lazy=True, uselist=False, primaryjoin="Conta.id == ContaCorrente.conta_id")
    # contas_poupanca = db.relationship('ContaPoupanca', backref='conta', lazy=True, uselist=False, primaryjoin="Conta.id == ContaPoupanca.conta_id")
    def __init__(self,  titular):
        self.titular = titular

class Extrato(db.Model):
    __tablename__ = 'extrato'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    conta_id = db.Column(db.Integer, db.ForeignKey('conta.id'), nullable=False, autoincrement=True)
    tipo_conta = db.Column(db.Integer)
    data = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    descricao = db.Column(db.String(100))
    valor = db.Column(db.Float)
    saldo = db.Column(db.Float)

    def __init__(self, data, descricao, valor, conta,tipo_conta, saldo):
        self.data = data
        self.descricao = descricao
        self.valor = valor
        self.conta_id = conta
        self.saldo = saldo
        self.tipo_conta = tipo_conta

    def serialize(self):
        return {
            'data': self.data,
            'descricao': self.descricao,
            'valor': self.valor,
            'saldo': self.saldo
        }

class ContaCorrente(db.Model):
    __tablename__ = 'conta_corrente'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    saldo = db.Column(db.Float, nullable=False)
    conta_id = db.Column(db.Integer, db.ForeignKey('conta.id'), nullable=False)
    def __init__(self,conta_id):
        self.saldo = 1000
        self.conta_id = conta_id

class ContaPoupanca(db.Model):
    __tablename__ = 'conta_poupanca'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    saldo = db.Column(db.Float, nullable=False)
    conta_id = db.Column(db.Integer, db.ForeignKey('conta.id'), nullable=False)
    def __init__(self,conta_id):
        self.saldo = 1
        self.conta_id = conta_id
   
