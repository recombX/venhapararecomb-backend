from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from flask_dropzone import Dropzone
from werkzeug.exceptions import abort
from typing import List
from NotaFiscal import NotaFiscal
from Database import Database
import os
import sqlite3

test_db : Database = None

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'uploads'),
    DROPZONE_ALLOWED_FILE_CUSTOM = True,
    DROPZONE_ALLOWED_FILE_TYPE='.xml',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=30,
)

app.run(debug=True)
dropzone = Dropzone(app)

@app.route('/')
def index():

    return render_template('index.html')

# Busca no banco de d
@app.route('/search', methods=['GET', 'POST'])
def search():

    # Recebe da página web o valor de um indentificador (CPF/CNPJ)
    idetifier =  request.args.get('identificador')
    # Caso não receba nada não haverá busca alguma
    if(idetifier == ''):
        return render_template('index.html')

    # os.remove('database.db')
    # Cria conexão com banco existente ou cria um novo banco
    # Baseado no schema contido no aquivo schema.sql
    test_db : Database = Database('database.db', 'schema.sql')

    # Consulta as notas fiscais e boletos de um dado emitente (fornecedor)
    notas_fiscais_de_um_emitente = test_db.consulta_nota_fiscal_e_duplicatas_de_um_emitente(idetifier)
    # Caso não encontre nenhuma nota fiscal não há o que procurar
    if notas_fiscais_de_um_emitente == None:
        return render_template('index.html')

    # Consulta todos os destinadores (clientes) de um fornecedor
    clientes_de_um_emitente = test_db.consulta_clientes_de_um_emitente(idetifier) 

    return render_template('index.html', notas_fiscais_de_um_emitente=notas_fiscais_de_um_emitente, clientes_de_um_emitente = clientes_de_um_emitente)

# Permite que os arquivos colocados na área de upload sejam salvos na pasta uploads
@app.route('/', methods=['POST', 'GET'])
def upload_xml_files():
    if request.method == 'POST':
        f = request.files.get('file')
        file_path = os.path.join(app.config['UPLOADED_PATH'], f.filename)
        f.save(file_path)

    # os.remove('database.db')
    test_db : Database = Database('database.db', 'schema.sql')

    # vetor das notas fiscais lidas na entrada
    vet_nota_fiscal : List[NotaFiscal] = [] 

    # Lê arquivos xml e guarda eles em objetos 
    # do tipo NotaFiscal
    for file in os.listdir("uploads"):
        if file.endswith(".xml"):
            nota_fiscal = NotaFiscal("uploads/" + file)
            vet_nota_fiscal.append(nota_fiscal)

    # Percorre as notas fiscais guardadas
    for nota_fiscal in vet_nota_fiscal:
        # Salva uma nota fiscal no banco de dados
        test_db.save_nota_fiscal_on_db(nota_fiscal)  
        
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)