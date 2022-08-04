<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import vSelect from "vue-select";
import PulseLoader from "vue-spinner/src/PulseLoader.vue";
import EasyDataTable from "vue3-easy-data-table";
</script>

<template>
  <div v-show="!clicked && !got_response">
    <h1>IGCSE Chemistry</h1>
    <h2>Select your studied topics:</h2>
    <v-select
      :modelValue="selected_topics"
      @update:modelValue="selected_topics = $event"
      multiple
      :options="topic_list"
    ></v-select>
    <h2>Also, select your component option:</h2>
    <v-select
      :modelValue="selected_option"
      @update:modelValue="selected_option = $event"
      :options="['CX', 'CY', 'CZ']"
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
    <h3>Question Papers</h3>
    <button class="generate-button">
      <a :href="component2" target="_blank">component2</a>
    </button>
    <button class="generate-button">
      <a :href="component4" target="_blank">component4</a>
    </button>
    <button class="generate-button">
      <a :href="component6" target="_blank">component6</a>
    </button>
    <h3>Grade Thresholds</h3>
    <EasyDataTable
      :headers="[
        { text: 'A*', value: 'A*' },
        { text: 'A', value: 'A' },
        { text: 'B', value: 'B' },
        { text: 'C', value: 'C' },
        { text: 'D', value: 'D' },
        { text: 'E', value: 'E' },
        { text: 'F', value: 'F' },
        { text: 'G', value: 'G' },
      ]"
      :items="grade_thresholds"
    />
    <div style="margin-top: 50px">
      <button class="generate-button" @click="reset">Retry</button>
    </div>
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
      grade_list: ["A*", "A", "B", "C", "D", "E", "F", "G"],
      component2: "",
      component4: "",
      component6: "",
      grade_thresholds: [
        {
          "A*": "180>",
          A: "170>",
          B: "160>",
          C: "150>",
          D: "140>",
          E: "130>",
          F: "120>",
          G: "110>",
        },
      ],
      selected_option: [],
      option_map: {
        CX: [21, 41, 61],
        CY: [22, 42, 62],
        CZ: [23, 43, 63],
      },
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
      const response = await fetch("http://127.0.0.1:5000/generate", {
        method: "post",
        headers: {
          "Content-Type": "application/json; charset=utf-8",
        },
        body: JSON.stringify({
          topics: this.selected_topics,
          options: this.option_map[this.selected_option],
        }),
      });

      const data = await response.json();

      this.component2 = await this.get_pdf_download_url(data.pdfs.component2);
      this.component4 = await this.get_pdf_download_url(data.pdfs.component4);
      this.component6 = await this.get_pdf_download_url(data.pdfs.component6);
      this.grade_thresholds = {};
      this.grade_thresholds = {};
      this.grade_list.forEach(
        (key, i) => (this.grade_thresholds[key] = data.grade_thresholds[i])
      );
      this.grade_thresholds = [this.grade_thresholds];

      this.got_response = true;
      this.clicked = false;
    },
    get_pdf_download_url: async function (pdf_path) {
      const pdfReference = ref(storage, pdf_path);
      const pdfURL = await getDownloadURL(pdfReference);
      return pdfURL;
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
