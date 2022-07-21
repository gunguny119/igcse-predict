<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import vSelect from "vue-select";
</script>

<template>
  <div v-show="!clicked">
    <h1>IGCSE Chemistry</h1>
    <h2>Select your studied topcis:</h2>
    <v-select
      v-model="selected_topics"
      multiple
      :options="topic_list"
    ></v-select>
    <button class="generate-button" @click="onGeneratePaper">
      Generate Paper
    </button>
  </div>

  <div v-show="clicked">
    <h1>Server Respone</h1>
    <p>component2 : {{ component2 }}</p>
    <p>component4 : {{ component4 }}</p>
    <p>component6 : {{ component6 }}</p>
    <button class="generate-button" @click="reset">Retry</button>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      clicked: false,
      selected_topics: [],
      topic_list: ["Organic Chemistry", "State of Matter", "Electrolysis"],
      component2: [],
      component4: [],
      component6: [],
    };
  },
  methods: {
    onGeneratePaper() {
      this.clicked = true;
      this.sendRequest();
    },
    sendRequest: async function () {
      const response = await fetch("http://127.0.0.1:5000/generate", {
        method: "post",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ topics: this.selected_topics }),
      });

      const data = await response.json();
      this.component2 = data.component2;
      this.component4 = data.component4;
      this.component6 = data.component6;
    },
    reset() {
      this.clicked = false;
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
