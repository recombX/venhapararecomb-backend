import psycopg2 as db
import csv

class Config:
    def __init__(self):
        self.config = {
            "postgres": {
                "user": "postgres",
                "password": "lucas123",
                "host": "localhost",
                "port": "5432",
                "database": "nota-fiscal"
            }
        }
        
class Connection(Config):
    def __init__(self):
        Config.__init__(self)
        try:
            self.conn = db.connect(**self.config["postgres"])
            self.cur = self.conn.cursor()
        except Exception as e:
            print("Erro na conexão", e)
            exit(1)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()
      
            
    @property
    def connection(self):
        return self.conn

    @property
    def cursor(self):
        return self.cur

    def commit(self):
        self.connection.commit()
        
    
    def fetchall(self):
        return self.cursor.fetchall()
    
    def execute(self, sql, params=None):
        self.cursor.execute(sql ,params or ())
    
    def query(self, sql, params=None):
        self.cursor.execute(sql ,params or ())
        return self.fetchall()
    
    
class Nota_fiscal(Connection):
    def __init__(self):
        Connection.__init__(self)
        
        
    def insert(self, nome_fonec, cnpj_fonec, nome_cli, cnpj_cli, endereco_cli, data_pg, valor):
        try:
            sql = f"INSERT INTO nota_fiscal (nome_fonec, cnpj_fonec, nome_cli, cnpj_cli, endereco_cli, data_pg, valor) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            self.execute(sql, (nome_fonec, cnpj_fonec, nome_cli, cnpj_cli, endereco_cli, data_pg, valor))
            self.commit()
        except Exception as e:
            print("Erro ao inserir", e)
            
    
    def insert_csv(self, filename):
        try:
            data = csv.DictReader(open(filename, encoding="utf-8"))
            for row in data:
                self.insert(row["nome_fonec"], row["cnpj_fonec"], row["nome_cli"], row["cnpj_cli"], row["endereco"], row["data_venc"], row["valor"])
        except Exception as e:
            print("Erro ao inserir", e)
            
      
    def print_registros(self):
        try:
            registros = self.query("SELECT * FROM nota_fiscal")
            return registros 
        except Exception as e:
            print("Erro ao buscar registros", e)
            return [] 
                       