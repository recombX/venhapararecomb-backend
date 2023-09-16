<template>
  <div class="grid grid-cols-3 grid-rows-3 h-screen w-screen">
    <div class="font-bold col-span-full text-center text-3xl">
      RECOMB NFe Serializer
    </div>
    <div class="text-center col-start-2 flex items-center font-semibold text-xl">
      <div class="bg-blue-500 rounded-3xl p-10 w-full h-full">
        <div class="text-white font-bold">
          SEND YOUR FILE
        </div>
        <form @submit.prevent="sendFile">
          <input class="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400" type="file" ref="uploadImage" @change="onImageUpload()">
          <button type="submit" class="w-full block bg-green-500 hover:bg-green-700 focus:bg-indigo-400 text-white font-semibold rounded-lg
              px-4 py-3 mt-6">ENVIAR</button>
        </form>
      </div>

    </div>

  </div>
</template>

<script>
import {sendFileXML, teste} from "../service/axiosService";

export default {
  name: "TheWelcome",
  data()
  {
    return{
      xml_file: null,
    }
  },
  methods: {
    sendFile(){
      let FileForm = new FormData();
      FileForm.append("fileNf", this.xml_file);
      sendFileXML(FileForm).then((response) => {
        if(response.status !== 200 || response.status !== 201){
          alert("ENVIADO")
        }
      })
    },
    onImageUpload(){
      this.xml_file = this.$refs.uploadImage.files[0];
    }
  }
}
</script>

<style scoped>

</style>
