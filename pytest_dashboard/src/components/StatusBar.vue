<template>
  <div>
    <span
      v-for="(counter, status) in metrics"
      class="statusbar-icon"
      :key="status"
    >
      <status-icon :status="status" :counter="counter" />
    </span>
  </div>
</template>

<script>
import StatusIcon from "@/components/StatusIcon";

export default {
  components: { StatusIcon },
  props: {
    metrics: {
      type: Object,
      default: () => ({}),
    },
  },
};
</script>

<style scoped>
.statusbar-icon {
  margin-right: 1em;
}
</style>
