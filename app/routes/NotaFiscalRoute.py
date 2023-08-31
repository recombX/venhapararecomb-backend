from sqlalchemy.exc import IntegrityError
from flask import make_response, request, jsonify
from app.models.NotaFiscal import NotaFiscal
from app.models.Cliente import Cliente
from app.models.Fornecedor import Fornecedor
from app.models.Duplicata import Duplicata
from app import app, db
import xmltodict
from datetime import datetime

@app.route("/nfe/xml", methods = ['POST'])
def create_nfe_by_xml():
    xml_file = request.files['xml_file']

    if xml_file:
        xml_data = xml_file.stream.read()
        xml_dict = xmltodict.parse(xml_data)
        try:   
            # Aqui extraímos os dados necessários do nosso arquivo XML
            nfe_data = xml_dict["nfeProc"]["NFe"]["infNFe"]
            emit_data = xml_dict["nfeProc"]["NFe"]["infNFe"]["emit"]
            dest_data = xml_dict["nfeProc"]["NFe"]["infNFe"]["dest"]
            dup_data = xml_dict["nfeProc"]["NFe"]["infNFe"]["cobr"]["dup"]

            # Aqui temos uma lógica simples para descobrir se utilizaremos
            # CNPJ ou CPF
            fornecedor_tipo = "CPF" if "CPF" in emit_data.keys() else "CNPJ"
            cliente_tipo = "CPF" if "CPF" in emit_data.keys() else "CNPJ"

            # Nessa parte é importante verificar se tanto o cliente quanto o fornecedor
            # já estão cadastrados no banco de dados, para evitar uma exceção
            cliente = Cliente.query.get(dest_data[cliente_tipo])
            fornecedor = Fornecedor.query.get(emit_data[fornecedor_tipo])

            if cliente is None:
                # Essa não é a melhor implementação para armazenar endereço em um banco de dados
                # porém para evitar um complexidade a mais, optei por essa opção de inserir estáticamente
                endereco = f'{dest_data["enderDest"]["xLgr"]}, {dest_data["enderDest"]["nro"]}, {dest_data["enderDest"]["xBairro"]}, {dest_data["enderDest"]["xMun"]}, {dest_data["enderDest"]["UF"]}, {dest_data["enderDest"]["xPais"]}'
                cliente = Cliente(id=dest_data[cliente_tipo], nome=dest_data["xNome"], endereco=endereco, cep=dest_data["enderDest"]["CEP"])
                cliente.add()

            if fornecedor is None:
                fornecedor = Fornecedor(id=emit_data[fornecedor_tipo], nome=emit_data["xNome"])
                fornecedor.add()

            nfe = NotaFiscal(id=nfe_data["@Id"],fornecedor=fornecedor, cliente=cliente)
            nfe.add() 

            ## Verificando se é uma lista de duplicatas, ou apenas uma unidade
            if isinstance(dup_data, list):
                for dup in dup_data:
                    duplicata = Duplicata(valor=dup["vDup"],
                                        dataVencimento=datetime.strptime(dup["dVenc"], "%Y-%m-%d").date(),
                                        nfe=nfe_data["@Id"])
                    duplicata.add()
            else:
                duplicata = Duplicata(valor=dup_data["vDup"],
                                        dataVencimento=datetime.strptime(dup_data["dVenc"], "%Y-%m-%d").date(),
                                        nfe=nfe_data["@Id"])
                duplicata.add()

            db.session.commit()
            return make_response("Dados armazenados com sucesso.", 201)
        except KeyError:
            return make_response("Erro: Chave ausente nos dados do XML.", 400)
        except IntegrityError:
            db.session.rollback()
            return make_response("Erro: Identificador já cadastrado.", 409)
        except Exception as e:
            # Logar a exceção para depuração
            app.logger.error(f"Erro na requisição: {e}")
            db.session.rollback()
            return make_response("Erro interno no servidor.", 500)
    return make_response("Erro: Nenhum arquivo fornecido.", 400)

@app.route("/nfe", methods = ['POST'])
def create_nfe():
    data = request.json()

    if data:
        try:
            # Nessa parte é importante verificar se tanto o cliente quanto o fornecedor
            # já estão cadastrados no banco de dados, para evitar uma exceção
            cliente = Cliente.query.get(data["id_cliente"])
            fornecedor = Fornecedor.query.get(data["id_fornecedor"])

            if cliente is None:
                return make_response("Cliente não cadastrado.",404)

            if fornecedor is None:
                return make_response("Fornecedor não cadastrado.",404)
            
            nfe = NotaFiscal(id=data["id"], fornecedor=fornecedor, cliente=cliente)
            nfe.add()
            db.session.commit()
            return make_response("Dados armazenados com sucesso.", 201)
        except KeyError:
            return make_response("Erro: Chave ausente na requisição.", 400)
        except IntegrityError:
            db.session.rollback()
            return make_response("Erro: Identificador já cadastrado.", 409)
        except Exception as e:
            # Logar a exceção para depuração
            app.logger.error(f"Erro na requisição: {e}")
            db.session.rollback()
            return make_response("Erro interno no servidor.", 500)
    return make_response("Erro: Nenhum dado fornecido.", 400)

@app.route("/nfe", methods = ['GET'])
def read_nfe():
    # Uma lógica simples, realizando uma querie para obter todos
    # os registros de NFe no banco de dados e retornando como um JSON
    try:
        notas_fiscais = []
        for nota_fiscal in NotaFiscal.query.all():
            notas_fiscais.append(
                {"id": nota_fiscal.id,
                "cliente_id": nota_fiscal.cliente_id,
                "forncedor_id": nota_fiscal.fornecedor_id}
            )
        return make_response(jsonify(notas_fiscais), 200)
    except Exception as e:
        app.logger.error(f"Erro na requisição: {str(e)}")
        return make_response("Erro interno no servidor.", 500)

@app.route("/nfe", methods = ['PUT'])
def update_nfe():
    data = request.get_json()
    nfe = NotaFiscal.query.get(data["id"])

    if nfe is not None:
        nfe.cliente_id = data["cliente_id"]
        nfe.fornecedor_id = data["fornecedor_id"]
        db.session.commit()
        return make_response("Nota Fiscal alterada com sucesso.", 200)
    return make_response("Nota Fiscal não encontrada.", 404)

@app.route("/nfe", methods = ['DELETE'])
def delete_nfe():
    data = request.get_json()
    nfe = NotaFiscal.query.get(data["id"])

    if nfe is not None:
        nfe.delete()
        db.session.commit()
        return make_response("Nota Fiscal excluída com sucesso.", 200)
    return make_response("Nota Fiscal não encontrada.", 404)
