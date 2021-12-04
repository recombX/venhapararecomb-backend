from os import name
import xml.etree.ElementTree as ET
import json
from re import match
import database

def parsing_and_saving(file):
    con = database.create_connection('my-test.db')
    database.drop_tables(con)
    database.initiate_tables(con)

    tree = ET.parse(file)
    root = tree.getroot()
    namespace = match(r'\{.*\}', root.tag).group(0)

    # Iterando sobre cada nota fiscal
    for nfe in root.findall(f'{namespace}NFe'):
        emit = nfe[0].find(f'{namespace}emit')
        dest = nfe[0].find(f'{namespace}dest')

        # CPF/CNPJ do fornecedor
        cpf_or_cnpj_emit = emit.find(f'{namespace}CNPJ')
        if cpf_or_cnpj_emit == None: emit.find(f'{namespace}CPF')

        cpf_or_cnpj_emit = cpf_or_cnpj_emit.text

        # CPF/CNPJ do cliente
        cpf_or_cnpj_dest = dest.find(f'{namespace}CNPJ')
        if cpf_or_cnpj_dest == None: dest.find(f'{namespace}CPF')

        cpf_or_cnpj_dest = cpf_or_cnpj_dest.text

        # Data de vencimento e valor do boleto
        cobr = (nfe[0].find(f'{namespace}cobr'))
        valor = (cobr.find(f'{namespace}fat')).find(f'{namespace}vLiq').text
        vencimento = (cobr.find(f'{namespace}dup')).find(f'{namespace}dVenc').text

        sql = 'INSERT INTO NOTAS_FISCAIS (cnpj_or_cpf_emit, cnpj_or_cpf_client, dvenc, valor) VALUES (?, ?, ?, ?)'
        data_tuple = (cpf_or_cnpj_emit, cpf_or_cnpj_dest, vencimento, float(valor))

        database.execute_query(sql, data_tuple, con)
        
        # Nome e Endereço do Cliente
        client_name = dest.find(f'{namespace}xNome').text
        ender_dest = dest.find(f'{namespace}enderDest')
        rua = ender_dest.find(f'{namespace}xLgr').text
        numero = ender_dest.find(f'{namespace}nro').text
        bairro = ender_dest.find(f'{namespace}xBairro').text
        municipio = ender_dest.find(f'{namespace}xMun').text

        client_address = rua + ', ' + numero + '. ' + bairro + ', ' + municipio + '.'

        # Inserir na tabela de clientes (cpf/cnpj_cliente, cpf/cnpj_emit, nome, endereco)
        sql2 = 'INSERT INTO CLIENTES (cnpj_or_cpf_client, cnpj_or_cpf_emit, nome, endereco) VALUES (?, ?, ?, ?)'
        data_tuple2 = (cpf_or_cnpj_dest, cpf_or_cnpj_emit, client_name, client_address)
        
        database.execute_query(sql2, data_tuple2, con)
    con.close()

def busca_query(cpf_or_cnpj, query):
    con = database.create_connection('my-test.db')
    data = (cpf_or_cnpj,)
    result = database.execute_and_print(query, data, con)
    con.close()
    return result

# def busca1(cpf_or_cnpj):
#     con = database.create_connection('my-test.db')
#     request = 
#     data = (cpf_or_cnpj,)
#     result = database.execute_and_print(request, data, con)
#     con.close()
#     return result

# def busca2(cpf_or_cnpj):
#     con = database.create_connection('my-test.db')
#     request = 
#     data = (cpf_or_cnpj,)
#     result = database.execute_and_print(request, data, con)
#     con.close()
#     return result
    
#06273476000182