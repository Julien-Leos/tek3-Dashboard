<template>
  <div class="registerPage">
    <el-form ref="form" :model="form" label-width="10vh">
      <el-form-item label="Email">
        <el-input
          v-model="form.email"
          placeholder="Enter your email"
        ></el-input>
      </el-form-item>
      <el-form-item label="Password">
        <el-input
          v-model="form.password"
          type="password"
          placeholder="Enter a strong password"
        ></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">Create Account</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data: () => {
    return {
      form: {
        email: "",
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
        url: "register",
        data: bodyFormData,
        config: { headers: { "Content-Type": "multipart/form-data" } }
      })
        .then(response => {
          if (response) {
            this.$message({
              showClose: true,
              message: response.data.message,
              type: "success"
            });
            this.$router.push("/login");
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
.registerPage {
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
