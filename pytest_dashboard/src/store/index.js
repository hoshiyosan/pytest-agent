import Vue from "vue";
import Vuex from "vuex";

import agent from "./agent";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: { agent },
});
