<template>
  <div class="grid grid-cols-3 grid-rows-3 h-screen w-screen overflow-x-hidden place-items-center" style="background-color: #381D2A">
    <div class="font-bold col-span-full text-center p-20">
      <h1 class="sm:text-5xl text-2xl text-center" style="color: #FCDE9C">
        RECOMB NFe DESERIALIZER
      </h1>
      <p class="text-white sm:text-lg text-sm">
        Digite mais de 2 caracteres para filtrar
      </p>
      <div class="mt-10 text-center">
        <!--      <p class="text-white">Digite mais {{ 3 - this.search.length }} caracteres</p>-->
        <input v-model="search" class="rounded-2xl text-center z-10 p-3" placeholder="Filtrar" type="text"/>
      </div>
    </div>
    <div v-if="this.clientes_fornecedor.length === 0 && this.search.length < 3" class="text-center sm:mt-0 mt-20 col-span-full row-start-2 font-semibold text-xl">
      <div class="rounded-3xl p-10 w-full h-full" style="background-color: #BA5624">
        <div class="text-white font-bold">
          SEND YOUR FILE
        </div>
        <form @submit.prevent="sendFile">
          <input
              ref="uploadImage"
              accept=".xml"
              class="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"
              type="file" @change="onImageUpload()">
          <button class="w-full block focus:bg-indigo-400 text-white font-semibold rounded-lg
              px-4 py-3 mt-6" style="background-color: #FCDE9C" type="submit">ENVIAR
          </button>
        </form>
      </div>
    </div>
    <div v-if="this.showMessage" class="col-span-full">
      <h2 class="text-white text-center">
        Infelizmente não houve resultado para a busca do CNPJ/CPF {{ this.search }}
      </h2>
    </div>
    <div v-for="fornecedor in this.clientes_fornecedor.fornecedores" class="text-white p-3 sm:col-span-1 col-span-full">
      <div
          class="block  rounded-lg bg-white p-6 shadow-[0_2px_15px_-3px_rgba(0,0,0,0.07),0_10px_20px_-2px_rgba(0,0,0,0.04)] dark:bg-neutral-700">
        <h2>
          <b>FORNECEDOR</b>
        </h2>
        <h5
            class="mb-2 text-xl font-medium leading-tight text-neutral-800 dark:text-neutral-50">
          {{ fornecedor.nome }}
        </h5>
        <div class="mb-4 text-base text-neutral-600 dark:text-neutral-200">
          <p>
            Endereco Fornecedor: {{ fornecedor.endereco.xlgr }}, {{ fornecedor.endereco.nro }}, {{ fornecedor.endereco.xbairro }}, {{ fornecedor.endereco.xmun }}, {{ fornecedor.endereco.xpais }}
          </p>
        </div>
      </div>
    </div>
    <div v-for="cliente in this.clientes_fornecedor.clientes" class="text-white p-3">
      <div
          class="block rounded-lg bg-white p-6 shadow-[0_2px_15px_-3px_rgba(0,0,0,0.07),0_10px_20px_-2px_rgba(0,0,0,0.04)] dark:bg-neutral-700">
        <h2>
          <b>CLIENTE</b>
        </h2>
        <h5
            class="mb-2 text-xl font-medium leading-tight text-neutral-800 dark:text-neutral-50">
          {{ cliente.nome }}
        </h5>
        <div class="mb-4 text-base text-neutral-600 dark:text-neutral-200">
          <p>
            Endereco Cliente: {{ cliente.endereco.xlgr }}, {{ cliente.endereco.nro }}, {{ cliente.endereco.xbairro }}, {{ cliente.endereco.xmun }}, {{ cliente.endereco.xpais }}
          </p>
        </div>
        <button
            type="button"
            class="inline-block rounded bg-primary px-6 pb-2 pt-2.5 text-xs font-medium uppercase leading-normal text-white shadow-[0_4px_9px_-4px_#3b71ca] transition duration-150 ease-in-out hover:bg-primary-600 hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:bg-primary-600 focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:outline-none focus:ring-0 active:bg-primary-700 active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] dark:shadow-[0_4px_9px_-4px_rgba(59,113,202,0.5)] dark:hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)]"
            data-te-ripple-init
            data-te-ripple-color="light">
          Consultar
        </button>
      </div>
    </div>
    <div v-if="this.resp"
         class="relative col-span-full text-white text-2xl font-bold animate-fade-up animate-once animate-duration-[2000ms] animate-ease-in-out animate-normal">
      <p class="text-center">
        Analise Concluida
      </p>
    </div>
  </div>

  <div v-if="this.resp" class="w-screen h-screen grid overflow-x-hidden p-3 place-items-center">
    <div class="text-2xl text-center bg-blue-500 w-1/4 rounded-2xl p-5">
      <h1 class="font-bold text-white">
        Dados do Fornecedor
      </h1>
      <div class="col-span-full text-center">
        <p class="text-sm">
          <b>Nome do Fornecedor:</b> {{ this.resp.fornecedor.nome }}
        </p>
        <p class="text-sm">
          <b>CNPJ do Fornecedor:</b> {{ this.resp.fornecedor.cnpj }}
        </p>
      </div>
    </div>
    <div class="text-2xl text-center bg-blue-500 w-1/4 rounded-2xl">
      <h1 class="font-bold text-white">
        Dados do Cliente
      </h1>
      <div class="col-span-full text-center p-5">
        <p class="text-sm mb-5">
          <b>Nome do Cliente:</b> {{ this.resp.cliente.nome }}
        </p>
        <p class="text-sm mb-5">
          <b>CPF do Cliente:</b> {{ this.resp.cliente.cpf }}
        </p>
        <h2 class="font-bold text-white">
          Endereco
        </h2>
        <p class="text-sm">
          <b>Logradouro:</b> {{ this.resp.cliente.endereco.xlgr }}
        </p>
        <p class="text-sm">
          <b>Numero:</b> {{ this.resp.cliente.endereco.nro }}
        </p>
        <p class="text-sm">
          <b>Bairro:</b> {{ this.resp.cliente.endereco.xbairro }}
        </p>
        <p class="text-sm">
          <b>Municipio:</b> {{ this.resp.cliente.endereco.xmun }}
        </p>
        <p class="text-sm">
          <b>CEP:</b> {{ this.resp.cliente.endereco.cep }}
        </p>
        <p class="text-sm">
          <b>Pais:</b> {{ this.resp.cliente.endereco.xpais }}
        </p>
      </div>
    </div>
    <div class="text-2xl text-center bg-blue-500 w-1/4 rounded-2xl p-5">
      <h1 class="font-bold text-white">
        Dados do Boleto
      </h1>
      <div v-for="boleto in this.resp.boleto" class="col-span-full text-center mt-3">
        <p class="text-sm">
          Valor do boleto: <b>{{ boleto.value }}</b>
        </p>
        <p class="text-sm">
          Data de vencimento: <b>{{ boleto.dataVencimento }}</b>
        </p>
        <p class="text-sm">
          Valor Parcelado: <b>{{ boleto.valorParcelado }}</b>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import {searchClient, sendFileXML} from "../service/axiosService";

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
  created() {
    this.resp = ""
  }
}
</script>

<style scoped>

</style>

