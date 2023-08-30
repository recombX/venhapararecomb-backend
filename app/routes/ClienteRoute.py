from sqlalchemy.exc import IntegrityError
from flask import make_response, request, jsonify
from app.models.Cliente import Cliente
from app.models.Fornecedor import Fornecedor
from app.models.NotaFiscal import NotaFiscal

from app import app, db

@app.route("/cliente", methods = ['POST'])
def create_cliente():
    data = request.json()

    if data:
        try:
            cliente = Cliente.query.get(data["id"])

            if cliente is not None:
                return make_response("Erro: Cliente já cadastrado.", 409)
            
            cliente = Cliente(id=data["id"], nome=data["nome"], cep=data["cep"])
            cliente.add()
            
            db.session.commit()
            return make_response("Dados armazenados com sucesso.", 201)
        except KeyError:
            return make_response("Erro: Chave ausente na requisição.", 400)
        except Exception as e:
            # Logar a exceção para depuração
            app.logger.error(f"Erro na requisição: {e}")
            db.session.rollback()
            return make_response("Erro interno no servidor.", 500)
    return make_response("Erro: Nenhum dado fornecido.", 400)

@app.route("/cliente", methods = ['GET'])
def read_cliente():
    # Uma lógica simples, realizando uma querie para obter todos
    # os registros de clientes no banco de dados e retornando como um JSON
    try:
        clientes = []
        for cliente in Cliente.query.all():
            clientes.append(
                {"id": cliente.id,
                "nome": cliente.nome,
                "cep": cliente.cep}
            )
        return make_response(jsonify(clientes), 200)
    except Exception as e:
        app.logger.error(f"Erro na requisição: {str(e)}")
        return make_response("Erro interno no servidor.", 500)

@app.route("/cliente/<fornecedor_id>", methods = ['GET'])
def read_cliente_by_fornecedor_id(fornecedor_id):
    try:
        fornecedor = Fornecedor.query.get(fornecedor_id)
    
        if fornecedor is None:
            return make_response("Fornecedor não encontrado",404)
        
        clientes = []
        for cliente in Cliente.query.join(NotaFiscal).filter(NotaFiscal.fornecedor_id == fornecedor.id).all():
            clientes.append(
                {"id": cliente.id,
                "nome": cliente.nome,
                "cep": cliente.cep}
            )
        return make_response(jsonify(clientes), 200)
    except Exception as e:
        app.logger.error(f"Erro na requisição: {str(e)}")
        return make_response("Erro interno no servidor.", 500)

@app.route("/cliente", methods = ['PUT'])
def update_cliente():
    data = request.get_json()
    cliente = Cliente.query.get(data["id"])

    if cliente is not None:
        cliente.nome = data["nome"]
        cliente.cep = data["cep"]
        db.session.commit()
        return make_response("Cliente alterado com sucesso.", 200)
    return make_response("Cliente não encontrado.", 404)

@app.route("/cliente", methods = ['DELETE'])
def delete_cliente():
    data = request.get_json()
    cliente = Cliente.query.get(data["id"])

    if cliente is not None:
        cliente.delete()
        db.session.commit()
        return make_response("Cliente excluído com sucesso.", 200)
    return make_response("Cliente não encontrado.", 404)
