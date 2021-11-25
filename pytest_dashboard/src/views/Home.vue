<template>
  <main>
    <v-container>
      <h2>Welcome home</h2>
      <v-text-field label="Tipe a search here to filter tests" />
      <test-list v-model="selectedTests" :modules="testModules" />
    </v-container>

    <div
      style="
        position: fixed;
        display: flex;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.1);
        padding: 8px 2em;
      "
    >
      <status-bar :metrics="testMetrics" />
      <v-spacer></v-spacer>

      {{ selectedTestsCounter }} test(s) selected
      <v-icon
        color="green"
        @click="refreshResults()"
        title="Refresh test results"
      >
        mdi-refresh
      </v-icon>

      <v-icon
        color="green"
        @click="runSelectedTests()"
        title="Run selected tests"
        v-if="selectedTestsCounter > 0"
      >
        mdi-play-circle
      </v-icon>
      <v-icon
        color="orange"
        @click="selectFailed()"
        title="Select failed tests"
      >
        mdi-alert-circle
      </v-icon>

      <v-icon color="blue" @click="selectAll()" title="Select all tests">
        mdi-checkbox-multiple-marked-outline
      </v-icon>
      <v-icon color="accent" @click="deselectAll()" title="Deselect all tests">
        mdi-close-circle
      </v-icon>

      <v-icon color="red" @click="dismissResults()" title="Clear test results">
        mdi-delete
      </v-icon>
    </div>
  </main>
</template>

<script>
import StatusBar from "@/components/StatusBar";
import TestList from "@/components/TestList";

import { mapGetters, mapState } from "vuex";

export default {
  name: "Home",
  components: { StatusBar, TestList },
  data: () => ({
    selectedTests: [],
  }),
  computed: {
    ...mapState("agent", ["tests"]),
    ...mapGetters("agent", ["testMetrics", "testModules"]),
    selectedTestsCounter() {
      return this.selectedTests.length;
    },
  },
  methods: {
    selectTest(fullname) {
      if (!this.selectedTests.includes(fullname)) {
        this.selectedTests.push(fullname);
      }
    },
    runSelectedTests() {
      this.$store
        .dispatch("agent/runTests", this.selectedTests)
        .then(() => this.deselectAll());
    },
    selectAll() {
      for (let test of this.tests) {
        this.selectTest(test.fullname);
      }
    },
    selectFailed() {
      for (let test of this.tests) {
        if (test.status === "failed") {
          this.selectTest(test.fullname);
        }
      }
    },
    deselectAll() {
      this.selectedTests = [];
    },
    refreshResults() {
      this.$store.dispatch("agent/refreshTestResults");
    },
  },
};
</script>

<style scoped>
.v-icon {
  margin-left: 1em;
}
</style>
