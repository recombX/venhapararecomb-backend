from Database import Database
import os
from NotaFiscal import NotaFiscal

def create_db(database_str : str) -> Database:
    db = Database(database_str)

    sql_create_emitente_table = """ CREATE TABLE IF NOT EXISTS emitente (
                                        emitente_id text PRIMARY KEY,
                                        nome text NOT NULL
                                    ); """

    sql_create_destinador_table = """ CREATE TABLE IF NOT EXISTS destinador (
                                        destinador_id text PRIMARY KEY,
                                        nome text NOT NULL
                                    ); """                

    sql_create_endereco_destinador_table = """ CREATE TABLE IF NOT EXISTS endereco_destinador (
                                        destinador_endereco_id text PRIMARY KEY,
                                        destinador_id text,
                                        logradouro text NOT NULL,
                                        numero text NOT NULL,
                                        bairro text NOT NULL,
                                        municipio text NOT NULL,
                                        estado text NOT NULL,
                                        cep text NOT NULL,
                                        telefone text NOT NULL,
                                        FOREIGN KEY (destinador_id) REFERENCES destinador (destinador_id)
                                    ); """  

    sql_create_nota_fiscal_table = """ CREATE TABLE IF NOT EXISTS nota_fiscal (
                                        nota_fiscal_id text PRIMARY KEY,
                                        emitente_id text NOT NULL,
                                        destinador_id text NOT NULL,
                                        valor_total text NOT NULL,
                                        FOREIGN KEY (emitente_id) REFERENCES emitente (emitente_id),
                                        FOREIGN KEY (destinador_id) REFERENCES destinador (destinador_id)
                                    ); """  

    sql_create_duplicata_table = """ CREATE TABLE IF NOT EXISTS duplicata (
                                        duplicata_id text PRIMARY KEY,
                                        nota_fiscal_id text NOT NULL,
                                        data_vencimento text NOT NULL,
                                        valor_pago text NOT NULL,
                                        FOREIGN KEY (nota_fiscal_id) REFERENCES nota_fiscal (nota_fiscal_id)
                                    ); """           


    # create tables
    if db.conn is not None:
        db.create_table(sql_create_emitente_table)
        db.create_table(sql_create_destinador_table)
        db.create_table(sql_create_endereco_destinador_table)
        db.create_table(sql_create_nota_fiscal_table)
        db.create_table(sql_create_duplicata_table)

    else:
        print("Error! cannot create the Database connection.")  

    return db

def delete_db(db_name : str):
    os.remove(db_name)

def save_nota_fiscal_on_db(test_db : Database, nota_fiscal : NotaFiscal):
    
    # Emitente
    emitente = check_if_emitente_exists_in_bd(test_db, nota_fiscal)
    if emitente:
        test_db.create_emitente(emitente)
    
    # Destinador
    destinador = check_if_destinador_exists_in_bd(test_db, nota_fiscal)
    if destinador:
        test_db.create_destinador(destinador)

        # Endereço do destinador
        endereco_destinador = nota_fiscal.get_dest_enderDest()
        test_db.create_endereco_destinador(endereco_destinador)

    # Nota fiscal
    nota_fiscal_dict = check_if_nota_fiscal_exists_in_bd(test_db, nota_fiscal)
    if nota_fiscal_dict:
        test_db.create_nota_fiscal(nota_fiscal_dict)

        # Duplicata é parte da fatura pois a mesma pode ter mais de uma
        # parcela.
        for duplicata in nota_fiscal.get_faturas():
            test_db.create_duplicata(duplicata)

def check_if_emitente_exists_in_bd(test_db : Database, nota_fiscal : NotaFiscal) -> dict:
    emitente_dict = {'emitente_id' : nota_fiscal.get_emit_identifier(), 
                     'nome' : nota_fiscal.get_emit_name()}

    test_db.cursor.execute("SELECT nome FROM emitente WHERE emitente_id = ?", 
                            (emitente_dict['emitente_id'],))

    data=test_db.cursor.fetchone()
    if data is None:
        # print('There is no component named %s', emitente_dict['emitente_id'])
        return emitente_dict
    else:
        print('Emitente com identificador %s já existe no sistema'%(emitente_dict['emitente_id']))
        return None

def check_if_destinador_exists_in_bd(test_db : Database, nota_fiscal : NotaFiscal) -> dict:
    destinador_dict = {'destinador_id' : nota_fiscal.get_dest_identifier(), 
                       'nome' : nota_fiscal.get_dest_name()}

    test_db.cursor.execute("SELECT nome FROM destinador WHERE destinador_id = ?", 
                            (destinador_dict['destinador_id'],))
    data=test_db.cursor.fetchone()
    if data is None:
        # print('There is no component named %s', destinador_dict['emitente_id'])
        return destinador_dict
    else:
        print('Destinador com identificador %s já existe no sistema'%(destinador_dict['destinador_id']))
        return None

def check_if_nota_fiscal_exists_in_bd(test_db : Database, nota_fiscal : NotaFiscal) -> dict:
    nota_fiscal_dict = {'nota_fiscal_id' : nota_fiscal.get_nota_fiscal_id(), 
                        'emitente_id' : nota_fiscal.get_emit_identifier(), 
                        'destinador_id' : nota_fiscal.get_dest_identifier(),
                        'valor_total' : nota_fiscal.get_nota_fiscal_valor_total()}

    test_db.cursor.execute("SELECT nota_fiscal_id FROM nota_fiscal WHERE nota_fiscal_id = ?", 
                            (nota_fiscal_dict['nota_fiscal_id'],))

    data=test_db.cursor.fetchone()
    if data is None:
        return nota_fiscal_dict
    else:
        print('Nota fiscal com identificador %s já existe no sistema'%(nota_fiscal_dict['nota_fiscal_id']))
        return None

def consulta_boletos_de_um_emitente(test_db : Database, identificador_emitente : str):
    test_db.cursor.execute("SELECT nome FROM emitente WHERE emitente_id = ?", 
                            (identificador_emitente,))
    nome_emitente = test_db.cursor.fetchone()[0]
    print("---------------------------------------------------------")
    print("Consulta notas fiscais do emitente %s de identificador %s"%(nome_emitente, identificador_emitente))
    test_db.cursor.execute("SELECT * FROM nota_fiscal WHERE emitente_id = ?", 
                            (identificador_emitente,))
    notas_fiscais=test_db.cursor.fetchall()
    
    for nota_fiscal in notas_fiscais:
        print('\n--------- Nota fiscal ---------')
        print('Código: ', nota_fiscal[0], ' ')
        print('Valor total da nota: ', nota_fiscal[3])
        test_db.cursor.execute("SELECT * FROM duplicata WHERE nota_fiscal_id = ?", 
                            (nota_fiscal[0],))
        duplicatas=test_db.cursor.fetchall()
        if duplicatas != None:
            print('\n--------- Parcelas da fatura ---------')
        for dup in duplicatas:
            print('Boleto: ', dup[0].split('NFe')[0]) 
            print('Data de vencimento: ', dup[2])
            print('Valor a ser pago: ', dup[3])

        print('\n\n')

def consulta_clientes_de_um_emitente(test_db : Database, identificador_emitente : str):
    test_db.cursor.execute("SELECT nome FROM emitente WHERE emitente_id = ?", 
                            (identificador_emitente,))
    nome_emitente = notas_fiscais=test_db.cursor.fetchone()[0]
    print("---------------------------------------------------------")
    print("Consulta clientes do emitente %s de identificador %s"%(nome_emitente, identificador_emitente))
    test_db.cursor.execute("SELECT * FROM nota_fiscal WHERE emitente_id = ?", 
                            (identificador_emitente,))
    notas_fiscais=test_db.cursor.fetchall()

    for nota_fiscal in notas_fiscais:
        test_db.cursor.execute("SELECT * FROM destinador WHERE destinador_id = ?", 
                            (nota_fiscal[2],))
        destinadores=test_db.cursor.fetchall()
        if destinadores != None:
            print('\n--------- Clientes ---------')
        for dest in destinadores:
            print('Nome: ', dest[1], 'Identificador: ', dest[0]) 

