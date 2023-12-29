# Solução
#### A solução implementada recebe 1 arquivo .xml por vez, envia para o banco de dados e apresenta o resultado logo a baixo.
#### Na pagina web o usuário consegue visualizar o arquivo que acabou de enviar e no 'Dados do Ciente' pode ver o que já está armazenado

# Como rodar
#### Existem outros 2 README dentro da pasta [api](#api) e [front_ler_xml](#front_ler_xml)
#### É necessario executar um START dentro de cada pasta, dentro dos outros 2 README contém as informaçõs

# Modulos
#### A implentação da solução foi dividida em módulos:

   * [User:](#User) define um modelo de dados utilizando o Sequelize.
   * [db:](#db)configura uma instância do Sequelize para se conectar ao banco de dados.
   * [app:](#app) entrada principal para aplicação Node.js usando o framework Express.
   * [globals:](#globals) gerado automaticamente pelo next é um arquivo de estilo escrito em CSS, que define variáveis de cor, esquemas de cores, estilos e outras configurações globais para serem usadas em uma aplicação web.
   * [layout:](#layout) um componente React que define o layout padrão para a aplicação.
   * [page:](#page) componente React funcional que representa a página principal da aplicação.
   * [styles:](#styles) todo componente css dos dados dos clientes.
    
# Pastas

   * [api:](#api) pasta onde esta concentrado o backend que contém:
        * [modules:](#modules) contém os módulos relacionados a aplicação.
        * [routes:](#routes) nela contém as rotas da aplicação Express.js
   * [front_ler_xml:](#front_ler_xml) pasta onde esta concentrado o frontend que contém:
        * [public:](#public) gerado automaticamente pelo next.
        * [src/app:](#src/app) contém toda logica do lado do frontend.


# Execução
##### Para executar, por favor, olhe os dois README dentro da pasta /api e /front_ler_xml
###### Decidi divir essa parte para não gerar confusão


# Diferenciais implementados

|          Itens                 |  Pontos |
|--------------------------------|---------|
| Criar um serviço com o problema|   30    |
| Utilizar banco de dados        |   30    |