<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import vSelect from "vue-select";
import PulseLoader from "vue-spinner/src/PulseLoader.vue";
</script>

<template>
  <div v-show="!clicked && !got_response && !failed">
    <h1>IGCSE Past Paper Generator</h1>
    <h2>Select your studied subjects</h2>
    <v-select
      :modelValue="selected_subjects"
      @update:modelValue="selected_subjects = $event"
      :options="subject_list"
    ></v-select>
    <h2>Select your studied topics:</h2>
    <v-select
      :modelValue="selected_topics"
      @update:modelValue="selected_topics = $event"
      multiple
      :options="topic_list[selected_subjects]"
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

  <div v-show="failed">
    <h2>We could not generate exam papers with your selected topics.</h2>
    <h2>Please select another topics.</h2>
    <div style="margin-top: 50px">
      <button class="generate-button" @click="reset">Retry</button>
    </div>
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
    <h3>Marking Schemes</h3>
    <button class="generate-button" @click="show_comp2 = !show_comp2">
      component2
    </button>
    <button class="generate-button">
      <a :href="ms4" target="_blank">component4</a>
    </button>
    <button class="generate-button">
      <a :href="ms6" target="_blank">component6</a>
    </button>
    <div v-show="show_comp2">
      <table>
        <tr>
          <th>Q No.</th>
          <th>Answer</th>
        </tr>
        <tr v-for="answer in ms2">
          <th>{{ answer[0] }}</th>
          <td>{{ answer[1] }}</td>
        </tr>
      </table>
    </div>
    <h3>Grade Thresholds</h3>
    <table>
      <thead>
        <tr>
          <th>A*</th>
          <th>A</th>
          <th>B</th>
          <th>C</th>
          <th>D</th>
          <th>E</th>
          <th>F</th>
          <th>G</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td v-for="item in grade_thresholds">{{ item }}</td>
        </tr>
      </tbody>
    </table>
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
      failed: false,
      show_comp2: false,
      selected_topics: [],
      selected_subjects: [],
      topic_list: {
        Chemistry: [
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
        Physics: [
          "1. General Physics",
          "2. Thermal Physics",
          "3. Properties of Waves including Light and Sounds",
          "4. Electricity and Magnetism",
          "5. Atomic Physics",
        ],
        Biology: ["1. Molecule"],
      },
      subject_list: ["Chemistry", "Physics", "Biology"],
      component2: "",
      component4: "",
      component6: "",
      ms2: [],
      ms4: "",
      ms6: "",
      grade_thresholds: [180, 170, 160, 150, 140, 130, 120, 110],
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
      if (
        this.selected_topics.length == 0 ||
        this.selected_option.length == 0
      ) {
        this.show_error_msg = true;
      } else {
        this.clicked = true;
        this.sendRequest();
      }
    },
    sendRequest: async function () {
      try {
        const response = await fetch(
          "https://igcse-backend.onrender.com/generate",
          {
            method: "post",
            headers: {
              "Content-Type": "application/json; charset=utf-8",
            },
            body: JSON.stringify({
              subject: this.selected_subjects,
              topics: this.selected_topics,
              options: this.option_map[this.selected_option],
            }),
          }
        );

        const data = await response.json();

        this.component2 = await this.get_pdf_download_url(data.pdfs.component2);
        this.component4 = await this.get_pdf_download_url(data.pdfs.component4);
        this.component6 = await this.get_pdf_download_url(data.pdfs.component6);

        this.ms4 = await this.get_pdf_download_url(
          data.marking_schemes.component4
        );
        this.ms6 = await this.get_pdf_download_url(
          data.marking_schemes.component6
        );

        this.ms2 = data.marking_schemes.component2;
        this.grade_thresholds = data.grade_thresholds;

        this.got_response = true;
        this.clicked = false;
      } catch (e) {
        this.failed = true;
        this.clicked = false;
      }
    },
    get_pdf_download_url: async function (pdf_path) {
      const pdfReference = ref(storage, pdf_path);
      const pdfURL = await getDownloadURL(pdfReference);
      return pdfURL;
    },
    reset() {
      this.clicked = false;
      this.got_response = false;
      this.failed = false;
      this.show_error_msg = false;
      this.show_comp2 = false;
      this.component2 = "";
      this.component4 = "";
      this.component6 = "";
      this.selected_topics = [];
      this.selected_option = [];
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

table {
  width: 100%;
  border: 1px solid;
}

th,
td {
  border: 1px solid;
}
</style>
