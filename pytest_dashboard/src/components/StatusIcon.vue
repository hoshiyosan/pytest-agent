<template>
  <span :class="statusColor + '--text'" :title="title">
    <v-icon :color="statusColor">{{ statusIcon }}</v-icon>
    {{ counter }}
  </span>
</template>

<script>
const STATUS_COLOR = {
  "n/a": "orange",
  succeed: "green",
  failed: "red",
  running: "blue",
  pending: "teal",
  total: "white",
};

const STATUS_ICON = {
  "n/a": "mdi-cancel",
  succeed: "mdi-check",
  failed: "mdi-alert-circle",
  running: "mdi-run-fast",
  pending: "mdi-sleep",
  total: "mdi-magnify",
};

export default {
  props: {
    status: {
      type: String,
      default: "n/a",
    },
    counter: {
      type: Number,
      default: null,
    },
  },
  computed: {
    statusColor() {
      return STATUS_COLOR[this.status];
    },
    statusIcon() {
      return STATUS_ICON[this.status];
    },
    title() {
      return (this.counter ? this.counter + " " : "") + this.status;
    },
  },
};
</script>
