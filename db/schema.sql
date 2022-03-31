DROP TABLE IF EXISTS fornecedores;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS boletos;
DROP TABLE IF EXISTS notas_fiscais;

CREATE TABLE fornecedores (
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    identificador TEXT NOT NULL UNIQUE
);

CREATE TABLE clientes (
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    identificador TEXT NOT NULL UNIQUE,
    nome TEXT NOT NULL,
    endereco TEXT NOT NULL
);

CREATE TABLE notas_fiscais (
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    chave_acesso TEXT NOT NULL UNIQUE,
    fornecedor_id INTEGER,
    cliente_id INTEGER,
    FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(_id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(_id)
);

CREATE TABLE boletos (
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor REAL NOT NULL,
    vencimento TIMESTAMP NOT NULL,
    nota_fiscal_id INTEGER,
    FOREIGN KEY (nota_fiscal_id) REFERENCES notas_fiscais(_id)
);

