from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from flask_dropzone import Dropzone
import sqlite3
from werkzeug.exceptions import abort
import os
# Biblioteca para trabalhar com XML
import xml.etree.ElementTree as ET
from typing import List
from NotaFiscal import NotaFiscal
from Database import Database

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
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_CUSTOM = True,
    DROPZONE_ALLOWED_FILE_TYPE='.xml',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=30,
)
app.run(debug=True)
dropzone = Dropzone(app)

@app.route('/')
def index():
    # os.remove('database.db')
    test_db : Database = Database('database.db', 'schema.sql')

    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():

    idetifier =  request.args.get('identificador')
    if(idetifier == ''):
        return render_template('index.html')

    # os.remove('database.db')
    test_db : Database = Database('database.db', 'schema.sql')

    # vetor das notas fiscais lidas na entrada
    vet_nota_fiscal : List[NotaFiscal] = []

    
    # Lê arquivos xml e guarda eles em objetos 
    # do tipo NotaFiscal
    for file in os.listdir("uploads"):
        if file.endswith(".xml"):
            # print(file)
            nota_fiscal = NotaFiscal("uploads/" + file)
            vet_nota_fiscal.append(nota_fiscal)

    emitente_dict_list = []
    for nota_fiscal in vet_nota_fiscal:
        emitente_dict = {}
        emitente_dict['emitente_id'] = nota_fiscal.get_emit_identifier()
        emitente_dict['nome'] = nota_fiscal.get_emit_name()
        emitente_dict_list.append(emitente_dict)

    # Percorre as notas fiscais guardadas
    for nota_fiscal in vet_nota_fiscal:
        test_db.save_nota_fiscal_on_db(nota_fiscal)   

    # print("\n\nResultado")
    notas_fiscais_de_um_emitente = test_db.consulta_boletos_de_um_emitente(idetifier)
    if notas_fiscais_de_um_emitente == None:
        return render_template('index.html')

    clientes_de_um_emitente = test_db.consulta_clientes_de_um_emitente(idetifier) 
    if clientes_de_um_emitente == None:
        return render_template('index.html')

    return render_template('index.html', notas_fiscais_de_um_emitente=notas_fiscais_de_um_emitente, clientes_de_um_emitente = clientes_de_um_emitente)

@app.route('/', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        file_path = os.path.join(app.config['UPLOADED_PATH'], f.filename)
        f.save(file_path)
        
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)