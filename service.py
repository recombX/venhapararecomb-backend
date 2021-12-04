from flask import Flask
from flask_wtf.csrf import CSRFProtect
import parsing
import sys

app = Flask(__name__)
csrf = CSRFProtect(app)

file = str(sys.argv[1])
if file == None:
    print("Não foi passado o nome do arquivo XML")
    exit()
parsing.parsing_and_saving(file)

@app.route('/')
def a():
    f = open("home.html", "r")
    text = f.read()
    f.close()
    return text

@app.route('/<tipo>/<id>')
def busca(tipo, id):
    if tipo == '1':
        request = 'SELECT valor, dVenc FROM NOTAS_FISCAIS WHERE cnpj_or_cpf_emit = ?'
        result = parsing.busca_query(id, request)
        if result == None:
            return "Nenhum boleto encontrado!"
        return result
    else:
        request = 'SELECT nome, cnpj_or_cpf_client, endereco FROM CLIENTES WHERE cnpj_or_cpf_emit = ?'
        result = parsing.busca_query(id, request)
        if result == None:
            return "Nenhum cliente encontrado!"
        return result


app.run(host="0.0.0.0", port=5000)