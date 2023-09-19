# Documentação do Funcionamento da Implementação do Sistema

## O FRONTEND
### VUE
- O VUE, framework de JavaScript, com possibilidade de implementação utilizando o TypeScript também,
foi escolhido por conta da versatilidade, usabilidade e facilidade na comuniação de seus componentes com
o consumo da API desenvolvida. Além disso, pode-se destacar a organização de sua estrutura, que, por ser simples, torna
viável o uso de bibliotecas necessárias, através do node, para desenvolvimento do sistema

#### VIEWS
- <b>Home View</b> <br>
A Home View, localizado em _views_, possui a renderização do componente desenvolvido para esse sistema.
Como o _App.vue_ está com o RouterView para renderização, ao inserirmos o path: "_/_", ou seja, o path root, a renderização a ser
realizada é da própria home. Dessa forma, o componente _TheWelcome_ está sendo "consumido" para a criação 
do modelo da página e sua posterior renderização.

```
<script setup>
import TheWelcome from '../components/TheWelcome.vue'
</script>

<template>
  <main>
    <TheWelcome />
  </main>
</template>

```

#### ROTAS
- <b>index.js</b> <br>
As rotas, como abordado de forma rápida no tópico acima, define qual URL está sendo renderizada no momento, ou seja,
qual View deve ser renderizada conforme o path informado. Na rota implementada não houve necessidade de implementação
de outras possibilidades, visto que, uma única rota possui a formatação necessária para o envio do arquivo e visualização da consulta quando filtrado.<br>
```
  const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
      routes: [
      {
          path: '/',
          name: 'home',
          component: HomeView
      },
      ]
  })
```

#### COMPONENTES
- <b>components/TheWelcome</b> <br>
O único componente desenvolvido foi o _TheWelcome_, o mesmo que é inicializado quando é criado um projeto
em VUE. Para definir melhor cada parte, separemos em partes:
---
##### Nome e Dados
```
export default {
  name: "TheWelcome",
  data() {
    return {
      xml_file: null,
      resp: null,
      showMessage: false,
      search: "",
      clientes_fornecedor: []
    }
  },
```
O trecho de código acima possui a criação do nome do componente, ou seja, outro componente, view, serviço, etc, que queiram
importar esse componente, fazem através do nome informado no campo _name_. <br>

**DATA**<br>
Data retorna a criação de objetos no DOM do componente. Dessa forma, a parte lógica e o desenvolvimento de métodos
que precisam de consumir determinados dados, atualizar informações, fazem assim através da chamada _this.nomedodado_.
Dessa forma, no sistema desenvolvido existem alguns campos diferentes:
- xml_file: Responsavel por armazenar o arquivo xml
- resp: Responsável por armazenar o response em Json
- showMessage: Determina se houveram inicidências de Clientes ou Fornecedores a partir do filtro informado
- search: Armazena o campo de Pesquisa atual, ou seja, o que o usuário está digitando no campo de filtro
- clientes_fornecedor: Armazena todos os clientes e fornecedores que possuem CPF ou CNPJ com a os numeros informados

---
**Metodos**
```
methods: {
    sendFile() {
      let FileForm = new FormData();
      FileForm.append("fileNf", this.xml_file);
      if (this.xml_file['type'] !== 'text/xml') {
        alert("Por favor, envie um arquivo XML válido!")
      } else {

        sendFileXML(FileForm).then((response) => (this.resp = response.data))
            .then((response) =>
                this.resp = this.resp.map((d) => {
                  return {
                    boleto: d.boleto,
                    cliente: d.cliente,
                    fornecedor: d.fornecedor,
                  };
                }));
      }
    },
    doSearch(value) {
      searchClient(value).then((response) => {
        this.clientes_fornecedor = response.data;
        if(response.data.fornecedores.length > 0 || response.data.clientes.length > 0){
          this.showMessage = false
        }
      })

    },
    onImageUpload() {
      this.xml_file = this.$refs.uploadImage.files[0];
    }
  },
```
**sendFile**<br>
O Método cria um FormData em sua inicialização. Isso ocorre, pois, como estamos fazendo o envio de um arquivo,
para que a API possa entender o que está sendo passado e para que a requisição possa enviar o XML, o formData oferece
a possibilidade de fazer esse envio. Observa-se, no entanto, que, o FileForm possui um nome e um valor, e nesse caso
o nome informado no FileForm é o mesmo em que a API está esperando o arquivo, dessa forma facilita o consumo e a chegada do arquivo na Controller
para ser processado no serviço.<br>
Na continuação da chamada desse serviço, o Método então se comunica com sendFileXml, uma função inclusa no _axiosService_ e nesse momento,
após criar o FormFile, passa ele como parâmetro.<br>
O mapeamento que ocorre em seguida recebe as informações da NotaFiscal que a Controller retorna como um ResponseEntity no padrão informado.
No decorrer do processamento dessa página, ao enviar um arquivo XML válido, é criada uma seção abaixo da ‘interface’ principal que retorna com as informações da NFE referente
ao arquivo enviado.<br>

**doSearch()**<br>
O método faz a busca, com a chamada do axios em _axiosService_ informando o valor que está presente no campo de filtro.
```
<div class="mt-10 text-center">
    <input v-model="search" class="rounded-2xl text-center z-10 p-3" placeholder="Filtrar" type="text"/>
</div>
```
O retorno da chamada do axios, o response, é passado para a variável criada _clientes_fornecedor_, e na continuidade,
é feita uma verificação para saber se houve algum retorno de objetos esperados. Caso haja retorno, a variável _showMessage_ recebe o valor de false,
indicando que não é necessário informar que não houve retornos, e por fim, a _div_ que possui essa condição não será renderizada.

**onFileUpload**<br>
A função _onImageUpload_ é apenas chamada em condição de alteração de campo.
```
 <input
    ref="uploadFile"
    accept=".xml"
    class="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"
    type="file" @change="onFileUpload()">
```
A notação _@change_ verifica se houve alguma mudança no input. Se houver qualquer alteração, a função é chamada. Sua funcionalidade é armazenar 
o arquivo enviado à variável informada, e dessa forma, possibilitar a ciração do FileForm.

---
**WATCHER**

```
watch: {
    search(value) {
      if (this.search.length < 3) {
        this.showMessage = false
        this.clientes_fornecedor = []
      }
      if (this.search.length > 2) {
        this.showMessage = true
        this.doSearch(value)
      }
    }
  },
```
O Watcher, ou watch, como seu próprio nome indica, assiste alguma mudança que possa ocorrer. No desenvolvimento do sistema,
uma das ideias foi implementar a funcionalidade de filtro de forma dinâmica, ou seja, sem a necessidade de clicar em um botão para
consumir o serviço. Dessa forma, houve a implementação:
```
<div class="mt-10 text-center">
    <input v-model="search" class="rounded-2xl text-center z-10 p-3" placeholder="Filtrar" type="text"/>
</div>
```
O _watch_ observa o input com o v-model _search_, o qual possui o campo em _data_ como já informado. Dessa forma, a cada mudança, ocorre a chamada
da pesquisa de Clientes e Fornecedores para visualização na Interface _doSearch_. Para impedir uma consulta constante,
foi implementada a necessidade de que o campo possua no mínimo 3 caracteres para que a consulta seja realizada.

### Estilização
Apenas para referenciamento, a estilização dos componentes da página foi realizada com _Tailwind_. A implementação do Tailwind se deu pela conta da 
familiariedade com a ferramente e as opções ofertadas para construção de elementos no DOM com a utilização de diversas classes disponibilizadas.
---
## O BACKEND
### JAVA (SpringBoot) - MYSQL

A utilização de JAVA nesse sistema não foi por acaso. A escolha da linguagem e seu Framework foi realizada através da conclusão de possuir uma organização
bem estruturada. O Java é uma linguagem robusta, fortemente tipada com seu desenvolvimento voltado para Orientação a Objetos, o qual também é utilizado no desenvolvimento
de banco de dados. Dessa forma, torna-se mais viável, por conta da estratégia de criação de objetos semelhante na comunicação da linguagem com o Banco de Dados (MySql).<br>
O Padrão escolhido para esse projeto foi o MVC(Model, View, Controller). Como abordado em algumas partes do _Front End_ a controller tem um papel fundamental na chamada de serviços com
recebimento de dados do _Front-End_ ou no envio de informações à ‘interface’.

---
### Controllers
#### ConvertXmlJson
A controller possui apenas o Método de POST. O seu endpoint _/convert/xmlToJson_ permite que o arquivo enviado seja redirecionado para o serviço desejado.

#### ClienteController
A controller possui dois métodos _GET_, pois, no desenvolvimento de busca de informações, não houve necessidade de implementar o POSTMAPPING do cliente,
uma vez que, a criação de cliente se dá pela análise do arquivo XML enviado pelo usuário.
##### ("/cliente/getAll") - Retorna todos os clientes no Banco de Dados
##### ("/cliente/{documento}") - Retorna os clientes com o documento(cpf) informado.

#### NotaFiscalController
Possui apenas um GET, o qual retorna os Clientes e Fornecedores conforme o documento. O mesmo foi colocado em NotaFiscalController, pois na continuidade de uma implementação,
as informaçãoes completas dos mesmo serão trazidas, ou seja, a NotaFiscal completa.
##### ("/notafiscal/{documento}") - Retorna Clientes e Fornecedores com a inicialização do CPF ou CNPJ iguais ao documento informado

---
### Model
Os modelos Criados são as mesmas entidades criadas no Banco de dados. A notação de persistência abaixo garante que isso aconteça.
```
@Table(name = "nome_tabel")
@Entity
@Getter
@Setter
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
```
Em table cria-se a tabela.<br>
Em Entity cria-se a entidade daquele objeto.<br>
Em Getter cria-se os Getters de todos os campos do objeto.<br>
Em Setter cria-se os Setters de todos os campos do objeto.<br>
Em Data é garantida a persitência de dados.<br>
Em Builder é possível construir o objeto sem necessariamente instanciar com _new_.<br>

---
### Payload
Os Payloads são tratados como As requisições necessárias que a controller pode receber, ou as Responses que a Controller pode enviar.
O Paylaod.response.NFResponse, por exemplo, é utilizado para aramazenar o retorno dos clientes e fornecedores, e retornar à Controller.<br>
Os Payloads possuem também a notação _@Builder_, dessa forma, um serviço pode construir a resposta sem Instanciação, deixando o código mais legível e eficiente.

---
### Repository
Os repositórios são interfaces responsáveis pelas Queries com o Banco de dados. Ou seja, cada repositório é responsável por um modelo.

#### A implementação com o JPA
O JPA, Java Persistence API, possui uma linguagem de criação de consulta inteligente. Para uma determinada consulta, a API possui palavras reservadas,
para o nome da função resultante, que entende o retorno que será obtido e qual query, ou queries, devem ser feitas no Banco de Dados. Exemplo:
```
List<Fornecedor> findFornecedorsByCNPJStartsWith(String Cnpj);
```
O JPA entende da seguinte forma: _findFornecedores_, como a palavra está no plural, deve-se dar um "SELECT *" e o resultado vai ser o mapeamento para a Model de Fornecedores.
Porém, como eu vou achá-los? Qual o parâmetro? O mesmo é passado em seguida. _ByCNPJStartsWith_ é similar ao _LIKE %%_, porém, apenas a inicialização da palavra, pois, se o número do CPF ou CNPJ
que estivermos filtrando estiver no meio, ou separado pelo campo, não fará sentido em ser um resultado da busca que possui uma determinada ordem.

---
### SERVICES
#### Deserialize.DeserializeXML
O serviço de Deserialização do XML é realizado com o Jackson. O Jackson é um processador JSON de altoi desempenho. Com ele foi possível implementar a conversão de XML para JSON e criar o objeto necessário de acordo com o Modelo requerido.
<br>_SaveXml_ Possui a implementação do Mapeador para XML ser lido como JSON. Dessa forma, é criado um JsonNode, o qual faz a leitura do arquivo solicitado e o mapeia como nós em JSON.<br>
Sendo assim, para que cada componente pudesse receber um valor, o Objeto JsonNode permite fazer uma busca com base nas Tags XML. Dessa forma, para cada campo de cada modelo, foi passado o caminho e extraído o valor.
```
ClienteDTO clienteDTO = ClienteDTO.builder()
                .CPF(node.at("/NFe/infNFe/dest").get("CNPJ").asText())
                .nome(node.at("/NFe/infNFe/dest").get("xNome").asText())
                .endereco(enderecoDTOModel)
                .build();
                
FornecedorDTO fornecedorDTO = FornecedorDTO.builder()
                .CNPJ(node.at("/NFe/infNFe/emit").get("CNPJ").asText())
                .nome(node.at("/NFe/infNFe/emit").get("xNome").asText())
                .EnderecoEmissor(enderecoEmissorDTOModel)
                .build();
                
EnderecoDTO enderecoEmissorDTO = EnderecoDTO.builder()
                .CEP(node.at("/NFe/infNFe/emit/enderEmit").get("CEP").asText())
                .cMun(node.at("/NFe/infNFe/emit/enderEmit").get("cMun").asText())
                .cMun(node.at("/NFe/infNFe/emit/enderEmit").get("cMun").asText())
                .cPais(node.at("/NFe/infNFe/emit/enderEmit").get("cPais").asText())
                .xMun(node.at("/NFe/infNFe/emit/enderEmit").get("xMun").asText())
                .nro(node.at("/NFe/infNFe/emit/enderEmit").get("nro").asText())
                .UF(node.at("/NFe/infNFe/emit/enderEmit").get("UF").asText())
                .xLgr(node.at("/NFe/infNFe/emit/enderEmit").get("xLgr").asText())
                .xBairro(node.at("/NFe/infNFe/emit/enderEmit").get("xBairro").asText())
                .xPais(node.at("/NFe/infNFe/emit/enderEmit").get("xPais").asText())
                .fone(node.at("/NFe/infNFe/emit/enderEmit").get("fone").asText())
                .build();

        EnderecoDTO enderecoDTO = EnderecoDTO.builder()
                .CEP(node.at("/NFe/infNFe/dest/enderDest").get("CEP").asText())
                .cMun(node.at("/NFe/infNFe/dest/enderDest").get("cMun").asText())
                .cPais(node.at("/NFe/infNFe/dest/enderDest").get("cPais").asText())
                .xMun(node.at("/NFe/infNFe/dest/enderDest").get("xMun").asText())
                .nro(node.at("/NFe/infNFe/dest/enderDest").get("nro").asText())
                .UF(node.at("/NFe/infNFe/dest/enderDest").get("UF").asText())
                .xLgr(node.at("/NFe/infNFe/dest/enderDest").get("xLgr").asText())
                .xBairro(node.at("/NFe/infNFe/dest/enderDest").get("xBairro").asText())
                .xPais(node.at("/NFe/infNFe/dest/enderDest").get("xPais").asText())
                .fone(node.at("/NFe/infNFe/dest/enderDest").get("fone").asText())
                .build();
```
Como exemplos acima, o JsonNode possui a chamada de função _at_ o qual permite informar o caminho, como um URL até o valor desejado.<br>
Após informar o caminho, a função _get_ aceita como parâmetro uma string, referente ao nome do campo com o valor requerido. Por fim, a função _asText_ retorna
o valor do campo como texto para poder ser atribuído ao objeto em questão.


##### DTOS
Como os modelos que recebem as informações não estão presentes no banco de dados, e, além disso, como não é uma troca de informação entre controller e interface, foram criados os DTOS.<br>
Cada DTO criado possui os mesmos campos do model, com excessão do ID, pois como informado, eles não estão presentes ainda no Banco de Dados. Dessa forma, para que um DTO possa ser mapeado como um objeto de Modelo do Banco de dados,
foi implementado o código a seguir:
```
ModelMapper modelMapper = new ModelMapper();
```
O modelMapper possui a função no sistema de fazer o mapeamento entra a DTO e sua respectiva classe, para que, ao chamar o repositório, o modelo possa ser salvo no banco como o objeto requerido.