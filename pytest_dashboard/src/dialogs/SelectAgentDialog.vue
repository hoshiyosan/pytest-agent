<template>
  <v-dialog v-model="isDialogDisplayed" width="500">
    <v-card>
      <v-toolbar color="primary" dark>Opening from the bottom</v-toolbar>
      <v-card-text style="padding-top: 1em">
        <div v-if="agentURLs.length > 0">
          <p>Use an existing agent</p>
          <v-select
            label="Select an existing agent"
            :items="agentURLs"
            @change="useAgent"
            return-object
          />
        </div>

        <form @submit.prevent="addAgent(newAgentURL)">
          <p>
            <strong v-if="agentURLs.length > 0">OR</strong>
            Connect to a new agent
          </p>
          <v-row>
            <v-text-field
              label="Type a new agent URL"
              v-model="newAgentURL"
              required
            />
            <v-btn color="primary" type="submit" icon>
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </v-row>
        </form>
      </v-card-text>

      <v-card-actions class="justify-end">
        <v-btn text @click="disconnect()" color="red">Disconnect</v-btn>
        <v-btn text @click="isDialogDisplayed = false">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  data: () => ({
    isDialogDisplayed: false,
    newAgentURL: null,
  }),
  computed: {
    ...mapGetters("agent", ["agentURLs"]),
  },
  props: {
    value: {
      type: Boolean,
      default: false,
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
  methods: {
    addAgent() {
      this.$store.dispatch("agent/addAgent", this.newAgentURL);
      this.isDialogDisplayed = false;
    },
    useAgent(agentURL) {
      this.$store.dispatch("agent/useAgent", agentURL);
      this.isDialogDisplayed = false;
    },
    disconnect() {
      this.$store.dispatch("agent/useAgent", null);
      this.isDialogDisplayed = false;
    },
  },
};
</script>
