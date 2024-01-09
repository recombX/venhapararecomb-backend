# Desafio Recomb
## Leitor de Nota Fiscal XML

## Sumário

1. Como executar a aplicação?
2. Esplicando o programa
3. Configurando o Banco de dados
4. Explicando o funcionamento dos arquivos da aplicação
5. Padrões de progrmação do Framework streamlit
6. Testes unitários
7. Sonarqube
8. Aplicação do Clean Code

### Lista dos diferenciais aplicados.
- Serviço web - Streamlit
- Banco de dados - Postgres
- Clean Code - Explicação encontrada na parte 8
- Padrão de programação da tecnologia - pode ser encontrado na parte 5. Padrões de programação do Framework streamlit
- Qualidade do código sonarqube - Exemplo encontrado na parte 7. Sonnarqube
- Testes unitários - explicação encontrada na parte 6. Testes unitários

##  1. Como executar a aplicação?
Tenha o [python](https://www.python.org/) instalado em sua máquina.

Em seguida, você vai abrir o terminal,seja pelo editor de código de sua preferência, ou pelo próprio terminal acessando o diretório da pasta do programa, em seguida siga os seguintes passos:

- Inicialize o ambiente virtual:

```sh
.\.venv\Scripts\Activate.ps1
```

- Inicialize a aplicação pelo streamlit:

```sh
streamlit run main.py
```

## 2. Explicando o programa

- Fluxo do programa:
Quando executado, você será direcionado poara uma página web, que terá um botão para inserir um arquivo de nota fiscal no formato xml de seu computador, em seguida ele irá exibir na tela todas as informações do nota fiscal, e abaixa dessas informações terá um botão de salvar, quando o usuário clicar neste botão, as informações serão salvas em um banco de dados e em seguida o site vai exibir as informações das tabelas desse banco.

- Como funciona:
O 'main' é o arquivo a que deve ser executado, pois ele é o responsável por reunir os métodos e classes dos outros arquivos, além de possuir o visual da página.
Depois de aberto ele vai guardar o caminho relativo da nota fiscal e chamar os métodos do arquivo 'read_nf.py' que responsável pela leitura da nota fiscal,após isso o main vai receber os dados da nota fiscal pelas as funções do 'read_nf' e vai imprimir as informações para o usuário.
Para salvar as informações no banco de dados, os dados serão escritas em um arquivo CSV, por meu do arquivo 'write_csv', em seguida serão processadas pelo arquivo chamado 'nota_fiscal' que possui a classes métodos que permitem a manipulação do banco de dados.



## 3. Configurando o Banco de dados
O banco de dados utilizado é o [PostgreSQL](https://www.postgresql.org/). Instale e configure esse banco de dados.
Para que a conexão do progrma funcione com o banco de dados, você deverá acessar o arquivo 'nota_fiscal.py' que se encontra dentro da pasta 'model' do projeto. Nele vocé irá mudar as configurações de conexão, basta alterar na classe config os campos que estão "***" para as informações do seu banco de dados.
```sh
"postgres": {
                "user": "***",
                "password": "***",
                "host": "***",
                "port": "***",
                "database": "***"
            }
```

Abra seu postgres e execute o seguinte e crie uma sequência:
```sh
CREATE SEQUENCE nota_fiscal_id_seq INCREMENT 1;
```
Depois Crie uma tabela com os seguintes comandos:
```sh
CREATE TABLE nota_fiscal(
	id INTEGER PRIMARY KEY NOT NULL DEFAULT nextval('nota_fiscal_id_seq'::regclass),
	nome_fonec CHARACTER VARYING(80),
	cnpj_fonec CHARACTER VARYING(80),
	nome_cli CHARACTER VARYING(80),
	cnpj_cli CHARACTER VARYING(80),
	endereco_cli CHARACTER VARYING(200),
	data_pg CHARACTER VARYING(50),
	valor float
)
```

## 4. Explicando o funcionamento dos arquivos da aplicação

### main
O main é responsável por exibir todas as informações do código em minha página web, ele Importa as bibliotecas necessárias: streamlit, os, tempfile, e os módulos personalizados como read_nf e write_csv.
- importando bibliotecas
```sh
import streamlit as st
import os
import read_nf
import tempfile
import write_csv as wr
from model.nota_fiscal import Nota_fiscal
```
- função main()
Define as configurações iniciais do Streamlit com e já define um título para a página st.set_page_config```st.set_page_config(page_title="Nota fiscal")```. Ele é iniciado pela função main(),criando um título na interface web usando st.title, e usa st.file_uploader para permitir que o usuário faça upload de um arquivo XML da NFe.
Ele faz o processamento de arquivo xml, cria um diretório temporário (tempfile.mkdtemp()) e salva o arquivo XML temporariamente nesse diretório. em seguida ele pega o camiho relativo desse arquivo e armazena em uma variável caminho_arquivo_relativo por meio do seguinte comando: ``` caminho_arquivo_relativo = os.path.relpath(caminho_arquivo_temp, os.getcwd())```
Depois é criado um container com os métodos com os métodos importados do meu arquivo de leitura da nota fiscal (read_nf), em seguida ele imprime os retornos desses com o a função ```st.write()```. Após a execução dos comandos dentro desse container, ele verifica se o botão salvar foi acionado serção dos dados em um banco de dados Postgres através do método writeCSV e insert_csv respectivamente do módulo write_csv e printa as tabelas do meu banco de dados por meio do ```nf.print_registros().```



### read_nf
Esse é o arquivo responsável por fazer a leitura dos dados da nota fiscal, onde cada método é responsável por retornar um tipo dados específicos da nota.
- Impotando bibliotecas
Primeiro é importado a bibliotecas xml.etree.ElementTree e depois o minidom do xml.dom que são bibliotecas usadas para trabalhar com arquivos xml.

```sh
import xml.etree.ElementTree as ET
from xml.dom import minidom
```
- Métodos:
BuscarDadosEmissor -Recebe como instância o caminho do arquivo pelo main e o método parse abre o arquivo XML e getroot() obtém o elemento raiz```sh root = ET.parse(caminho_arquivo).getroot() ``` , depois é definido um namespace para usar na busca do elemento xml ```nsNFE = {'ns' : "http://www.portalfiscal.inf.br/nfe"}```, logo em seguida ele armazena os dados em variáveis atravez de um método 'find()' para localizar as informações presentes no xml pelas tags passadas como no exemplo: ```cnpj_emit =root.find('ns:NFe/ns:infNFe/ns:emit/ns:CNPJ', nsNFE) ``` , aqui ele está pegando o CNPJ do emissor da nota. Depois de extrair todas as informações necessárias, o método retorna um vetor com assas informações.
Os métodos BuscarEnderecoEmissor,BuscarDadosDestinatario,BuscarEnderecoDestinatario, seguem a mesma lógica para fazer a busa dos itens, só será mudado as tags de procura e as informações em que eles vão retornar. (Esses métodos vão usar a biblioteca xml.etree.ElementTree)
BuscarValorItens - Nesse método, será retornado os itens e seus respectivos valores, ele abre o  arquivo XML  ```xml = open(caminho_arquivo)```, Parseia o arquivo XML utilizando a biblioteca minidom```nfe = minidom.parse(xml)```,recebe todos os elementos XML com a tag 'det' (itens)```itens = nfe.getElementsByTagName('det')```, percorre por um vetor de todos os itens encontrados e armazena em variáveis o valor encotrado para cada item. Depois de pegar todos os valores do primeiro item ele irá armazenar em um vetor, depois o método vai retornar um vetor de vetores,cujo um é o de itens e o outro é possui todos os itens.
Os métodos BuscarDataVencimento,BuscarvalorPagar seguem a mesma lpogica BuscarValorItens, porem serão mudadas as tags buscadas.

- OBS: 
Foram usadas duas formas diferentes de buscar os dados do meu xml, pois acredito que para os métodos: BuscarDadosEmissor, BuscarEnderecoEmissor, BuscarDadosDestinatario, BuscarEnderecoDestinatario, a forma de busca que foi implementada era a mais apropirada, pois faz a busca por um dado específico pelo caminho da tag. já nos outros métodos a busca foi feito pecorrendo a árvore do meu xml para achar a tag passada na funlçao``` nfe.getElementsByTagName()```, dessa forma, se torna mais fácil obter os valores datags em que se repetem, como no caso de itens, que possui mais de um, como no caso do xml usado de exemplo.

### nota_fical
Esse arquivo é responsável pela conexão com meu banco de dados e das função que permitem a manipulação do meu banco de dados, além de ter o meu objeto Nota_Fiscal.
- Será necessário importar a biblioteca psycopg2, que permite a interação do meu código python com meu banco de dados PostgreSQL, e importar csv para a leitura de meu arquivo CSV.
```sh
import psycopg2 as db
import csv
```
- Classe Config
Armazena as informações de configuração do banco de dados em um dicionário.

- Classe Connection
Estabelece a conexão com o banco de dados usando as informações de configuração.
Sobrescreve os métodos __enter__ e __exit__ para permitir que a classe seja usada com a declaração with e garantir que a conexão seja fechada corretamente.Fornece métodos para executar consultas SQL (execute, query) e realizar operações de busca (fetchall) e inserção (commit, insert).
```sh
 def __enter__(self):
        return self
```
```sh
def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()
```

- Classe Nota_Fiscal
Herda de Connection para aproveitar os métodos de conexão.
Implementa métodos para manipular dados na tabela nota_fiscal.
insert: Insere dados na tabela nota_fiscal.
insert_csv: Lê um arquivo CSV e insere seus dados na tabela nota_fiscal, por meio do comando ```self.insert(row["nome_fonec"], row["cnpj_fonec"], row["nome_cli"], row["cnpj_cli"], row["endereco"], row["data_venc"], row["valor"])```, que me permite a leitura dos dados do arquivo CSV chamando muinha função insert para armazenar os dados no banco de dados
delete: Remove um registro da tabela nota_fiscal com base no ID fornecido.
update: Atualiza um registro da tabela nota_fiscal com base no ID e nos novos valores fornecidos.
print_registros: Retorna todos os registros da tabela nota_fiscal.

### writeCSV
Esse é o arquivo responsável por escrever dados da nota fiscal em meu arquivo CSV. Para isso será primordial a importação a biblioteca CSV
```sh
 import csv
```
- Método writeCSV
Nele será implementado o mesmo modelo de busca do arquivo read_nf, infelismente não será aproveitado os mesmos métodos do read_nf, não serão usadas, todas as informações presentes nos retornos das funções de arquivo.
Primeiramente   as informações buscadas na nota fiscal serão armazenadas em um arquivo chamado 'dados' que recebes essas informações e cria uma lista contendo um dicionário
```sh
dados = [
        {"nome_fonec": nome_fonec,"cnpj_fonec": cnpj_fonec,"nome_cli": nome_cli,"cnpj_cli": cnpj_cli,"endereco": endereco,"data_venc": data_venc,"valor": valor},
    ]
```  
- Escrita no arquivo CSV
Primeiro é necessário criar uma chave ```chaves = dados[0].keys()```, onde dados[0] acessa o primeiro dicionário da lista, keys() é um método de dicionário que retorna um objeto que contém as chaves (nomes dos campos) desse dicionário, chaves armazena esses nomes de campos para serem usados como cabeçalho do arquivo CSV.
Logo em seguida o arquivo CSV vai ser aberto em modo de escrita (node='w') ```with open("data.csv", mode='w', newline='') as arquivo_csv:```, após isso, escreve a linha de cabeçalho no arquivo CSV.
```sh
for linha in dados:
    escritor_csv.writerow(linha)
```

## 5. Padrões de programação do Framework streamlit
- O programa usa um framework chamado [streamlit](https://streamlit.io/), que resumidamente, com o streamlit, é possível criar o uma aplicação web, cujo é possível editar o visual de minha página web, sem ter que tenha a necessidade de criar arquivos html, csss ou javaScript, basta chamar as funções do streamlit que que é possível criar textos, formulários , bottões etc.

- Padrão de programação do framework
O Streamlit é construído em torno de um conceito de programação declarativa e reativa,o mesmo utiliza um estilo de programação baseado em scripts. Você escreve o código sequencialmente, como faria em um script Python tradicional, e o Streamlit cuida da atualização automática da interface do usuário conforme os dados ou parâmetros mudam. Em resumo, o Streamlit oferece uma abordagem de programação simples e reativa para criar aplicativos web com Python. Seu modelo de programação permite que os desenvolvedores se concentrem na lógica do aplicativo, enquanto a biblioteca cuida da atualização dinâmica da interface do usuário com base nas mudanças nos dados e nos parâmetros.

## 6. Testes unitários
- Para os testes unitários, foi usado a biblioteca  [pytest](https://docs.pytest.org/en/7.4.x/).
- Para executar nossos testes basta digitar o comando pytest no terminal da aplicação:
```sh
pytest
```
- Se quisermos executar uma função específica basta usar o pytest -k e colocar o nome da função como no exemplpo abaixo:
```sh
pytest -k NOME_DA_FUNCAO
```

### test_read_fiscal.py
Neste arquivo de test, foram criados, métodos parecidos com os dos arquivos normais, porém estas não recebem um caminho como parâmetro, mas sim já é definida nala mesma o caminho em que o xml usado para os testes se encontra. Nisso foi criado um variável com o nome de 'result', que é um vetor que vai receber os resultados da busca feita dentro da função, e depois é criado uma variável 'expected', que é um vetor que vai conter os resultados esperados, no caso o 'expected' é preenchido com valores que se oncontram no xml da pasta de testes. Por fim, as funções irão fazer um 'assert' para asegurar que o resultados obtidos são compatíveis com os esperados ```assert result == expected```. 
Após rodar o meu pytest, ele irá retornar os resultados do teste.

### test_write_csv.py 
Neste arquivo há uma função 'write_csv()' que é responsável pela a escrita no arquivo csv da mesma formaem que foi visto antes, porém essa função retorna os dados que foram passados paraa a escrita.
Exite outra função, que é a 'read_csv()', essa função faz a leitura do meu csv e retorna as informações obtidas.
Logo depois é criada a minha função de teste, que é a 'test_write_csv()'. nela vou ter um 'result' que vai ter os dados passados pela 'write_csv()' e um 'expeted' que vai possuir as informações no meu 'read_csv()'', se de fato o arquivo csv foi iscrito, as informação de ambos vão bater, então é feito um ```assert result == expeted```.

### test_nota_fiscal.py
Neste arquivo é importado a minha classe nota fisca, para que se possa trabalhar com os métodos dessa classe.
Método test_insert(): nesse métoda a minha classe Nota_Fiscal é instanciada, depois é criado vaiáveis para conter daods que serão inseridos na nota, em seguida é feito um try que vai chamar meu método insert passando os dados das variáveis acima, em seguida e uma variável chamada 'insercao_sucesso' será armazenado TRUE, caso não dê certo a inserção, passará pelo except, onde a variável 'insercao_sucesso' vai receber FALSE, por fim, será feito um assert de 'insercao_sucesso' ```assert insercao_sucesso```, caso a inserção seja feita com sucesso (TRUE), ele passará no teste.
Método test_insert_csv(): nesse método a classe Npta_Fiscal é instanciado e definimos o caminho do arquivo csv, depois é feita a verifiação se o caminho existe```if os.path.exists(caminho_arquivo_csv):```, para isso será necessário a biblioteca 'os', dentro desse 'if' é feito um try que que vai chamar o método 'insert_csv' passando o caminho do arquivo, e caso a inserção seja feita com sucesso, uma variável 'insercao_sucesso' vai receber TRUE, caso não, será feito um except cujo insercao_sucesso' vai receber FALSE, depois o 'if' é fechado, e caso o e inicia um else, para caso o caminho do arquivo não seja encontrado, dentro do else a variável 'insercao_sucesso' vai receber false. Por fim, será feito um assert para verificar se inserção_sucesso é TRUE  ```assert insercao_sucesso```, caso sim, ele passa no test.

## 7. Sonnarqube

Deixei disponível os resultados do sonarqube em uma pasta, também é possível visualizar na imagem abaixo.
A ferramanta se mostrou muito efetiva apontando os pontos de melhoria e sujerindo o que fazer, consegui corrigir alguns bugs com o auxílio dela.
<img src="img\sonarqube\Captura de tela 2024-01-09 162605.png">

## 8. Aplicação do Clean Code
O clean code estabelece regras e características em que o código deve seguir para que faça sentido, assim ajudando na em suas futuras correções ou quando outra pessoa começar a desnevolver nele.
Tendo isso en vista neste código foi usados conceitos como funções com nomes bem definidos fazendo o que é sugerido no nome, como por exemplo a função "BuscarDadosEmissor()" função responsável no arquivo "read_nf", o nome do arquivo já sugere que será feito uma leitura na nota fiscal, e a função vai retornar os dados coletados do Emissor.
Foram usados outros conceitos, como colocar objetos do banco de dados em uma pasta "model", devidir arquivos de testes em uma pasta "TESTS", e imagens em pastas separadas
