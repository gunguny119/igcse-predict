<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import vSelect from "vue-select";
import PulseLoader from "vue-spinner/src/PulseLoader.vue";
</script>

<template>
  <div v-show="!clicked && !got_response">
    <h1>IGCSE Chemistry</h1>
    <h2>Select your studied topics:</h2>
    <v-select
      v-model="selected_topics"
      multiple
      :options="topic_list"
    ></v-select>
    <p v-show="show_error_msg" style="color: red">
      Please select one or more topics.
    </p>
    <button class="generate-button" @click="onGeneratePaper">
      Generate Paper
    </button>
  </div>

  <div v-show="clicked">
    <h1>Generating Paper...</h1>
    <pulse-loader color="green"></pulse-loader>
  </div>

  <div v-show="got_response">
    <h1>Server Response</h1>
    <p>component2 : {{ component2 }}</p>
    <p>component4 : {{ component4 }}</p>
    <p>component6 : {{ component6 }}</p>
    <button class="generate-button" @click="reset">Retry</button>
  </div>
</template>

<script>
import storage from "./components/load_firebase";
import { ref, getDownloadURL } from "firebase/storage";

export default {
  name: "App",
  data() {
    return {
      clicked: false,
      show_error_msg: false,
      got_response: false,
      selected_topics: [],
      topic_list: [
        "1 The particulate nature of matter",
        "2 Experimental techniques",
        "3 Atoms, elements and compounds",
        "4 Stoichiometry",
        "5 Electricity and chemistry",
        "6 Chemical energetics",
        "7 Chemical reactions",
        "8 Acids, bases and salts",
        "9 The Periodic Table",
        "10 Metals",
        "11 Air and water",
        "12 Sulfur",
        "13 Carbonates",
        "14 Organic chemistry",
      ],
      component2: "",
      component4: "",
      component6: "",
      selected_option: ["22", "42", "62"],
    };
  },
  methods: {
    onGeneratePaper() {
      if (this.selected_topics.length == 0) {
        this.show_error_msg = true;
      } else {
        this.clicked = true;
        this.sendRequest();
      }
    },
    sendRequest: async function () {
      const response = await fetch(
        "https://127.0.0.1:5000/generate",
        {
          method: "post",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ topics: this.selected_topics, options: this.selected_option }),
        }
      );

      const data = await response.json();

      this.component2 = await this.get_pdf_donwload_url(data.component2);
      this.component4 = await this.get_pdf_donwload_url(data.component4);
      this.component6 = await this.get_pdf_donwload_url(data.component6);

      this.got_response = true;
      this.clicked = false;
    },
    get_pdf_download_url: async function(pdf_path){
      const pdfReference = ref(storage, pdf_path);
      const pdfURL = await getDownloadURL(pdfReference);
      return pdfURL
    },
    reset() {
      this.clicked = false;
      this.got_response = false;
      this.component2 = "";
      this.component4 = "";
      this.component6 = "";
      this.selected_topics = [];
    },
  },
};
</script>

<style scoped>
.generate-button {
  background-color: #646cffaa;
}

.generate-button:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
</style>
