<template>
  <div>
    <b-row>
      <b-col sm="12" md="4" offset-md="4">
        <b-card title="登录">
          <b-form @submit="onSubmit">
            <b-alert :show="errors.length>0" variant="danger">
              <ul class="pl-2">
                <li class="small" v-for="(error, index) in errors" :key="index">{{ error.detail }}</li>
              </ul>
            </b-alert>
            <b-form-group
                label="用户名:"
                label-for="id_username"
            >
              <b-form-input
                  id="id_username"
                  v-model="form.username"
                  type="text"
                  required
              ></b-form-input>
            </b-form-group>
            <b-form-group label="密码:" label-for="id_password">
              <b-form-input
                  id="id_password"
                  v-model="form.password"
                  type="password"
                  required
              ></b-form-input>
            </b-form-group>
            <b-button type="submit" block variant="primary" :disabled="formProcessing">登录</b-button>
          </b-form>
        </b-card>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import {postAuthLogin} from "@/api";
import storage from "../utils"
import {Formatter} from "sarala-json-api-data-formatter";

export default {
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
      errors: [],
      formProcessing: false,
      formatter: new Formatter()
    }
  },
  methods: {
    async login(username, password) {
      const type = "tokens"
      const data = this.formatter.serialize({type, username, password})
      return await postAuthLogin(data)
    },

    async onSubmit(event) {
      this.formProcessing = true
      event.preventDefault()
      try {
        const loginRes = await this.login(this.form.username, this.form.password)
        const result = this.formatter.deserialize(loginRes.data)

        const authToken = result["auth_token"]
        this.$store.commit("SET_AUTH_TOKEN", authToken)
        storage.saveAuthToken(authToken)

        const userData = result.user.data
        const user = {
          userId: userData.id,
          username: userData.username,
          nickname: userData.nickname
        }
        this.$store.commit("SET_USER", user)
        storage.saveUser(user)

        this.formProcessing = false

        await this.$router.push({name: 'robot-list'})
      } catch (error) {
        if (error.response) {
          if (error.response.status >= 500) {
            this.$bvToast.toast('服务端错误', {
              title: '登录失败',
              autoHideDelay: 3000,
              toaster: 'b-toaster-top-center',
              variant: 'danger',
              appendToast: false
            });
          } else if (error.response.status >= 400) {
            // form validation error
            this.errors = error.response.data.errors
          }
        } else {
          this.$bvToast.toast(error.message, {
            title: '登录失败',
            autoHideDelay: 3000,
            toaster: 'b-toaster-top-center',
            variant: 'danger',
            appendToast: false
          });
        }
        this.$store.commit("REMOVE_AUTH_TOKEN")
        this.$store.commit("REMOVE_USER")
        storage.clear()
        this.formProcessing = false
      }
    }
  }
}
</script>

