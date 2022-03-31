# Venha para Recomb

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=LKhoe_venhapararecomb&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=LKhoe_venhapararecomb)

## Documentação da solução

### Solução

O Código desenvolvido cria um serviço Flask que permite o upload de arquivos de NFe em formato `.xml` e realiza o parsing em cada um deles.

A partir do parsing as informações de Cliente, Fornecedor e Boletos de uma NFe são extraídos e armazenados em um banco de dados.

Também no serviço Flask é possível consultar informações de um Fornecedor a partir de seu identificador (CPF ou CNPJ).

As informações informadas são aquelas especificadas no desafio:
1. Nome, CPF ou CNPJ e Endereço dos Clientes que compram desse Fornecedor;
2. Boletos emitidos por esse Fornecedor;

### Código

O código foi desenvolvido em módulos, onde cada módulo realiza operações em uma área específica.
- [Database](./src/database.py): Responsável pela conexão de manipulação do banco de dados.
- [Parsing](./src/parsing.py): Responsável por reconhecer dos arquivos de entrada e extrair as informações dele.
- [Models](./src/models.py): Define as classes que representam os objetos que serão manipulados.

Além dos módulos foi desenvolvido um serviço em Flask para facilitar o uso.
- [Service](./src/service.py): Serviço em Flask responsável pela aplicação web.

A documentação de cada uma das funções dos módulos foi gerada pelo [pdoc3](https://pypi.org/project/pdoc3/), através dos comentários feitos no código.
Para consultar a documentação em um formato amigável:
- Clone o repositório ```git clone https://github.com/LKhoe/venhapararecomb.git```
- Na pasta `docs/` abra o arquivo `index.html` com algum navegador.

### Execução

```bash
docker build -t recomb .
docker run -it -p 5000:5000 recomb
```

## Lista dos diferenciais implementados

|Item |	Pontos Ganhos|
|-----|--------------|
|Criar um serviço com o problema 	|30|
|Utilizar banco de dados 	|30|
|Implementar Clean Code 	|20|
|Implementar o padrão de programação da tecnologia escolhida 	|20|
|Qualidade de Código com SonarQube| 	15|
|Implementar usando Docker 	|5|
|Total |	120|

## Desafio

Descrito no [repositório original](https://github.com/recombX/venhapararecomb#readme) do desafio.