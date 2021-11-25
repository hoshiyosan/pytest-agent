import axios from "axios";

const SECONDS = 1000;
const REFRESH_TIMEOUT = 5 * SECONDS;

const http = axios.create();

function loadAgents() {
  let agents;
  try {
    agents = JSON.parse(localStorage.getItem("agentURLs"));
    if (!agents) {
      console.log("No agents reloaded");
      return [];
    }
  } catch {
    console.log("No agents reloaded");
    return [];
  }
  console.log("agents reloaded", agents);
  return agents;
}

function countStatuses(tests) {
  const statusCounter = { total: 0 };
  for (let test of tests) {
    if (!statusCounter[test.status]) statusCounter[test.status] = 0;
    statusCounter[test.status] += 1;
    statusCounter.total += 1;
  }
  return statusCounter;
}

function getTestGroupStatuses(tests) {
  const statusCounter = countStatuses(tests);

  const statuses = [];
  if (statusCounter.failed > 0) {
    statuses.push("failed");
  } else if (statusCounter.succeed === statusCounter.total) {
    statuses.push("succeed");
  }

  if (statusCounter.running > 0) {
    statuses.push("running");
  } else if (statusCounter.pending > 0) {
    statuses.push("pending");
  }

  if (statuses.length === 0) {
    statuses.push("n/a");
  }

  return statuses;
}

export default {
  namespaced: true,

  state: {
    selectedAgent: null,
    agentURLs: loadAgents(),
    tests: [],
  },

  getters: {
    agentURLs(state) {
      return state.agentURLs;
    },
    isConnected(state) {
      return !!state.selectedAgent;
    },
    testMetrics(state) {
      return countStatuses(state.tests);
    },
    testModules(state) {
      const modules = {};
      console.log(state.tests);
      for (let test of state.tests) {
        if (!(test.modulename in modules)) {
          modules[test.modulename] = { modulename: test.modulename, tests: [] };
        }
        modules[test.modulename].tests.push(test);
      }
      Object.values(modules).map(
        (testModule) =>
          (testModule.statuses = getTestGroupStatuses(testModule.tests))
      );
      return modules;
    },
  },

  mutations: {
    addAgent(state, agentURL) {
      state.agentURLs.push(agentURL);
      console.log(state.agentURLs.map((url) => url));
      localStorage.setItem("agentURLs", JSON.stringify(state.agentURLs));
    },
    useAgent(state, agentURL) {
      state.selectedAgent = agentURL;
      http.defaults.baseURL = agentURL;
      state.tests = [];
    },
    setTests(state, tests) {
      state.tests = tests;
    },
  },

  actions: {
    setTests({ commit, dispatch }, tests) {
      commit("setTests", tests);

      let shouldRefresh = false;
      for (let test of tests) {
        if (test.status === "pending" || test.status === "running") {
          shouldRefresh = true;
          console.log("triggering refresh, culprit:", test);
          break;
        }
      }
      if (shouldRefresh) {
        setTimeout(() => dispatch("refreshTestResults"), REFRESH_TIMEOUT);
      }
    },
    async refreshTestResults({ dispatch }) {
      const response = await http.get("/tests/summary");
      dispatch("setTests", response.data);
    },
    async addAgent({ commit, dispatch }, agentURL) {
      commit("addAgent", agentURL);
      await dispatch("useAgent", agentURL);
    },
    async useAgent({ commit, dispatch }, agentURL) {
      commit("useAgent", agentURL);
      if (agentURL) {
        await dispatch("refreshTestResults");
      }
    },
    async runTests({ dispatch }, tests) {
      const response = await http.post("/tests/run", tests);
      dispatch("setTests", response.data);
    },
    async collectTests({ dispatch }) {
      const response = await http.post("/tests/collect");
      dispatch("setTests", response.data);
    },
    async getTestOutput(context, testFullname) {
      const response = await http.get(`/tests/output/${testFullname}`);
      return response.data;
    },
  },
};
