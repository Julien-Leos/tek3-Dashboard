<template>
  <div>
    <el-container class="bg-gray-light">
      <el-header height="5vh">Activated Widgets</el-header>
      <el-main class="widgetCard bg-gray">
        <span v-if="activatedWidgets.length === 0"
          >There are no widgets configured</span
        >
        <WidgetCard
          v-for="widget in activatedWidgets"
          v-else
          :key="widget.id"
          :widget="widget"
          :is-connected="true"
          @onConnect="getActivatedServices"
        />
      </el-main>
    </el-container>
    <el-container class="bg-gray-light">
      <el-header height="5vh">Available Widgets</el-header>
      <el-main class="widgetCard bg-gray">
        <span v-if="availableWidgets.length === 0"
          >There are no more widgets to configure</span
        >
        <WidgetCard
          v-for="widget in availableWidgets"
          v-else
          :key="widget.id"
          :widget="widget"
          :is-connected="false"
          @onConnect="getActivatedServices"
        />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import WidgetCard from "../components/Card/WidgetCard";

export default {
  middleware: "auth",
  components: {
    WidgetCard
  },
  data: () => {
    return {
      services: {},
      activatedServices: [],
      availableWidgets: [],
      activatedWidgets: []
    };
  },
  async mounted() {
    await this.$axios
      .get("services")
      .then(response => {
        if (response) {
          this.services = response.data.data.services;
        }
      })
      .catch(error => {
        if (error.response) {
          this.$message({
            showClose: true,
            message: error.response.data.message,
            type: "error"
          });
        }
      });
    this.getActivatedServices();
  },
  methods: {
    async getActivatedServices() {
      await this.$axios
        .get("users/" + this.$store.state.auth.userId + "/services")
        .then(response => {
          if (response) {
            this.activatedServices = response.data.data.services;
            this.activatedWidgets = [];
            this.availableWidgets = [];
            this.getActivatedWidgets();
          }
        })
        .catch(error => {
          if (error.response) {
            this.$message({
              showClose: true,
              message: error.response.data.message,
              type: "error"
            });
          }
        });
    },
    getActivatedWidgets() {
      Object.entries(this.activatedServices).forEach(activatedService => {
        const service = this.services.find(
          service => service.name === activatedService[1].name
        );
        service.widgets.forEach(widget => {
          const activatedWidget = Object.entries(
            activatedService[1].widgets
          ).find(
            dbActivatedWidget => dbActivatedWidget[1].name === widget.name
          );
          widget.color = service.color;
          widget.serviceName = service.name;
          widget.serviceId = activatedService[0];
          if (activatedWidget) {
            widget.id = activatedWidget[0];
            widget.timer = activatedWidget[1].timer;
            widget.paramsData = Object(JSON.parse(activatedWidget[1].params));
            this.activatedWidgets.push(widget);
          } else this.availableWidgets.push(widget);
        });
      });
    }
  }
};
</script>

<style scoped>
.el-container {
  border-radius: 1em;
  margin-bottom: 3vh;
}

.el-header {
  margin: 1vh 3vh;
  font-size: 1.5em;
}

.el-main {
  margin: 0 1.5vh 1.5vh 1.5vh;
  border-radius: 0.5em;
}

.widgetCard {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: space-evenly;
}

.el-main {
  text-align: center;
}
</style>
