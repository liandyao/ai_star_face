import Vue from 'vue'
import App from './App'
import request from './request/request.js'

Vue.config.productionTip = false

Vue.prototype.$app = request

App.mpType = 'app'

const app = new Vue({
  ...App
})
app.$mount()
