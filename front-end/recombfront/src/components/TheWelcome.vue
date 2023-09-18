<template>
  <div class="grid grid-cols-3 grid-rows-3 h-screen w-screen" style="background-color: #381D2A">
    <div class="font-bold col-span-full flex items-center justify-items-start text-center p-3 text-5xl">
      <h1 style="color: #FCDE9C" class="">
        RECOMB NFe DESERIALIZER
      </h1>
    </div>
    <div class="text-center col-start-2 flex items-center font-semibold text-xl">
      <div class="rounded-3xl p-10 w-full h-full" style="background-color: #BA5624">
        <div class="text-white font-bold">
          SEND YOUR FILE
        </div>
        <form @submit.prevent="sendFile">
          <input
              class="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"
              type="file" ref="uploadImage" @change="onImageUpload()">
          <button type="submit" class="w-full block focus:bg-indigo-400 text-white font-semibold rounded-lg
              px-4 py-3 mt-6" style="background-color: #FCDE9C">ENVIAR
          </button>
        </form>
      </div>

    </div>

  </div>
  <div v-if="this.resp">
    <div>

    </div>
  </div>
  <p v-if="this.resp" class="text-white text-sm">
    {{ this.resp.fornecedor.nome }}
  </p>
</template>

<script>
import {sendFileXML, teste} from "../service/axiosService";

export default {
  name: "TheWelcome",
  data() {
    return {
      xml_file: null,
      resp: null
    }
  },
  methods: {
    sendFile() {
      let FileForm = new FormData();
      FileForm.append("fileNf", this.xml_file);
      sendFileXML(FileForm).then((response) => (this.resp = response.data))
          .then((response) =>
              this.resp = this.resp.map((d) => {
                return {
                  boleto: d.boleto,
                  cliente: d.cliente,
                  fornecedor: d.fornecedor,
                };
              }));
    },
    onImageUpload() {
      this.xml_file = this.$refs.uploadImage.files[0];
    }
  }
}
</script>

<style scoped>

</style>
