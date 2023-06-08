from flask import request, jsonify
from app import app, db
from models import Conta, ContaCorrente, ContaPoupanca, Extrato
import datetime
from sqlalchemy import extract


@app.route("/saldo", methods=["GET"])
def consultar_saldo():
    conta_id = request.args.get("conta_id")
    tipo = request.args.get("tipo")

    if tipo == "conta_corrente":
        conta = ContaCorrente.query.filter_by(conta_id=conta_id).first()
    elif tipo == "conta_poupanca":
        conta = ContaPoupanca.query.filter_by(conta_id=conta_id).first()
    else:
        return jsonify({"mensagem": "Tipo de conta inválido"}), 400

    if not conta:
        return jsonify({"mensagem": "Conta não encontrada"}), 404

    return jsonify({"saldo": conta.saldo})


@app.route("/extrato", methods=["GET"])
def consultar_extrato():
    conta_id = request.args.get("conta_id")
    tipo = request.args.get("tipo")

    data_atual = datetime.datetime.now()
    primeiro_dia_mes = datetime.datetime(data_atual.year, data_atual.month, 1)
    ultimo_dia_mes = datetime.datetime(
        data_atual.year, data_atual.month + 1, 1
    ) - datetime.timedelta(days=1)
    if tipo == "conta_corrente":
        conta = ContaCorrente.query.filter_by(conta_id=conta_id).first()
    elif tipo == "conta_poupanca":
        conta = ContaPoupanca.query.filter_by(conta_id=conta_id).first()
    else:
        return jsonify({"mensagem": "Tipo de conta inválido"}), 400

    if conta:
        registros_mes_corrente = (
            Extrato.query.filter_by(conta_id=1)
            .filter(
                extract("year", Extrato.data) == data_atual.year,
                extract("month", Extrato.data) == data_atual.month,
                extract("day", Extrato.data).between(
                    primeiro_dia_mes.day, ultimo_dia_mes.day
                ),
            )
            .all()
        )
        return {"extrato": [extrato.serialize() for extrato in registros_mes_corrente]}
    else:
        return {"mensagem": "Conta não encontrada"}, 404


@app.route("/transferencia", methods=["POST"])
def transferencia():
    data = request.json
    id = data["conta"]
    tipo_conta_destino = data["tipo_conta_destino"]
    valor = data["valor"]
    if tipo_conta_destino == "conta_corrente":
        conta_origem = ContaPoupanca.query.filter_by(conta_id=id).first()
        conta_destino = ContaCorrente.query.filter_by(conta_id=id).first()
    elif tipo_conta_destino == "poupanca":
        conta_origem = ContaCorrente.query.filter_by(conta_id=id).first()
        conta_destino = ContaPoupanca.query.filter_by(conta_id=id).first()
    else:
        return {"mensagem": "tipo de transferência inválido"}, 400

    if conta_origem and conta_destino:
        if conta_origem.saldo >= valor:
            conta_origem.saldo -= valor
            conta_destino.saldo += valor
            extrato_origem = Extrato(data=datetime.datetime.utcnow(), descricao='Depósito2', valor=-valor, conta=conta_origem.id, tipo_conta=conta_origem.__tablename__,saldo = conta_origem.saldo)
            extrato_destino = Extrato(data=datetime.datetime.utcnow(), descricao='Depósito1', valor=valor, conta=conta_destino.id, tipo_conta=conta_destino.__tablename__, saldo = conta_destino.saldo)

            db.session.add(extrato_origem)
            db.session.add(extrato_destino)

            db.session.commit()
            return {"mensagem": "Transferência realizada com sucesso"}

        else:
            return {"mensagem": "Saldo insuficiente"}, 400
    else:
        return {"mensagem": "Conta não encontrada"}, 404
