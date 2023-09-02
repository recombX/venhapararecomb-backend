import xmltodict
import psycopg2

def abrir_conexão_bd():
  connection="ERRO"
  dbname = "eggvfinq"
  user = "eggvfinq"
  password = "9iD3LdnjQpf4zd-OBSJvo2FM55tDppev"
  host = "silly.db.elephantsql.com"
  port = "5432"  # Porta padrão do PostgreSQL

  try:
      connection = psycopg2.connect(
          dbname=dbname,
          user=user,
          password=password,
          host=host,
          port=port
      )
      print("Conexão estabelecida com sucesso!")

    # Aqui você pode realizar operações no banco de dados usando a conexão

  except psycopg2.Error as e:
      print("Erro ao conectar ao banco de dados:", e)
  return connection

def inserir_registro_tabela_valores_e_vencimentos_boletos(valor,vencimento,connection):
    cursor = connection.cursor()
    query = "INSERT INTO VALORES_E_VENCIMENTOS_BOLETOS (data_validade, valor_boleto) VALUES (%s,%s);"
    data_to_insert = (vencimento,valor)
    cursor.execute(query, data_to_insert)
    connection.commit()
    print("Inserção realizada com sucesso!")

def inserir_registro_tabela_clientes(nome, cpf, cnpj, endereco,connection):
    cursor = connection.cursor()
    query = "INSERT INTO CLIENTES (nome, cpf, cnpj, endereco) VALUES (%s, %s, %s, %s);"
    data_to_insert = (nome, cpf, cnpj, endereco)
    cursor.execute(query, data_to_insert)
    connection.commit()
    print("Inserção realizada com sucesso!")

def ler_arquivo(patharquivo):
  with open(patharquivo, 'r', encoding='utf-8') as xml_file:
    xml_string = xml_file.read()
    dicionario = xmltodict.parse(xml_string)
    return dicionario

def buscar_arquivo_de_nota_fiscal(cpf_cnpj_fornecedor):
  dic_arquivo1 = ler_arquivo(
      "32211207872718000117550010000217781877120005-nfe.xml")
  dic_arquivo2 = ler_arquivo("NFe-002-3103.xml")

  emitente1 = dic_arquivo1['nfeProc']['NFe']['infNFe']['emit']
  emitente2 = dic_arquivo2['nfeProc']['NFe']['infNFe']['emit']

  if 'CNPJ' in emitente1:
    if emitente1['CNPJ'] == cpf_cnpj_fornecedor:
      print("Emitente 1/CNPJ: " + emitente1['CNPJ'])
      return dic_arquivo1
  if 'CPF' in emitente1:
    if emitente1['CPF'] == cpf_cnpj_fornecedor:
      print("Emitente 1/CPF: " + emitente1['CPF'])
      return dic_arquivo1
  if 'CNPJ' in emitente2:
    if emitente2['CNPJ'] == cpf_cnpj_fornecedor:
      print("Emitente 2/CNPJ: " + emitente2['CNPJ'])
      return dic_arquivo2
  if 'CPF' in emitente2:
    if emitente2['CPF'] == cpf_cnpj_fornecedor:
      print("Emitente 2/CPF: " + emitente2['CPF'])
      return dic_arquivo2

def printar_valores_e_vencimento_dos_boletos(dic_arquivo,connection):
  d_vencimento=dic_arquivo['nfeProc']['NFe']['infNFe']["cobr"]["dup"]["dVenc"]
  v_dup=dic_arquivo['nfeProc']['NFe']['infNFe']["cobr"]["dup"]["vDup"]
  print("Vencimento: "+d_vencimento)
  print("Valor do Boleto: R$"+v_dup)
  inserir_registro_tabela_valores_e_vencimentos_boletos(v_dup,d_vencimento,connection)

def printar_nome_cpf_ou_cnpj_endereco_dos_clientes(dic_arquivo,connection):
  cpf=""
  cnpj=""
  
  dest=dic_arquivo['nfeProc']['NFe']['infNFe']['dest']['xNome']
  print("Destinatário: "+dest)
  if 'CNPJ' in dic_arquivo['nfeProc']['NFe']['infNFe']['dest']:
    cnpj=dic_arquivo['nfeProc']['NFe']['infNFe']['dest']['CNPJ']
    print("CNPJ:"+cnpj)
  if 'CPF' in dic_arquivo['nfeProc']['NFe']['infNFe']['dest']:
    cpf=dic_arquivo['nfeProc']['NFe']['infNFe']['dest']['CPF']
    print("CPF:"+cpf)
  print("ENDEREÇO:")
  
  logr=dic_arquivo['nfeProc']['NFe']['infNFe']['dest']['enderDest']['xLgr']
  numero=dic_arquivo['nfeProc']['NFe']['infNFe']['dest']['enderDest']['nro']
  bairro=dic_arquivo['nfeProc']['NFe']['infNFe']['dest']['enderDest']['xBairro']
  num_municipio=dic_arquivo['nfeProc']['NFe']['infNFe']['dest']['enderDest']['cMun']
  municipio=dic_arquivo['nfeProc']['NFe']['infNFe']['dest']['enderDest']['xMun']
  uf=dic_arquivo['nfeProc']['NFe']['infNFe']['dest']['enderDest']['UF']
  cep=dic_arquivo['nfeProc']['NFe']['infNFe']['dest']['enderDest']['CEP']
  num_pais=dic_arquivo['nfeProc']['NFe']['infNFe']['dest']['enderDest']['cPais']
  pais=dic_arquivo['nfeProc']['NFe']['infNFe']['dest']['enderDest']['xPais']
  telefone=dic_arquivo['nfeProc']['NFe']['infNFe']['dest']['enderDest']['fone']
  
  print("Logradouro:"+logr)
  print("Número:"+numero)
  print("Bairro:"+bairro)
  print("NumMunicípio:"+num_municipio)
  print("Município:"+municipio)
  print("UF:"+uf)
  print("CEP:"+cep)
  print("numPaís:"+num_pais)
  print("País:"+pais)
  print("Telefone:"+telefone)
  inserir_registro_tabela_clientes(dest, cpf, cnpj,(municipio+"-"+logr+"-"+numero),connection)

def main():
  '''faça um programa que informado o CPF leia todos os arquivos buscando um fornecedor com esse CPF, selecionado o arquivo mostre as seguintes opções: 1) Listar os valores e data de Vencimento dos boletos presentes em um nota fiscal conforme o CPF ou CNPJ de um fornecedor.2) Apresentar o nome, identificador (CPF ou CNPJ), endereço dos clientes de um fornecedor.
  
  0-conectar ao banco de dados
  1-informar_cpf
  2-buscar_arquivo_de_nota_fiscal(cpf_cnpj_fornecedor)
  3-pedir input de 1 ou 2.
    3.1- caso 1: printar_valores_e_vencimento_dos_boletos(dic_arquivo)
    3.2- caso 2: printar_nome_cpf_ou_cnpj_endereco_dos_clientes(dic_arquivo)'''

  #0
  conn=abrir_conexão_bd()
  #1
  cpf_cnpj = input("Insira o CPF/CNPJ do fornecedor: ")
  #2
  dic_arquivo_alvo = buscar_arquivo_de_nota_fiscal(cpf_cnpj)
  #print(dic_arquivo_alvo) descomente para validar a variavel dic_arquivo_alvo.
  
  #3
  teclado = ""
  while teclado != "1" and teclado != "2":
    teclado = input(
        "1-Mostrar Valores e Vencimentos dos boletos \n2-Mostrar Nome,CPF/CNPJ e endereço dos clientes"
    )
  if teclado == "1":  #3.1
    printar_valores_e_vencimento_dos_boletos(dic_arquivo_alvo,conn)
    #inserir dados lidos no banco de dados
  if teclado == "2":  #3.2
    printar_nome_cpf_ou_cnpj_endereco_dos_clientes(dic_arquivo_alvo,conn)
    #inserir dados lidos no banco de dados


main()



