# -*- coding: utf-8 -*-
import unittest, json
import datetime
from app import app, db, Conta,ContaCorrente, ContaPoupanca,Extrato

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

            conta = Conta(titular='João Silva')
            db.session.add(conta)
            db.session.commit()
            
            conta_corrente = ContaCorrente(conta_id= conta.id)
            db.session.add(conta_corrente)
            db.session.commit()
            conta_poupanca = ContaPoupanca(conta_id= conta.id)
            db.session.add(conta_poupanca)
            db.session.commit()
            extrato_poupanca = Extrato(data=datetime.datetime.utcnow(), descricao='Depósito2', valor=1, conta=conta_poupanca.id, tipo_conta='poupanca', saldo = 1)
            db.session.add(extrato_poupanca)
            db.session.commit()
            extrato_cc = Extrato(data=datetime.datetime.utcnow(), descricao='Depósito1', valor=1000, conta=conta_corrente.id, tipo_conta='conta_corrente', saldo = 1000)
            db.session.add(extrato_cc)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_consultar_saldo_sucesso(self):
        response = self.app.get('/saldo?conta_id=1&tipo=conta_corrente')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertIn('saldo', data)

    def test_consultar_saldo_falha(self):
        response = self.app.get('/saldo?conta_id=99&tipo=conta_corrente')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertIn('mensagem', data)

    def test_consultar_extrato_sucesso(self):
        response = self.app.get('/extrato?conta_id=1&tipo=conta_corrente')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertIn('extrato', data)

    def test_consultar_extrato_falha(self):
        response = self.app.get('/extrato?conta_id=99&tipo=conta_corrente')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertIn('mensagem', data)

    def test_transferencia_sucesso(self):
        data = {
            'conta': 1,
            'tipo_conta_destino': 'poupanca',
            'valor': 500
        }
        response = self.app.post('/transferencia', json=data)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertIn('mensagem', data)

    def test_transferencia_falha(self):
        data = {
            'conta': 1,
            'tipo_conta_destino': 'zuado',
            'valor': 2000
        }
        response = self.app.post('/transferencia', json=data)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertIn('mensagem', data)

if __name__ == '__main__':
    unittest.main()






