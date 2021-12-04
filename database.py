import sqlite3 as sl
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sl.connect(db_file)
    except Error as e:
        print(e)

    return conn

def initiate_tables(con):
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS NOTAS_FISCAIS (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            cnpj_or_cpf_emit TEXT,
            cnpj_or_cpf_client TEXT,
            dvenc TEXT,
            valor FLOAT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS CLIENTES (
            cnpj_or_cpf_client TEXT,
            cnpj_or_cpf_emit TEXT,
            nome TEXT,
            endereco TEXT
        );
    """)

    con.commit()

def execute_query(request, data, con):
    cur = con.cursor()
    cur.execute(request, data)
    con.commit()

def execute_and_print(request, data, con):
    cur = con.cursor()
    cur.execute(request, data)
    rows = cur.fetchall()
    result = ""
    for row in rows:
        result += "; ".join(map(str, row))
        print(result)
    print(rows)
    return result

def drop_tables(con):
    with con:
        con.execute("DROP TABLE CLIENTES")
        con.execute("DROP TABLE NOTAS_FISCAIS")
    