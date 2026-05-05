<script>
import request from './request/request.js'

export default {
  globalData: {
    loginPromise: null
  },
  onLaunch() {
    console.log('App Launch')
    // 全局登录，保存 Promise 供页面使用
    this.globalData.loginPromise = request.miniAppLogin()
  },
  onShow() {
    console.log('App Show')
  },
  onHide() {
    console.log('App Hide')
  }
}
</script>

<style>
page {
  background-color: #fff0f5;
  min-height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
</style>
