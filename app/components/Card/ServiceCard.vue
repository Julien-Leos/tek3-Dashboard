<template>
  <div
    class="card"
    :style="'background: #' + backgroundColor"
    @mouseover="isOvered = true"
    @mouseleave="isOvered = false"
  >
    <el-button
      v-show="isOvered"
      class="actionBtn"
      type="primary"
      plain
      rounded
      @click="actionBtn"
      >{{ isConnected ? "Disconnect" : "Connect" }}</el-button
    >
    <span
      class="cardName"
      :style="'color: #' + nameColor + ';opacity: ' + (isOvered ? 0.4 : 1)"
    >
      {{ service.name | serviceName }}
    </span>
    <img
      class="cardImage"
      :src="'/' + service.name + '.png'"
      :style="'opacity: ' + (isOvered ? 0.4 : 1)"
    />
  </div>
</template>

<script>
export default {
  name: "ServiceCard",
  filters: {
    serviceName: value => {
      return value
        .replace(/_/gi, " ")
        .split(" ")
        .map(element => element[0].toUpperCase() + element.slice(1))
        .join(" ");
    }
  },
  props: {
    service: {
      type: Object,
      default: () => {}
    },
    isConnected: {
      type: Boolean,
      default: false
    }
  },
  data: () => {
    return {
      backgroundColor: "#FFFFFF",
      nameColor: "#000000",
      isOvered: false
    };
  },
  mounted() {
    this.backgroundColor = this.$brighterColor(this.service.color, 65);
    this.nameColor = this.$idealTextColor(this.service.color);
  },
  methods: {
    actionBtn() {
      if (this.isConnected) {
        this.$emit("onAction", [false, this.service]);
      } else if (this.service.isOauth) {
        this.getOauthCallback();
      } else {
        this.$emit("onAction", [true, this.service]);
      }
    },
    getOauthCallback() {
      this.$axios.get(this.service.name + "/oauth").then(response => {
        window.open(response.data, "_self");
      });
    }
  }
};
</script>

<style scoped>
.card {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
  width: 25vh;
  height: 25vh;
  border-radius: 0.3em;
  margin: 1.3vh;
}

.cardName {
  display: block;
  margin: 1.5vh 0.5vh;
  font-size: 1.4em;
  font-weight: bold;
}

.cardImage {
  width: 40%;
  flex-shrink: 0;
}

.actionBtn {
  position: absolute;
  z-index: 1;
}
</style>
