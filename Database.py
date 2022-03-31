from multiprocessing.connection import Connection
import sqlite3
from sqlite3 import Error
from NotaFiscal import NotaFiscal

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

    def create_table(self, create_table_sql : str, args : str = None) -> None:
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        # print(args)
        try:
            if args == None:
                self.cursor.execute(create_table_sql)
            else:
                self.cursor.execute(create_table_sql, args)
            self.conn.commit()
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
        self.create_table(sql, (emitente['emitente_id'],
                                  emitente['nome']))
        
    def create_destinador(self, destinador) -> None:
        sql = ''' INSERT INTO destinador(destinador_id,
                                           nome) 
                                           VALUES(?,?) '''
        self.create_table(sql, (destinador['destinador_id'], 
                                  destinador['nome']))
        
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
        self.create_table(sql, (endereco['destinador_endereco_id'],
                                  endereco['destinador_id'],
                                  endereco['xLgr'],
                                  endereco['nro'], 
                                  endereco['xBairro'], 
                                  endereco['xMun'],
                                  endereco['UF'],
                                  endereco['CEP'],
                                  endereco['fone']
                                  ))
        
    def create_nota_fiscal(self, nota_fiscal):
        # print(nota_fiscal)
        sql = ''' INSERT INTO nota_fiscal(nota_fiscal_id, 
                                           emitente_id, 
                                           destinador_id,
                                           valor_total) 
                                           VALUES(?,?,?,?) '''
        
        self.create_table(sql, (nota_fiscal['nota_fiscal_id'], 
                                  nota_fiscal['emitente_id'], 
                                  nota_fiscal['destinador_id'],
                                  nota_fiscal['valor_total']))
    
    def create_duplicata(self, duplicata):
        sql = ''' INSERT INTO duplicata(duplicata_id, 
                                           nota_fiscal_id, 
                                           data_vencimento,
                                           valor_pago) 
                                           VALUES(?,?,?,?) '''
        self.create_table(sql, (duplicata['duplicata_id'], 
                                  duplicata['nota_fiscal_id'], 
                                  duplicata['data_vencimento'],
                                  duplicata['valor_pago']))

    def check_if_exists_in_bd(self, table : str, identifier : str) -> bool:
        sql = "SELECT * FROM "+ table + " WHERE "+ table +"_id = ?"
        self.cursor.execute(sql, (identifier,))

        data = self.cursor.fetchone()
        if data is None:
            # print('There is no component named %s', emitente_dict['emitente_id'])
            return True
        else:
            print('Emitente com identificador %s já existe no sistema'%(identifier))
            return False

    def consulta_boletos_de_um_emitente(self, identificador_emitente : str):
        self.cursor.execute("SELECT nome FROM emitente WHERE emitente_id = ?", 
                                (identificador_emitente,))
        nome_emitente = self.cursor.fetchone()[0]
        print("---------------------------------------------------------")
        print("Consulta notas fiscais do emitente %s de identificador %s"%(nome_emitente, identificador_emitente))
        self.cursor.execute("SELECT * FROM nota_fiscal WHERE emitente_id = ?", 
                                (identificador_emitente,))
        notas_fiscais=self.cursor.fetchall()
        
        for nota_fiscal in notas_fiscais:
            print('\n--------- Nota fiscal ---------')
            print('Código: ', nota_fiscal[0], ' ')
            print('Valor total da nota: ', nota_fiscal[3])
            self.cursor.execute("SELECT * FROM duplicata WHERE nota_fiscal_id = ?", 
                                (nota_fiscal[0],))
            duplicatas=self.cursor.fetchall()
            if duplicatas != None:
                print('\n--------- Parcelas da fatura ---------')
            for dup in duplicatas:
                print('Boleto: ', dup[0].split('NFe')[0]) 
                print('Data de vencimento: ', dup[2])
                print('Valor a ser pago: ', dup[3])

            print('\n\n')

    def consulta_clientes_de_um_emitente(self, identificador_emitente : str):
        self.cursor.execute("SELECT nome FROM emitente WHERE emitente_id = ?", 
                                (identificador_emitente,))
        nome_emitente = notas_fiscais=self.cursor.fetchone()[0]
        print("---------------------------------------------------------")
        print("Consulta clientes do emitente %s de identificador %s"%(nome_emitente, identificador_emitente))
        self.cursor.execute("SELECT * FROM nota_fiscal WHERE emitente_id = ?", 
                                (identificador_emitente,))
        notas_fiscais=self.cursor.fetchall()

        for nota_fiscal in notas_fiscais:
            self.cursor.execute("SELECT * FROM destinador WHERE destinador_id = ?", 
                                (nota_fiscal[2],))
            destinadores=self.cursor.fetchall()
            if destinadores != None:
                print('\n--------- Clientes ---------')
            for dest in destinadores:
                print('Nome: ', dest[1], 'Identificador: ', dest[0]) 

    def save_nota_fiscal_on_db(self, nota_fiscal : NotaFiscal):
        
        # Emitente
        emitente_dict = {'emitente_id' : nota_fiscal.get_emit_identifier(), 
                        'nome' : nota_fiscal.get_emit_name()}
        if self.check_if_exists_in_bd('emitente',emitente_dict['emitente_id']):
            self.create_emitente(emitente_dict)

        # Destinador
        destinador_dict = {'destinador_id' : nota_fiscal.get_dest_identifier(), 
                        'nome' : nota_fiscal.get_dest_name()}

        if self.check_if_exists_in_bd("destinador",destinador_dict['destinador_id']):
            self.create_destinador(destinador_dict)

            # Endereço do destinador
            endereco_destinador = nota_fiscal.get_dest_enderDest()
            self.create_endereco_destinador(endereco_destinador)

        # Nota fiscal
        nota_fiscal_dict = {'nota_fiscal_id' : nota_fiscal.get_nota_fiscal_id(), 
                            'emitente_id' : nota_fiscal.get_emit_identifier(), 
                            'destinador_id' : nota_fiscal.get_dest_identifier(),
                            'valor_total' : nota_fiscal.get_nota_fiscal_valor_total()}

        if self.check_if_exists_in_bd("nota_fiscal",nota_fiscal_dict['nota_fiscal_id']):
            self.create_nota_fiscal(nota_fiscal_dict)

            # Duplicata é parte da fatura pois a mesma pode ter mais de uma
            # parcela.
            for duplicata in nota_fiscal.get_faturas():
                self.create_duplicata(duplicata)