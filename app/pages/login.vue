<template>
  <div class="loginPage">
    <el-form ref="form" :model="form" label-width="10vh">
      <el-form-item>
        <el-input v-model="form.email" placeholder="Email"></el-input>
      </el-form-item>
      <el-form-item>
        <el-input
          v-model="form.password"
          type="password"
          placeholder="Password"
        ></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">Login</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data: () => {
    return {
      form: {
        mail: "",
        password: ""
      }
    };
  },
  methods: {
    onSubmit() {
      const bodyFormData = new FormData();

      bodyFormData.set("email", this.form.email);
      bodyFormData.set("password", this.form.password);
      this.$axios({
        method: "post",
        url: "login",
        data: bodyFormData,
        config: { headers: { "Content-Type": "multipart/form-data" } }
      })
        .then(async response => {
          if (response) {
            this.$message({
              showClose: true,
              message: response.data.message,
              type: "success"
            });
            await this.$store.dispatch("auth/login", {
              token: response.data.data.accessToken,
              userMail: this.form.email
            });
            this.$router.push("/home");
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
    }
  }
};
</script>

<style scoped>
.loginPage {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.el-form {
  width: 50vh;
  margin-top: 10vh;
}
</style>
