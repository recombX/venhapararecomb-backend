import xml.etree.ElementTree as ET

#xml = ET.parse('32211207872718000117550010000217781877120005-nfe.xml')
xml = ET.parse('NFe-002-3103.xml')
root = xml.getroot()
nsNFe = {'ns': 'http://www.portalfiscal.inf.br/nfe'}
# recuperando o valor do campo NFe infNFe dest xNome e cnpj
#1) Listar os valores e data de Vencimento dos boletos presentes em um nota fiscal conforme o CPF ou CNPJ de um fornecedor. Verificar qual deles está presente
#2) Apresentar o nome, identificador (CPF ou CNPJ), endereço dos clientes de um fornecedor.
# fornecedor
xNome = root.find('ns:NFe/ns:infNFe/ns:emit/ns:xNome', nsNFe).text
cnpj = root.find('ns:NFe/ns:infNFe/ns:emit/ns:CNPJ', nsNFe).text
print(f'Fornecedor: {xNome} - CNPJ: {cnpj}')
# clientes
for dest in root.findall('ns:NFe/ns:infNFe/ns:dest', nsNFe):
    xNome = dest.find('ns:xNome', nsNFe).text
    cpf = dest.find('ns:CPF', nsNFe)
    cnpj = dest.find('ns:CNPJ', nsNFe)
    if cpf is not None:
        ident = cpf.text
    else:
        ident = cnpj.text
    print(f'Cliente: {xNome} - Identificador: {ident}')
