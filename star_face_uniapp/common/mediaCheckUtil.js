/**
 * 图片内容安全检测工具（通用）
 * 调用后端 /school_api/media/check 同步检测图片内容
 * 无需配置微信消息推送，直接返回检测结果
 */
var mediaCheckUtil = {
  /**
   * 获取当前小程序 appId（通用，微信/抖音均可）
   */
  getAppId: function() {
    try {
      var info = uni.getAccountInfoSync();
      return info.miniProgram.appId || '';
    } catch (e) {
      return '';
    }
  },

  /**
   * 检测图片内容安全（同步）
   * @param {string} mediaUrl 图片公网URL
   * @param {object} $app request.js 导出的实例
   * @returns {Promise} 通过->resolve, 违规->reject
   */
  check: function(mediaUrl, $app) {
    var that = this;
    var openid = uni.getStorageSync('openid');
    if (!openid) {
      return Promise.reject(new Error('请先登录'));
    }
    return $app.post($app.apiPath.media.check, {
      appid: that.getAppId(),
      media_url: mediaUrl
    }).then(function(res) {
      if (res.code == 200 && res.data) {
        if (res.data.status === 'pass') {
          return;
        }
        if (res.data.status === 'risky') {
          throw new Error('图片内容违规，请更换照片');
        }
      }
      throw new Error(res.msg || '图片审核失败，请重试');
    });
  }
};

module.exports = mediaCheckUtil;
