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
    def __init__(self, input_path: str, schema_path: str):
        self.db_path : str = input_path
        self.schema_path : str = schema_path
        self.conn : Connection = self.create_connection()
        self.cursor = self.conn.cursor()

    # Cria conexão com um banco de dados já existente ou cria 
    # um novo banco de dados atraves do esquema passado
    def create_connection(self) -> Connection:
        conn : Connection = None
        try:
            conn = sqlite3.connect(self.db_path)
            with open(self.schema_path) as f:
                conn.executescript(f.read())
            return conn
        except Error as e:
            print(e)

        return conn

    # Cria tabela no banco de dados ou caso sejam passos argumentos
    # os mesmos são usados para prencher uma tabela existente.
    def create_table(self, create_table_sql : str, args : str = None) -> None:
        try:
            if args == None:
                self.cursor.execute(create_table_sql)
            else:
                self.cursor.execute(create_table_sql, args)
            self.conn.commit()
        except Error as e:
            print(e)

    def create_emitente(self, emitente) -> None:
        
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

    # Checa se um dado identificador existe em uma dada tabela
    def check_if_exists_in_bd(self, table : str, identifier : str) -> bool:
        sql = "SELECT * FROM "+ table + " WHERE "+ table +"_id = ?"
        self.cursor.execute(sql, (identifier,))

        data = self.cursor.fetchone()
        if data is None:
            return True
        else:
            print('Emitente com identificador %s já existe no sistema'%(identifier))
            return False

    # Consulta nota fiscal de duplicatas de um dado emitente. 
    def consulta_nota_fiscal_e_duplicatas_de_um_emitente(self, identificador_emitente : str) -> dict:
        
        self.cursor.execute("SELECT * FROM nota_fiscal WHERE emitente_id = ?", 
                                (identificador_emitente,))
        notas_fiscais=self.cursor.fetchall()
        if notas_fiscais == None:
            return None

        notas_fiscais_dict = []
        for nota_fiscal in notas_fiscais:
            nota_fiscal_dict = {}
            
            nota_fiscal_dict['nota_fical_id'] = nota_fiscal[0]
            nota_fiscal_dict['valor_total'] = nota_fiscal[3]

            self.cursor.execute("SELECT * FROM duplicata WHERE nota_fiscal_id = ?", 
                                (nota_fiscal[0],))
            duplicatas=self.cursor.fetchall()
            duplicatas_dict = []

            for dup in duplicatas:
                duplicata_dict = {}
                duplicata_dict['duplicata_id'] =  dup[0].split('NFe')[0]
                duplicata_dict['data_vencimento'] =  dup[2]
                duplicata_dict['valor_pago'] =  dup[3]
                duplicatas_dict.append(duplicata_dict)
            nota_fiscal_dict['duplicatas'] = duplicatas_dict
            notas_fiscais_dict.append(nota_fiscal_dict)

        return notas_fiscais_dict
        

    def consulta_clientes_de_um_emitente(self, identificador_emitente : str) -> dict:
        
        self.cursor.execute("SELECT * FROM nota_fiscal WHERE emitente_id = ?", 
                                (identificador_emitente,))
        notas_fiscais=self.cursor.fetchall()

        if notas_fiscais == None:
            return None

        destinadores_dict = []

        for nota_fiscal in notas_fiscais:
            self.cursor.execute("SELECT * FROM destinador WHERE destinador_id = ?", 
                                (nota_fiscal[2],))
            destinadores=self.cursor.fetchall()

            for dest in destinadores:

                destinador_dict = {'destinador_id' : dest[0], 'nome':dest[1]}
                destinadores_dict.append(destinador_dict)
        
        return destinadores_dict

    # Salva nota fiscal no banco de dados
    def save_nota_fiscal_on_db(self, nota_fiscal : NotaFiscal):
        
        # Emitente
        # Salva novo emitente (fornecedor) no banco de dados caso o mesmo 
        # não exista.
        emitente_dict = {'emitente_id' : nota_fiscal.get_emit_identifier(), 
                        'nome' : nota_fiscal.get_emit_name()}
        if self.check_if_exists_in_bd('emitente',emitente_dict['emitente_id']):
            self.create_emitente(emitente_dict)

        # Destinador
        # Salva novo destinador (cliente) no banco de dados caso o mesmo
        # não exista
        destinador_dict = {'destinador_id' : nota_fiscal.get_dest_identifier(), 
                        'nome' : nota_fiscal.get_dest_name()}

        if self.check_if_exists_in_bd("destinador",destinador_dict['destinador_id']):
            self.create_destinador(destinador_dict)

            # Endereço do destinador
            # Salva endereço relacionado a um novo destinador.
            endereco_destinador = nota_fiscal.get_dest_enderDest()
            self.create_endereco_destinador(endereco_destinador)

        # Nota fiscal
        # Salva uma nova nota fiscal no banco  caso a mesma não exista
        nota_fiscal_dict = {'nota_fiscal_id' : nota_fiscal.get_nota_fiscal_id(), 
                            'emitente_id' : nota_fiscal.get_emit_identifier(), 
                            'destinador_id' : nota_fiscal.get_dest_identifier(),
                            'valor_total' : nota_fiscal.get_nota_fiscal_valor_total()}

        if self.check_if_exists_in_bd("nota_fiscal",nota_fiscal_dict['nota_fiscal_id']):
            self.create_nota_fiscal(nota_fiscal_dict)

            # Salva as duplicatas relacionadas a uma nota fiscal.
            # Duplicata é parte da fatura pois a mesma pode ter mais de uma
            # parcela. Duplicata também é chamada de boleto no contexto em
            # que esse programa se aplica
            for duplicata in nota_fiscal.get_faturas():
                self.create_duplicata(duplicata)