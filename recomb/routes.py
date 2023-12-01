'''Creates routes system'''
from flask import render_template
import xmltodict
from recomb import app, database
from recomb.forms import FormNFe
from recomb.models import Fornecedor, Cliente, Endereco, Nota

@app.route("/", methods=("GET", "POST"))
def homepage():
    '''
    Function that reads information from the

    .XML file read through the formNFE form


    Args: none

    Returns: Form validation for sending the XML file.
    And all Supplier, Customer, Address and Billing data

    '''
    form_nfe=FormNFe()
    if form_nfe.validate_on_submit():
        nota = form_nfe.botao_NFe.data

        #Converts file data into a python dictionary.
        dic_nota = xmltodict.parse(nota)
        #Get only the dictionaries after the infNFE subtree
        infos_nf = dic_nota["nfeProc"]["NFe"]["infNFe"]

        #Filter to check if the 'Fornecedor' already exists in the database, 
        # so as not to insert redundant information
        doc_fornecedor = Fornecedor.query.filter_by(documento=infos_nf['emit']['CNPJ']).first()
        if not doc_fornecedor:
            fornecedor = Fornecedor(nome = infos_nf['emit']['xNome'],
                                    documento = infos_nf['emit']['CNPJ'])
            database.session.add(fornecedor)
            database.session.commit()
            fornecedor_id = fornecedor.id
        else:
            #Gets customer data and their respective address directly from the database
            fornecedor = doc_fornecedor
        
        #Filter to check if the 'Cliente' already exists in the database,
        # so as not to insert redundant information
        doc_cliente = Cliente.query.filter_by(documento=infos_nf['dest']['CNPJ']).first()
        if not doc_cliente:
            cliente = Cliente(nome = infos_nf['dest']['xNome'],
                          documento = infos_nf['dest']['CNPJ'])
            database.session.add(cliente)
            database.session.commit()

            endereco = Endereco(rua = infos_nf['dest']['enderDest']['xLgr'],
                                num = infos_nf['dest']['enderDest']['nro'],
                                bairro = infos_nf['dest']['enderDest']['xBairro'],
                                municipio = infos_nf['dest']['enderDest']['xMun'],
                                uf = infos_nf['dest']['enderDest']['UF'],
                                cep = infos_nf['dest']['enderDest']['CEP'],
                                pais = infos_nf['dest']['enderDest']['xPais'],
                                telefone = infos_nf['dest']['enderDest']['fone'],
                                id_cliente = cliente.id)
            database.session.add(endereco)
            cliente_id = cliente.id
        else:
            #Gets 'cliente' data and their respective address directly from the database
            cliente = doc_cliente
            endereco = Endereco.query.filter_by(id_cliente=cliente.id).first()
        
        #Filter to check if the 'Nota' already exists in the database,
        # so as not to insert redundant information
        doc_nota = Nota.query.filter_by(num_nota=infos_nf['ide']['nNF']).first()
        if not doc_nota:
            notas = infos_nf['cobr']['dup']

            #Checks situations in which there is more than one installment
            # to be paid. In this case the notes variable will be a list of
            # dictionaries, otherwise it will just be a dictionary
            if isinstance(notas, list):
                for i in notas:
                    nota = Nota()
                    nota.valor = i['vDup']
                    nota.vencimento = i['dVenc']
                    nota.num_nota = infos_nf['ide']['nNF']
                    nota.id_cliente = cliente_id
                    nota.id_fornecedor = fornecedor_id
                    database.session.add(nota)
                    database.session.commit()
            else:
                nota = Nota(valor = notas['vDup'], vencimento = notas['dVenc'],
                                num_nota = infos_nf['ide']['nNF'], id_cliente = cliente_id,
                                id_fornecedor = fornecedor_id)
                database.session.add(nota)
        else:
            nota = doc_nota
        #Add everything to the database
        database.session.commit()
        return render_template("homepage.html", form=form_nfe, fornecedor=fornecedor, cliente=cliente, endereco=endereco, nota=nota)
    return render_template("homepage.html", form=form_nfe)