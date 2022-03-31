from flask import Flask, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename
import re
from parsing import parse_nota_fiscal
from database import create_database as create_database_original, \
    create_nota_fiscal as create_nota_fiscal_original, \
    query1 as query1_original, \
    query2 as query2_original

# Setup functions for local database
DB_FILE_PATH = 'db/database.db'
DB_SCHEMA_PATH = 'db/schema.sql'
create_database = lambda: create_database_original(DB_FILE_PATH, DB_SCHEMA_PATH)
create_nota_fiscal = lambda x: create_nota_fiscal_original(DB_FILE_PATH, x)
query1 = lambda x: query1_original(DB_FILE_PATH, x)
query2 = lambda x: query2_original(DB_FILE_PATH, x)

# Setup Flask app
app = Flask(__name__)

@app.route('/')
def page_1():
   return render_template('1.html')

@app.route('/2', methods = ['GET', 'POST'])
def page_2():
    if request.method != 'POST':
        # To avoid breaking the flow of application, we will redirect to the first page
        return redirect(url_for('page_1'))

    # Get the list of files from the request
    files = request.files.getlist("file")
    for file in files:
        if file.filename == '':
            continue
        nf = parse_nota_fiscal(file.read()) # Parse the file
        if nf is not None:
            create_nota_fiscal(nf) # Create the nota fiscal in database

    return render_template('2.html')

@app.route('/3', methods = ['GET', 'POST'])
def page_3():
    if request.method != 'POST':
        # To avoid breaking the flow of application, we will redirect to the first page
        return redirect(url_for('page_1'))
    # Get the identificador from the request without the following characters . - /
    identificador = re.sub(r'[\.\-\/]', '', request.form.get('identificador', '')) 
    boletos = query1(identificador) # Get all boletos from a fornecedor
    clientes = query2(identificador) # Get all clientes related to a fornecedor

    return render_template('3.html', clientes=clientes, boletos=boletos)

@app.template_filter()
def format_datetime(value):
    return value.strftime('%d/%m/%Y')

if __name__ == '__main__':
    try:
        create_database() # Create the database
    except Exception:
        print("Não foi possível criar o banco de dados")
    app.run("0.0.0.0", port=5000, debug = True) # Run the app
