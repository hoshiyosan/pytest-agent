<template>
  <v-app>
    <v-app-bar app color="black" dark>
      <div class="d-flex align-center">
        <v-img
          class="shrink mr-2"
          contain
          src="@/assets/logo.png"
          transition="scale-transition"
          width="40"
        />
      </div>

      <v-spacer></v-spacer>

      <v-btn
        @click="isSelectAgentDialogDisplayed = true"
        title="click to select agent url"
      >
        {{ selectAgentMessage }}
      </v-btn>
    </v-app-bar>

    <select-agent-dialog v-model="isSelectAgentDialogDisplayed" />

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import SelectAgentDialog from "@/dialogs/SelectAgentDialog";
import { mapState } from "vuex";

export default {
  name: "App",
  components: { SelectAgentDialog },

  data: () => ({
    isSelectAgentDialogDisplayed: false,
  }),

  computed: {
    ...mapState("agent", ["selectedAgent"]),
    selectAgentMessage() {
      return !this.selectedAgent
        ? "Connect to a pytest agent"
        : this.selectedAgent;
    },
  },
};
</script>
