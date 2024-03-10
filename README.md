## Documentação da Solução

### Tecnologias Utilizadas
- Django: Framework web em Python.
- Sqlite3: Serviço de banco de dados local do Django.
- HTML, CSS e Bootstrap: para a interface do usuário.

### Funcionalidades Implementadas
1. **Parse de XML**: A função parse_xml recebe um arquivo XML de uma nota fiscal e extrai as informações relevantes, como fornecedor, clientes, endereços e boletos.
2. **Página Inicial**: A view index renderiza a página inicial do sistema, permitindo aos usuários enviar arquivos XML para processamento.
3. **Cadastro de Notas Fiscais**: Ao submeter um arquivo XML válido, as informações da nota fiscal são salvas no banco de dados, incluindo fornecedor, clientes e boletos associados.
4. **Listagem de Notas Fiscais**: A view list_nfs apresenta uma lista de todas as notas fiscais cadastradas no sistema.
5. **Detalhes da Nota Fiscal**: A view detail_nf permite visualizar os detalhes de uma nota fiscal específica, incluindo clientes e boletos associados.
6. **Exclusão de Notas Fiscais**: A view delete_nf permite excluir uma nota fiscal do banco de dados, mas não exclui dados de fornecedor e clientes.
7. **Listagem de Fornecedores**: A view list_fornecedores lista todos os fornecedores cadastrados no sistema.
8. **Exclusão de Fornecedores**: A view delete_fornecedor permite excluir um fornecedor do banco de dados. Ao excluir um fornecedor do banco de dados as notas fiscais associadas também são apagadas.
9. **Listagem de Clientes**: A view list_clientes lista todos os clientes cadastrados no sistema.
10. **Exclusão de Clientes**: A view delete_cliente permite excluir um cliente do banco de dados. Ao apagar um cliente, as notas fiscais relacionadas não são apagadas.

### Como Executar a Aplicação
1. Clone o repositório do projeto:
   ```
   git clone https://github.com/jcquadros/venhapararecomb-backend.git
   ```
2. Instale o Django:
   ```
   pip install django
   ```
3. Navegue até o diretório do projeto que contenha o arquivo manage.py.

4. Inicie o servidor:
   ```
   python manage.py runserver
   ```

5. Acesse a aplicação em seu navegador, através do endereço 'http://127.0.0.1:8000/'.

## Diferenciais Implementados
- Interface de Usuário Responsiva: A interface do usuário foi desenvolvida de forma simples com Bootstrap, mas responsiva.
- Tratamento de Erros: O sistema trata erros comuns, como tentativa de envio de nota fiscal fornecedores e clientes duplicados.
- Padrão de programação Django MTV (Model, Template, View)
- Uso de banco de dados: A aplicação utiliza o Sqlite3 como serviço de banco de dados local.
- Implementação de Testes Unitários: Os testes cobrem as principais funções da aplicação, incluindo o parse de XML, as views e os modelos do Django.