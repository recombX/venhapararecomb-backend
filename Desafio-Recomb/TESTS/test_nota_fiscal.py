from model.nota_fiscal import Nota_fiscal 
import os

def test_insert():
    nf = Nota_fiscal()

    nome_fonec = "COMERCIAL S.R.DE ALIMENTOS LTDA-ME"
    cnpj_fonec = "07872718000117"
    nome_cli = "JEFERSON SIMAO DE OLIVEIRA - ME"
    cnpj_cli = "17197072000173"
    endereco_cli = "municipio: CARIACICA, lagradouro: RUA SAO JOAO, bairro: ITACIBA, numero: 49"
    data_pg = "duplicata 1: 2022-12-15; duplicata 2: 2022-12-22; 1"
    valor = 1136.23

    try:
        nf.insert(nome_fonec, cnpj_fonec, nome_cli, cnpj_cli, endereco_cli, data_pg, valor)
        insercao_sucesso = True
    except Exception as e:
        print("Erro ao inserir", e)
        insercao_sucesso = False


    assert insercao_sucesso
    
def test_insert_csv():
    nf = Nota_fiscal()

    caminho_arquivo_csv = "data.csv"

    if os.path.exists(caminho_arquivo_csv):
        try:
            nf.insert_csv(caminho_arquivo_csv)
            insercao_sucesso = True
        except Exception as e:
            print("Erro ao inserir", e)
            insercao_sucesso = False
    else:
        print(f"Arquivo CSV {caminho_arquivo_csv} não encontrado.")
        insercao_sucesso = False

    assert insercao_sucesso