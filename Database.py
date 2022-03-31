from multiprocessing.connection import Connection
import sqlite3
from sqlite3 import Error

'''
Utilização do banco de dados:
    Justificativa: Uma vez que um arquivo é lido ele é salvo no banco permitindo 
    acesso as informações relevante a aplicação em executações futuras do mesmo
    1. O programa deve listar valores e data de vencimento de boletos segundo um dado
    indentificador (CPF OU CNPJ) de um fornecedor (emitente).
    2. o program deve listar nome, identificador (CPF ou CNPJ) e endereço dos 
    clientes de um dado fornecedor(emitente)

'''

class Database():
    def __init__(self, input_path: str):
        self.db_path : str = input_path
        self.conn : Connection = self.create_connection()
        self.cursor = self.conn.cursor()

    def create_connection(self) -> Connection:
        """ create a Database connection to the SQLite Database
            specified by db_file
        :param db_file: Database file
        :return: Connection object or None
        """
        conn : Connection = None
        try:
            conn= sqlite3.connect(self.db_path)
            return conn
        except Error as e:
            print(e)

        return conn

    def create_table(self, create_table_sql) -> None:
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            self.cursor.execute(create_table_sql)
        except Error as e:
            print(e)

    def create_emitente(self, emitente) -> None:
        """
        Create a new project into the projects table
        :param conn:
        :param project:
        :return: project id
        """
        sql = ''' INSERT INTO emitente(emitente_id,
                                       nome) 
                                       VALUES(?,?) '''
        self.cursor.execute(sql, (emitente['emitente_id'],
                                  emitente['nome']))
        self.conn.commit()
        
    def create_destinador(self, destinador) -> None:
        sql = ''' INSERT INTO destinador(destinador_id,
                                           nome) 
                                           VALUES(?,?) '''
        self.cursor.execute(sql, (destinador['destinador_id'], 
                                  destinador['nome']))
        self.conn.commit()
        
    def create_endereco_destinador(self, endereco) -> None:
        sql = ''' INSERT INTO endereco_destinador(destinador_endereco_id,
                                            destinador_id,
                                            logradouro,
                                            numero,
                                            bairro,
                                            municipio,
                                            estado,
                                            cep,
                                            telefone) 
                                            VALUES(?,?,?,?,?,?,?,?,?) '''
        self.cursor.execute(sql, (endereco['destinador_endereco_id'],
                                  endereco['destinador_id'],
                                  endereco['xLgr'],
                                  endereco['nro'], 
                                  endereco['xBairro'], 
                                  endereco['xMun'],
                                  endereco['UF'],
                                  endereco['CEP'],
                                  endereco['fone']
                                  ))
        self.conn.commit()
        
    def create_nota_fiscal(self, nota_fiscal):
        # print(nota_fiscal)
        sql = ''' INSERT INTO nota_fiscal(nota_fiscal_id, 
                                           emitente_id, 
                                           destinador_id,
                                           valor_total) 
                                           VALUES(?,?,?,?) '''
        
        self.cursor.execute(sql, (nota_fiscal['nota_fiscal_id'], 
                                  nota_fiscal['emitente_id'], 
                                  nota_fiscal['destinador_id'],
                                  nota_fiscal['valor_total']))
        self.conn.commit()
    
    def create_duplicata(self, duplicata):
        sql = ''' INSERT INTO duplicata(duplicata_id, 
                                           nota_fiscal_id, 
                                           data_vencimento,
                                           valor_pago) 
                                           VALUES(?,?,?,?) '''
        self.cursor.execute(sql, (duplicata['duplicata_id'], 
                                  duplicata['nota_fiscal_id'], 
                                  duplicata['data_vencimento'],
                                  duplicata['valor_pago']))
        self.conn.commit()