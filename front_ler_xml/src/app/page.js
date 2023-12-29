'use client';

import React, { useState, useEffect } from 'react';
import './styles.css';

const Componente = () => {
  const [userForm, setUserForm] = useState({
    CNPJ: '',
    xNome: '',
    vNF: '',
    dVenc: '',
    xLgr: '',
    nro: '',
    xBairro: '',
    xMun: '',
    UF: '',
    CEP: ''
  });


  // Função para ler o arquivo XML
  const readXMLFile = () => {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    //Verifica se o arquivo foi selecionado
    if (file) {
      const reader = new FileReader(); // Cria uma instância de FileReader para ler o conteúdo do arquivo

      // Define uma função de retorno de chamada para ser executada quando a leitura do arquivo estiver concluída
      reader.onload = function (e) {
        // Obtém a string XML do resultado da leitura do arquivo
        const xmlString = e.target.result;
        // Cria uma instância do DOMParser para análise XML
        const parser = new DOMParser();
        // Analisa a string XML e cria um documento XM
        const xmlDoc = parser.parseFromString(xmlString, 'text/xml');

        try {
          // Acessando os elementos XML
          const CNPJValue = xmlDoc.getElementsByTagName('CNPJ')[0].textContent;
          const xNomeValue = xmlDoc.getElementsByTagName('xNome')[0].textContent;
          const vNFValue = xmlDoc.getElementsByTagName('vNF')[0].textContent;
          const dVencValue = xmlDoc.getElementsByTagName('dVenc')[0].textContent;
          const xLgrValue = xmlDoc.getElementsByTagName('xLgr')[0].textContent;
          const nroValue = xmlDoc.getElementsByTagName('nro')[0].textContent;
          const xBairroValue = xmlDoc.getElementsByTagName('xBairro')[0].textContent;
          const xMunValue = xmlDoc.getElementsByTagName('xMun')[0].textContent;
          const UFValue = xmlDoc.getElementsByTagName('UF')[0].textContent;
          const CEPValue = xmlDoc.getElementsByTagName('CEP')[0].textContent;

          // Atualizar o estado com os valores obtidos
          setUserForm({
            CNPJ: CNPJValue,
            xNome: xNomeValue,
            vNF: vNFValue,
            dVenc: dVencValue,
            xLgr: xLgrValue,
            nro: nroValue,
            xBairro: xBairroValue,
            xMun: xMunValue,
            UF: UFValue,
            CEP: CEPValue
          });

          // Enviar dados para o servidor Node.js
          fetch('http://localhost:8080/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },

            body: JSON.stringify({
              CNPJ: CNPJValue,
              xNome: xNomeValue,
              vNF: vNFValue,
              dVenc: dVencValue,
              xLgr: xLgrValue,
              nro: nroValue,
              xBairro: xBairroValue,
              xMun: xMunValue,
              UF: UFValue,
              CEP: CEPValue
            }),
          })
            .then(response => response.json())
            .then(data => {
              console.log('Sucesso:', data);

              // Recarregar pagina após sucesso
              window.location.reload();
            })
            // Erro que possa ocorrer durante a requisição fetch
            .catch((error) => {
              console.log('Erro ao processar o arquivo XML:', error);
            });
        // Alerta de erro caso a NF não esteja no padrão pré etabelecido 
        } catch (error) {
          console.warn('Erro, arquivo não condiz com padrão estabelecido:', error);
        }
      };

      // Inicia a leitura do arquivo como texto
      reader.readAsText(file);
    } else {
      console.warn('Nenhum arquivo selecionado.');
    }
  };

  const [storedData, setStoredData] = useState([]);

  // Função para obter os dados armazenados no banco de dados
  const fetchStoredData = async () => {
    try {
      const response = await fetch('http://localhost:8080/databaseEmpresa');
      const data = await response.json();
      setStoredData(data);
    } catch (error) {
      console.warn('Erro ao obter dados armazenados:', error);
    }
  };

  // Executar a função ao carregar a página
  useEffect(() => {
    fetchStoredData();
  }, []);


  return (
    <div className="container">
      <div className="file-upload-container">

        <input type="file" id="fileInput" />
        <button onClick={readXMLFile}>Ler Arquivo XML</button>

      </div>

      <br></br>
      <br></br>
      <br></br>


      <h2>Dados do Cliente</h2>
      <br></br>
      <table border="1">
        <thead>
          <tr>
            <th>CNPJ</th>
            <th>Nome</th>
            <th>Valor</th>
            <th>Data vencimento</th>
            <th>Logradouro</th>
            <th>Numero</th>
            <th>Bairro</th>
            <th>Municipio</th>
            <th>UF</th>
            <th>CEP</th>

          </tr>
        </thead>
        <tbody>
          {storedData.map((item, index) => (
            <tr key={index}>
              <td>{item.CNPJ}</td>
              <td>{item.xNome}</td>
              <td>{item.vNF}</td>
              <th>{item.dVenc}</th>
              <th>{item.xLgr}</th>
              <th>{item.nro}</th>
              <th>{item.xBairro}</th>
              <th>{item.xMun}</th>
              <th>{item.UF}</th>
              <th>{item.CEP}</th>
            </tr>
          ))}
        </tbody>
      </table>
    </div>



  );
};

export default Componente;