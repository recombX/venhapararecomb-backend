from datetime import datetime
from flask import make_response, request, jsonify
from app.models.Fornecedor import Fornecedor
from app import app, db

@app.route("/fornecedor", methods = ['POST'])
def create_fornecedor():
    data = request.json()

    if data:
        try:
            fornecedor = Fornecedor.query.get(data["id"])

            if fornecedor is not None:
                return make_response("Erro: Fornecedor já cadastrado.", 409)
            
            fornecedor = Fornecedor(id=data["id"],nfe=data["nome"])
            fornecedor.add()
            
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

@app.route("/fornecedor", methods = ['GET'])
def read_fornecedor():
    # Uma lógica simples, realizando uma querie para obter todos
    # os registros de fornecedors no banco de dados e retornando como um JSON
    try:
        fornecedores = []
        for fornecedor in Fornecedor.query.all():
            fornecedores.append(
                {"id": fornecedor.id,
                "nome": fornecedor.nome}
            )
        return make_response(jsonify(fornecedores), 200)
    except Exception as e:
        app.logger.error(f"Erro na requisição: {str(e)}")
        return make_response("Erro interno no servidor.", 500)

@app.route("/fornecedor", methods = ['PUT'])
def update_fornecedor():
    data = request.get_json()
    fornecedor = Fornecedor.query.get(data["id"])

    if fornecedor is not None:
        fornecedor.nome = data["nome"]
        return make_response("Fornecedor alterado com sucesso.", 200)
    return make_response("Fornecedor não encontrado.", 404)

@app.route("/fornecedor", methods = ['DELETE'])
def delete_fornecedor():
    data = request.get_json()
    fornecedor = Fornecedor.query.get(data["id"])

    if fornecedor is not None:
        fornecedor.delete()
        db.session.commit()
        return make_response("Fornecedor excluído com sucesso.", 200)
    return make_response("Fornecedor não encontrado.", 404)
