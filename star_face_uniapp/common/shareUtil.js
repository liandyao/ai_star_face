var shareUtil = {
  handleShareBonus: function($app, shareId, delay) {
    console.log('分享人shareID：', shareId);
    if (!shareId || !$app) return;
    var waitTime = delay || 2000;
    setTimeout(function() {
        console.log('分享加分等待时间：', waitTime);
      var url = $app.apiPath.common.shareUser + "?shareUserId=" + shareId;
      $app.post(url).then(function(res) {
        if (res.code == 200) {
          console.log('分享加分成功');
        }
      }, function(err) {
        console.error('分享加分失败', err);
      });
    }, waitTime);
  },

  getShareConfig: function(title, path) {
    var shareId = uni.getStorageSync("mySelfShareId") || '';
    var separator = path.indexOf('?') > -1 ? '&' : '?';
    return {
      title: title,
      path: path + separator + 'shareId=' + shareId
    };
  },

  getTimelineConfig: function(title) {
    var shareId = uni.getStorageSync("mySelfShareId") || '';
    return {
      title: title,
      query: 'shareId=' + shareId
    };
  }
};

module.exports = shareUtil;
