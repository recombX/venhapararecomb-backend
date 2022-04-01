DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);  


CREATE TABLE IF NOT EXISTS emitente (
    emitente_id text PRIMARY KEY,
    nome text NOT NULL
);

CREATE TABLE IF NOT EXISTS destinador (
    destinador_id text PRIMARY KEY,
    nome text NOT NULL
);

CREATE TABLE IF NOT EXISTS endereco_destinador (
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
);

CREATE TABLE IF NOT EXISTS nota_fiscal (
    nota_fiscal_id text PRIMARY KEY,
    emitente_id text NOT NULL,
    destinador_id text NOT NULL,
    valor_total text NOT NULL,
    FOREIGN KEY (emitente_id) REFERENCES emitente (emitente_id),
    FOREIGN KEY (destinador_id) REFERENCES destinador (destinador_id)
);

CREATE TABLE IF NOT EXISTS duplicata (
    duplicata_id text PRIMARY KEY,
    nota_fiscal_id text NOT NULL,
    data_vencimento text NOT NULL,
    valor_pago text NOT NULL,
    FOREIGN KEY (nota_fiscal_id) REFERENCES nota_fiscal (nota_fiscal_id)
);