<template>
  <div>
    <v-menu
      v-model="isContextMenuDisplayed"
      :position-x="contextMenu.x"
      :position-y="contextMenu.y"
      absolute
      offset-y
    >
      <v-list>
        <v-list-item @click="selectAllModuleTests()">
          <v-list-item-title> Select All </v-list-item-title>
          <v-list-item-action>
            <v-icon style="margin-left: 0.5em" color="blue">
              mdi-checkbox-multiple-marked-outline
            </v-icon>
          </v-list-item-action>
        </v-list-item>
        <v-list-item @click="deselectAllModuleTests()">
          <v-list-item-title> Deselect All </v-list-item-title>
          <v-list-item-action>
            <v-icon style="margin-left: 0.5em" color="orange" right>
              mdi-close-circle
            </v-icon>
          </v-list-item-action>
        </v-list-item>
      </v-list>
    </v-menu>

    <v-expansion-panels>
      <v-expansion-panel
        v-for="testModule in modules"
        :key="testModule.modulename"
      >
        <v-expansion-panel-header
          @contextmenu.prevent="showContextMenu(testModule, $event)"
        >
          {{ testModule.modulename }}
          <template v-slot:actions>
            <StatusIcon
              v-for="status in testModule.statuses"
              :status="status"
              :key="status"
            />
          </template>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-list dense>
            <v-list-item-group color="primary">
              <v-list-item
                v-for="test in testModule.tests"
                :key="test.fullname"
                @click="emitClick(test.fullname)"
              >
                <v-checkbox
                  v-model="selectedTests"
                  :value="test.fullname"
                  @click.stop
                ></v-checkbox>

                <v-list-item-content>
                  <v-list-item-title v-text="test.funcname"></v-list-item-title>
                </v-list-item-content>

                <v-list-item-icon>
                  <i style="margin-right: 0.5em">
                    {{ test.refresh_date | humandate }}
                  </i>
                  <StatusIcon :status="test.status" />
                </v-list-item-icon>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script>
import StatusIcon from "@/components/StatusIcon";

export default {
  components: { StatusIcon },
  data: () => ({
    selectedTests: [],
    isContextMenuDisplayed: false,
    contextMenu: { x: 0, y: 0, testModule: null },
  }),
  props: {
    tests: {
      type: Array,
      default: () => [],
    },
    value: {
      type: Array,
      default: () => [],
    },
    modules: { type: Object, default: () => ({}) },
  },
  watch: {
    selectedTests: {
      handler(value) {
        this.$emit("input", value);
      },
    },
    value(v) {
      this.selectedTests = v;
    },
  },
  filters: {
    humandate(s) {
      return new Date(s).toLocaleString();
    },
  },
  methods: {
    emitClick(testFullname) {
      this.$emit("click", testFullname);
    },
    showContextMenu(testModule, event) {
      this.isContextMenuDisplayed = true;
      this.contextMenu.x = event.clientX;
      this.contextMenu.y = event.clientY;
      this.contextMenu.testModule = testModule;
    },
    selectAllModuleTests() {
      console.log(this.contextMenu.testModule);
      console.log(this.selectedTests);
      for (let test of this.contextMenu.testModule.tests) {
        if (!this.selectedTests.includes(test.fullname)) {
          this.selectedTests.push(test.fullname);
        }
      }
    },
  },
};
</script>
