<template>
  <v-dialog v-model="isDialogDisplayed">
    <v-card>
      <v-toolbar color="primary" dark>Test Output</v-toolbar>
      <pre class="code" v-html="prettyOutput"></pre>
    </v-card>
  </v-dialog>
</template>

<script>
const LOG_COLORS = {
  ERROR: "red",
  WARNING: "orange",
  INFO: "blue",
  DEBUG: "green",
};

export default {
  data: () => ({
    isDialogDisplayed: false,
  }),
  computed: {
    prettyOutput() {
      if (!this.output) {
        return null;
      }

      let prettyOutput = this.output;
      Object.keys(LOG_COLORS).forEach(
        (logLevel) =>
          (prettyOutput = prettyOutput.replaceAll(
            logLevel,
            `<span color="${LOG_COLORS[logLevel]}">${logLevel}</span>`
          ))
      );
      return prettyOutput;
    },
  },
  props: {
    value: {
      type: Boolean,
      default: false,
    },
    output: {
      type: String,
      default: "",
    },
  },
  watch: {
    value: {
      immediate: true,
      handler(displayed) {
        this.isDialogDisplayed = displayed;
      },
    },
    isDialogDisplayed: {
      immediate: true,
      handler(displayed) {
        this.$emit("input", displayed);
      },
    },
  },
};
</script>

<style>
.code {
  font-size: 0.8em;
  color: whitesmoke;
  background-color: #212121;
  padding: 8px;

  white-space: pre-wrap; /* Since CSS 2.1 */
  white-space: -moz-pre-wrap; /* Mozilla, since 1999 */
  white-space: -pre-wrap; /* Opera 4-6 */
  white-space: -o-pre-wrap; /* Opera 7 */
  word-wrap: break-word; /* Internet Explorer 5.5+ */
}

.code span[color="green"] {
  color: rgb(76, 175, 80);
}
.code span[color="blue"] {
  color: rgb(33, 150, 243);
}
.code span[color="red"] {
  color: rgb(244, 67, 54);
}
.code span[color="orange"] {
  color: #ffc107;
}
</style>
