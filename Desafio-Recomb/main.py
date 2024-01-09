import streamlit as st
import os
import read_nf
import tempfile
import write_csv as wr
from model.nota_fiscal import Nota_fiscal



st.set_page_config(page_title="Nota fiscal")


def main():
    st.title("Insira a Nota Fiscal")
    arquivo_xml = st.file_uploader("Selecione um arquivo XML", type="xml")
    nf = Nota_fiscal()

    if arquivo_xml is not None:
        diretorio_temp = tempfile.mkdtemp()
        nome_arquivo = arquivo_xml.name 
        caminho_arquivo_temp = os.path.join(diretorio_temp, nome_arquivo)
        
        with open(caminho_arquivo_temp, 'wb') as arquivo_temp:
            arquivo_temp.write(arquivo_xml.read())
        
        caminho_arquivo_relativo = os.path.relpath(caminho_arquivo_temp, os.getcwd())
        
        
        with st.container():
            st.subheader("Fornecedor:")
            emits = read_nf.BuscarDadosEmissor(caminho_arquivo_relativo)
            for emit in emits:
                st.write(emit)
            st.write("---")
            
            
            st.subheader("Cliente:")
            dests = read_nf.BuscarDadosDestinatario(caminho_arquivo_relativo)
            for dest in dests:
                st.write(dest)
            st.write("---")
            
            
            st.subheader("Endereco do Cliente:")
            enderecoCli = read_nf.BuscarEnderecoDestinatario(caminho_arquivo_relativo) 
            for endereco in enderecoCli:
                st.write(endereco)
            st.write("---")
            
            st.subheader("Valores:")
            valorItems = read_nf.BuscarValorItens(caminho_arquivo_relativo)
            for valorItem in valorItems:
                st.write(valorItem)
            st.write("---")
            
            
            st.subheader("Data de vencimento: ")
            st.write("Duplicatas: ") 
            datas = read_nf.BuscarDataVencimento(caminho_arquivo_relativo)
            for data in datas:
                st.write(data) 
            st.write("---")
            
            
            st.subheader("Valor a pagar: ")
            valores = read_nf.BuscarvalorPagar(caminho_arquivo_relativo)
            for valor in valores:
                st.write(valor)
            st.write("---")
            
        
        #botão salvar
        if st.button("Salvar"):
            st.write("Arquivo salvo no banco de dados Postgres com sucesso!")
            st.subheader("Registros de seu banco de dados:")
            wr.writeCSV(caminho_arquivo_relativo)
           
            nf.insert_csv("data.csv")
            dbViews = nf.print_registros()
            for i in dbViews:
                st.write(i)
            
            

   

if __name__ == "__main__":
    main()
    