<template>
  <main>
    <v-container style="padding-bottom: 3em">
      <h2>Welcome home</h2>
      <v-text-field label="Tipe a search here to filter tests" />
      <test-list
        v-model="selectedTests"
        :modules="testModules"
        @click="showTestOutput"
      />
    </v-container>

    <div
      style="
        z-index: 10;
        position: fixed;
        display: flex;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: #424242;
        padding: 8px 2em;
      "
    >
      <status-bar :metrics="testMetrics" />
      <v-spacer></v-spacer>

      <span style="color: white">
        {{ selectedTestsCounter }} test(s) selected
      </span>
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
    <test-output-dialog v-model="isOutputDisplayed" :output="displayedOutput" />
  </main>
</template>

<script>
import StatusBar from "@/components/StatusBar";
import TestList from "@/components/TestList";
import TestOutputDialog from "@/dialogs/TestOutputDialog";

import { mapGetters, mapState } from "vuex";

export default {
  name: "Home",
  components: { StatusBar, TestList, TestOutputDialog },
  data: () => ({
    selectedTests: [],
    displayedOutput: null,
    isOutputDisplayed: false,
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
    dismissResults() {
      this.$store.dispatch("agent/collectTests");
    },
    showTestOutput(fullname) {
      this.$store.dispatch("agent/getTestOutput", fullname).then((output) => {
        this.displayedOutput = output;
        this.isOutputDisplayed = true;
      });
    },
  },
};
</script>

<style scoped>
.v-icon {
  margin-left: 1em;
}
</style>
