
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Muriloide21_notas-fiscais-python&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Muriloide21_notas-fiscais-python)


## Como Executar

### Com Docker:

- Com o Docker rodando, execute: `docker build -t CONTAINER_NAME .`

- Em seguida: `docker run -d -p 5000:5000 CONTAINER_NAME`

- Acesse [localhost:5000](http://localhost:5000)

### Sem Docker:

#### Pré-requisitos:
Python >= 3.8;
Python Virtual Environment;
Python pip.

- Criando um *Virtual Environment*: `python3 -m venv env`

- Acessando o *venv*:
    - Windows: `.\env\Scripts\activate`
    - Linux/Mac: `./env/bin/activate`   

- Instalando os *requirements*: `pip install -r requirements.txt`

- Executando o serviço: `python service.py FILENAME`
- Acesse [localhost:5000](http://localhost:5000)

## Documentação da Solução

Escolhi utilizar a linguagem Python para realizar o desafio,
Para a parte de parsing do XML, escolhi o módulo xml.etree.ElementTree;
Aproveitando-me da linguagem, utilizei a biblioteca sqlite3 para fazer a integração com Banco de Dados.
Para abrir uma porta com o serviço escolheu-se utilizar Flask.

A ideia da solução é percorrer todas as notas fiscais contidas no XML passado como parâmetro e obter as seguintes informações de cada uma:

- CPF/CNPJ do Fornecedor;
- CPF/CNPJ do Cliente;
- Valor e Data de Vencimento dos boletos;
- Nome e Endereço dos Clientes.

Para isso, utiliza-se dos métodos *find()* e *findall()* do módulo de Element Tree e da função *match()* da biblioteca de Regular Expressions.

Uma vez obtidas as informações necessárias em cada nota fiscal, são feitas inserções nas tabelas NOTAS_FISCAIS e CLIENTES criadas no início da execução. O formato dessas tabelas pode ser visualizado na função *initiate_tables()* do módulo *database.py*.

Passada toda a fase de *parsing* solicita-se ao usuário o tipo de busca que ele deseja realizar e o CPF/CNPJ do fornecedor em questão (tudo isso na página disponibilizada com Flask). Em seguida, realiza-se uma *query* de busca (SELECT) no banco de dados para obter as informações solicitadas.

## Lista dos diferenciais implementados

- Criar um serviço com o problema: Flask;
- Utilizar banco de dados: sqlite3;
- Implementar Clean Code:
    - Função de parsing bem comentada ao longo das etapas para melhor entendimento do leitor;
    - Nomes das funções, variáveis, módulos e tabelas do banco inteligíveis;
    - Modularização das etapas de parsing e interação com banco de dados;
    - Generalização de funções para evitar repetições de código;
- Qualidade de Código com SonarQube;
- Implementar Utilizando Docker
