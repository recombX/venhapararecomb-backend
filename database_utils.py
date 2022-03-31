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



