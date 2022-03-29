from ast import Try
from warnings import catch_warnings
from NotaFiscal import NotaFiscal
from typing import List
from pprint import pprint
import os
  
print("Bem vindo!")
print("Este progarma irá ler diversas notas fiscais em formato xml guardadas em uma pasta.")
print("Por favor informe o nome da pasta:")

# Entrada da linha de comando
# Pasta que contem as notas fiscais
path = input()

try: 
    # Diretório para ser percorrido em busca
    # de novos arquivos
    os.chdir(path)
except:
    print("Pasta não encontrada.")
    exit(1)

# vetor das notas fiscais lidas na entrada
vet_nota_fiscal : List[NotaFiscal] = []

indetifier = input()

# Percorre os arquivos de uma dada pasta
# e cria um objeto NotaFiscal para armazenar
# e percorrer os dados do arquivo XML da entrada
for file in os.listdir():
    if file.endswith('xml'):
        print(file)
        nota_fiscal = NotaFiscal(file)
        vet_nota_fiscal.append(nota_fiscal)

# Percorre as notas fiscais guardadas
for nota_fiscal in vet_nota_fiscal:
    # Caso uma nota fiscal possua o identificador 
    # dado como entrada o mesmo deve ser printado
    if nota_fiscal.get_emit_identifier() == indetifier:
        pprint(nota_fiscal.get_faturas())
        pprint(nota_fiscal.get_dest_identifier())
        pprint(nota_fiscal.get_dest_enderDest())    