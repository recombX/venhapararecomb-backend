## Solução
 A solução escolhida foi uma REST Api desenvolvida com Flask. Abaixo temos a descrição e instruções dos endpoints.

Para a solução do desafio, é necessário o cadastro das NFe's a partir do endpoint: `POST /nfe/xml`. Nele é enviado um arquivo XML no corpo da requisição e cadastradas as informações necessárias para o problema.

Para responder as questões utilizamos os endpoints:
- `GET /duplicata/<fornecedor_id>` 
- `GET /cliente/<fornecedor_id>` 
  
Que retornam as informações baseadas no identificador do fornecedor (CPF ou CNPJ)

Para inicializar o servidor, basta rodar o script "create-container.sh" como super usuário. Ou utilizar os seguintes comandos direto no seu terminal unix ou powershell:
```shell
docker build -t flask-api .
docker run -p 5000:5000 flask-api
```
O servidor Flask ficará disponivel em `localhost:5000`

        

## Diferenciais
|Item |	Pontos Ganhos|
|-----|--------------|
|Utilizar banco de dados 	|30|
|Implementar Clean Code 	|20|
|Implementar o padrão de programação da tecnologia escolhida 	|20
|Implementar usando Docker 	|5|
|Total |	75|



## Nota Fiscal
<details>

### Requisição

- `POST /nfe/xml`
- `POST /nfe`
- `GET /nfe`
- `PUT /nfe`
- `DELETE /nfe`
  
Endpoints para controlar as Notas Fiscais
#### Corpo da Requisição

`GET /nfe` 
- Retorna JSON com todos os nfees cadastrados


`POST /nfe/xml`
- Cadastra uma nota fiscal a partir do arquivo XML e suas duplicatas. Cadastra o cliente e fornecedor, caso não estejam cadastrados no banco de dados
```json
{
	"xml_file": Arquivo XML
}
````

`POST /nfe`
- Cadastra uma nota fiscal. Fornecedor e Cliente devem estar cadastrados.
```json
{   
    "id": Identificador unico da NFe,
	"id_cliente": "CPF ou CNPJ",
	"id_fornecedor": "CPF ou CNPJ"
}
````

`PUT /nfe`
- Atualiza uma nota fiscal,
```json
{
	"id": Identificador unico da NFe,
	"id_cliente": "CPF ou CNPJ",
	"id_fornecedor": "CPF ou CNPJ"
}
````

`DELETE /nfe`
- Deleta uma nota fiscal
```json
{
	"id": "CPF ou CNPJ",
}
````
</details>

__________________________________________
## Cliente
<details>

### Requisição
- `POST /cliente`
- `GET /cliente/<fornecedor_id>` 
- `GET /cliente`
- `PUT /cliente`
- `DELETE /cliente`
  
Endpoints para controlar o cliente
#### Corpo da Requisição

`GET /cliente` 
- Retorna JSON com todos os clientes cadastrados

`GET /cliente/<fornecedor_id>` 
- Retorna JSON com todos os clientes cadastrados, filtrados pelo fornecedor


`POST /cliente`
- Cadastra um novo cliente
```json
{
	"id": "CPF ou CNPJ",
	"nome": "Eduarsdoo",
	"endereco": "Rua São João, 101, Serra, ES, Brasil",
    "cep": CEP
}
````

`PUT /cliente`
- Atualiza um cliente
```json
{
	"id": "CPF ou CNPJ",
	"nome": "Eduardo",
	"endereco": "Rua São João, 101, Serra, ES, Brasil",
    "cep": CEP
}
````

`DELETE /cliente`
- Deleta um cliente

```json
{
	"id": "CPF ou CNPJ",
}
````
</details>

__________________________________________
## Duplicata/Boleto
<details>

### Requisição
- `POST /duplicata`
- `GET /duplicata/<fornecedor_id>` 
- `GET /duplicata`
- `PUT /duplicata`
- `DELETE /duplicata`
  
Endpoints para controlar o duplicata
#### Corpo da Requisição

`GET /duplicata` 
- Retorna JSON com todos as duplicatas cadastrados

`GET /duplicata/<fornecedor_id>` 
- Retorna JSON com todos as duplicatas cadastrados, filtradas pelo fornecedor


`POST /duplicata`
- Cadastra um novo duplicata
```json
{
	"nfeId": Identificador unico da NFe,
	"valor": 117.2,
    "vencimento": 24-05-2023
}
````

`PUT /duplicata`
- Atualiza um duplicata
```json
{
	"nfeId": Identificador unico da NFe,
	"valor": 117.2,
    "vencimento": 27-05-2023
}
````

`DELETE /duplicata`
- Deleta um duplicata

```json
{
	"id": "CPF ou CNPJ",
}
````
</details>

__________________________________________
## Fornecedor
<details>

### Requisição
- `POST /fornecedor`
- `GET /fornecedor`
- `PUT /fornecedor`
- `DELETE /fornecedor`
  
Endpoints para controlar o fornecedor
#### Corpo da Requisição

`GET /fornecedor` 
- Retorna JSON com todos os fornecedores cadastrados


`POST /fornecedor`
- Cadastra um novo fornecedor
```json
{
	"id": "CPF ou CNPJ",
	"nome": "Eduarsdoo"
}
````

`PUT /fornecedor`
- Atualiza um fornecedor
```json
{
	"id": "CPF ou CNPJ",
	"nome": "Eduardo"
}
````

`DELETE /fornecedor`
- Deleta um fornecedor

```json
{
	"id": "CPF ou CNPJ",
}
````
</details>



