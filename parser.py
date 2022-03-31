from database_utils import create_db, delete_db
from NotaFiscal import NotaFiscal
from Database import Database
from typing import List
import os

def main():
    print("Bem vindo!")
    print("Este progarma irá ler diversas notas fiscais em formato xml guardadas em uma pasta.")
    print("Por favor informe o nome da pasta:")

    # Entrada da linha de comando
    # Pasta que contem as notas fiscais
    path = 'notasFiscais'

    try: 
        # Diretório para ser percorrido em busca
        # de novos arquivos
        os.chdir(path)
    except:
        print("Pasta não encontrada.")
        exit(1)

    db_path = '../test.db'
    delete_db(db_path)
    test_db : Database = create_db('../test.db')
    
    # vetor das notas fiscais lidas na entrada
    vet_nota_fiscal : List[NotaFiscal] = []

    idetifier = '07872718000117'

    # Percorre os arquivos de uma dada pasta
    # e cria um objeto NotaFiscal para armazenar
    # e percorrer os dados do arquivo XML da entrada
    for file in os.listdir():
        if file.endswith('.xml'):
            # print(file)
            nota_fiscal = NotaFiscal(file)
            vet_nota_fiscal.append(nota_fiscal)

    # Percorre as notas fiscais guardadas
    for nota_fiscal in vet_nota_fiscal:
        test_db.save_nota_fiscal_on_db(nota_fiscal)

    # print("\n\nResultado")
    # test_db.consulta_boletos_de_um_emitente(idetifier)
    # test_db.consulta_clientes_de_um_emitente(idetifier)


if __name__ == '__main__':
    main()