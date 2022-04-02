# Venha para Recomb
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=00KL_venhapararecomb&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=00KL_venhapararecomb)

## Documentação da solução

### Solução

A solução implementada recebe um ou mais arquivos .xml de notas fiscais em um página web.

Através de um serviço Flask, esses arquivos são enviado da página web para ter suas informações extraidas e salvas em um banco de dados.

Por fim, é possível realizar consultas aos clientes e boletos de um dado fornecedor.
### Módulos

A implentação da solução foi dividida em módulos:
- [Database](./Database.py): Classe que realiza comunicação com o banco.
- [NotaFiscal](./NotaFiscal.py): Classe que extrai e armazena em memória as informações de um arquivo XML.
- [App](./app.py): Arquivo com funções que criam interfaces entre as classes chave do sistema e os componentes HTML que exibem os resultados.
- [Schema](./schema.sql): Arquivo com schema do banco de dados.

### Pastas
- [Static](./static): Pasta que contem os estilos CSS das páginas do sistema.
- [Templates](./templates/): Pasta que contem os arquivos HTML da página web.
- [Uploads](./uploads/): Pasta que armazena os quivos XML enviados pelo usuário do sistema.

### Execução
Para preparar o ambiente execute o comando:
```
make init_env
```

Para executar o código após a preparação do ambiente execute:
```
make all
```

Durante a execução do algorítimo os dados utilizados serão guardados assim, caso o usuário deseje apagar todos os dados salvos basta rodar o comando:
```
make clean_db_uploads
```

## Lista dos diferenciais implementados

|Item |	Pontos Ganhos|
|-----|--------------|
|Criar um serviço com o problema 	|30|
|Utilizar banco de dados 	|30|
|Qualidade de Código com SonarQube |15|
|Total |	75|

## Desafio

Descrito no [repositório original](https://github.com/recombX/venhapararecomb#readme) do desafio.
