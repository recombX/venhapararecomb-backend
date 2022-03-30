import sqlite3
from contextlib import closing
from datetime import datetime
from models import Fornecedor, Cliente, NotaFiscal

def create_database(db_file_path, db_schema_path):
    """
    Creates a database file from a schema file.

    Args:
        db_file_path (str): The path to the database file.
        db_schema_path (str): The path to the schema file.
    
    Returns:
        None
    """
    with closing(sqlite3.connect(db_file_path)) as connection:
        with open(db_schema_path) as f:
            connection.executescript(f.read())
        connection.commit()

def create_if_not_exist(connection, cursor, should_commit, table_name, columns, primary_key, primary_attribute, item_tuple):
    """
    Creates a new item in the database if it doesn't exist.
    
    Args:
        connection (sqlite3.Connection): The connection to the database.
        cursor (sqlite3.Cursor): The cursor to the database.
        should_commit (bool): Whether or not to commit the changes to the database.
        table_name (str): The name of the table to insert the item into.
        columns (list): The list of columns to insert the item into.
        primary_key (str): The name of the primary key column.
        primary_attribute (str): The value of the primary key attribute.
        item_tuple (tuple): The tuple of values to insert into the table.
        
    Returns:
        int: The id of the item. 
    """
    result = cursor.execute(f"SELECT * FROM {table_name} WHERE {primary_key} = ?", (primary_attribute,)).fetchone()
    if result is None:
        cursor.execute(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?']*len(columns))})",
            item_tuple
        )
        _id = cursor.lastrowid
        if should_commit:
            connection.commit()
    else:
        _id = result[0]
    return _id

def create_many(connection, cursor, should_commit, table_name, columns, items_list):
    """
    Creates many items in the database.

    Args:
        connection (sqlite3.Connection): The connection to the database.
        cursor (sqlite3.Cursor): The cursor to the database.
        should_commit (bool): Whether or not to commit the changes to the database.
        table_name (str): The name of the table to insert the item into.
        columns (list): The list of columns to insert the item into.
        items_list (list): The list of items to insert into the table.

    Returns:
        None
    """
    cursor.executemany(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?']*len(columns))})",
        items_list
    )
    if should_commit:
        connection.commit()

def create_fornecedor(connection, cursor, should_commit, fornecedor):
    """
    Creates a new fornecedor in the database if it not exists.

    Args:
        connection (sqlite3.Connection): The connection to the database.
        cursor (sqlite3.Cursor): The cursor to the database.
        should_commit (bool): Whether or not to commit the changes to the database.
        fornecedor (Fornecedor): The fornecedor to insert into the database.

    Returns:
        int: The id of the fornecedor.
    """
    return create_if_not_exist(connection, cursor, should_commit, 
        'fornecedores', ['identificador'], 'identificador', 
        fornecedor.identificador, (fornecedor.identificador,))

def create_cliente(connection, cursor, should_commit, cliente):
    """
    Creates a new cliente in the database if it not exists.
    
    Args:
        connection (sqlite3.Connection): The connection to the database.
        cursor (sqlite3.Cursor): The cursor to the database.
        should_commit (bool): Whether or not to commit the changes to the database.
        cliente (Cliente): The cliente to insert into the database.

    Returns:
        int: The id of the cliente.
    """
    return create_if_not_exist(connection, cursor, should_commit, 
        'clientes', ['identificador', 'nome', 'endereco'], 'identificador', 
        cliente.identificador, (cliente.identificador, cliente.nome, cliente.endereco))

def create_boletos(connection, cursor, should_commit, boletos):
    """
    Creates many boletos in the database.

    Args:
        connection (sqlite3.Connection): The connection to the database.
        cursor (sqlite3.Cursor): The cursor to the database.
        should_commit (bool): Whether or not to commit the changes to the database.
        boletos (list): The list of boletos to insert into the database.
    
    Returns:
        None
    """
    return create_many(connection, cursor, should_commit, 
        'boletos', ['nota_fiscal_id', 'valor', 'vencimento'], 
        boletos)

def create_NF(db_file_path, nota_fiscal):
    """
    Creates a new nota fiscal in the database.

    Args:
        db_file_path (str): The path to the database file.
        nota_fiscal (NotaFiscal): The nota fiscal to insert into the database.

    Returns:
        int: The id of the nota fiscal.
    """
    with closing(sqlite3.connect(db_file_path)) as connection:
        with closing(connection.cursor()) as cursor:
            fornecedor_id = create_fornecedor(connection, cursor, False, nota_fiscal.fornecedor)
            cliente_id = create_cliente(connection, cursor, False, nota_fiscal.cliente)
            cursor.execute("INSERT INTO notas_fiscais (fornecedor_id, cliente_id) VALUES (?, ?)",
                (fornecedor_id, cliente_id)
            )
            nota_fiscal_id = cursor.lastrowid
            create_boletos(connection, cursor, False, [(nota_fiscal_id, boleto['valor'], boleto['vencimento']) for boleto in nota_fiscal.boletos])
            connection.commit()

def query1(db_file_path, fornecedor_identificador):
    """
    Queries the database for the list of all boletos issued to a fornecedor.

    Args:
        db_file_path (str): The path to the database file.
        fornecedor_identificador (str): The fornecedor's identificador.

    Returns:
        list: The list of boletos issued to the fornecedor.
    """
    with closing(sqlite3.connect(db_file_path)) as connection:
        with closing(connection.cursor()) as cursor:
            return [{'valor': float(val), 'vencimento': datetime.strptime(ven, '%Y-%m-%d %H:%M:%S')} for _, val, ven in
                    cursor.execute("""
                    SELECT boletos.nota_fiscal_id, boletos.valor, boletos.vencimento
                    FROM boletos
                    INNER JOIN notas_fiscais ON boletos.nota_fiscal_id = notas_fiscais._id
                    INNER JOIN fornecedores ON notas_fiscais.fornecedor_id = fornecedores._id
                    WHERE fornecedores.identificador = ?;
                """, (fornecedor_identificador, )).fetchall()
            ]

def query2(db_file_path, fornecedor_identificador):
    """
    Queries the database for the list of all clientes of a fornecedor.

    Args:
        db_file_path (str): The path to the database file.
        fornecedor_identificador (str): The fornecedor's identificador.

    Returns:
        list: The list of clientes of the fornecedor.
    """
    with closing(sqlite3.connect(db_file_path)) as connection:
        with closing(connection.cursor()) as cursor:
            return [Cliente(i, n, e) for i, n, e in 
                cursor.execute("""
                    SELECT clientes.identificador, clientes.nome, clientes.endereco
                    FROM clientes
                    INNER JOIN notas_fiscais ON clientes._id = notas_fiscais.cliente_id
                    INNER JOIN fornecedores ON notas_fiscais.fornecedor_id = fornecedores._id
                    WHERE fornecedores.identificador = ?;
                """, (fornecedor_identificador, )).fetchall()
            ]
