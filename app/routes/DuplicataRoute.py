from datetime import datetime
from flask import make_response, request, jsonify
from app.models.Duplicata import Duplicata
from app import app, db
from app.models.Fornecedor import Fornecedor
from app.models.NotaFiscal import NotaFiscal

@app.route("/duplicata", methods = ['POST'])
def create_duplicata():
    data = request.json()

    if data:
        try:
            duplicata = Duplicata.query.get(data["id"])

            if duplicata is not None:
                return make_response("Erro: Duplicata já cadastrada.", 409)
            
            duplicata = duplicata(id=data["id"],
                                nfe=data["nfeId"],
                                valor=data["valor"],
                                dataVencimento=datetime.strptime(data["vencimento"], "%Y-%m-%d").date())
            duplicata.add()
            
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

@app.route("/duplicata", methods = ['GET'])
def read_duplicata():
    # Uma lógica simples, realizando uma querie para obter todos
    # os registros de duplicatas no banco de dados e retornando como um JSON
    try:
        duplicatas = []
        for duplicata in Duplicata.query.all():
            duplicatas.append(
                {"id": duplicata.id,
                "nfeId": duplicata.nfe,
                "valor": duplicata.valor,
                "vencimento": duplicata.dataVencimento}
            )
        return make_response(jsonify(duplicatas), 200)
    except Exception as e:
        app.logger.error(f"Erro na requisição: {str(e)}")
        return make_response("Erro interno no servidor.", 500)

@app.route("/duplicata/<fornecedor_id>", methods = ['GET'])
def read_duplicata_by_fornecedor_id(fornecedor_id):
    # Uma lógica simples, realizando uma querie para obter todos
    # os registros de duplicatas no banco de dados e retornando como um JSON
    try:
        fornecedor = Fornecedor.query.get(fornecedor_id)
        if fornecedor is None:
            return make_response("Fornecedor não encontrado",404)

        duplicatas = []
        for duplicata in Duplicata.query.join(NotaFiscal).filter(NotaFiscal.fornecedor_id == fornecedor.id).all():
            duplicatas.append(
                {"id": duplicata.id,
                "nfeId": duplicata.nfe,
                "valor": duplicata.valor,
                "vencimento": duplicata.dataVencimento}
            )
        return make_response(jsonify(duplicatas), 200)
    except Exception as e:
        app.logger.error(f"Erro na requisição: {str(e)}")
        return make_response("Erro interno no servidor.", 500)

@app.route("/duplicata", methods = ['PUT'])
def update_duplicata():
    data = request.get_json()
    duplicata = duplicata.query.get(data["id"])

    if duplicata is not None:
        duplicata.nfe = data["nfeId"]
        duplicata.valor = data["valor"]
        duplicata.dataVencimento = datetime.strptime(data["vencimento"], "%Y-%m-%d").date()
        return make_response("Duplicata alterada com sucesso.", 200)
    return make_response("Duplicata não encontrada.", 404)

@app.route("/duplicata", methods = ['DELETE'])
def delete_duplicata():
    data = request.get_json()
    duplicata = Duplicata.query.get(data["id"])

    if duplicata is not None:
        duplicata.delete()
        db.session.commit()
        return make_response("Duplicata excluída com sucesso.", 200)
    return make_response("Duplicata não encontrada.", 404)
