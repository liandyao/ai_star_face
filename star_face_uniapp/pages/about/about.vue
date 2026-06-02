<template>
  <view class="about-page">
    <view class="about-header">
      <text class="about-logo">🌟</text>
      <text class="about-title">明星脸比对</text>
      <text class="about-version">v1.2.1</text>
    </view>

    <view class="section">
      <view class="section-header">
        <text class="section-icon">💎</text>
        <text class="section-title">积分规则</text>
      </view>
      <view class="rule-card">
        <view class="rule-item">
          <view class="rule-left">
            <text class="rule-num">1</text>
          </view>
          <view class="rule-right">
            <text class="rule-name">分享给好友</text>
            <text class="rule-desc">分享小程序给好友，好友第一次打开后双方各得5积分</text>
          </view>
          <view class="rule-score">
            <text class="rule-score-text">+5</text>
          </view>
        </view>
        <view class="rule-divider"></view>
        <view class="rule-item">
          <view class="rule-left">
            <text class="rule-num">2</text>
          </view>
          <view class="rule-right">
            <text class="rule-name">观看视频广告</text>
            <text class="rule-desc">观看一段短视频广告即可获得5积分</text>
          </view>
          <view class="rule-score">
            <text class="rule-score-text">+5</text>
          </view>
        </view>
        <view class="rule-divider"></view>
         
      </view>
    </view>

    <view class="section">
      <view class="section-header">
        <text class="section-icon">🎮</text>
        <text class="section-title">玩法介绍</text>
      </view>
      <view class="play-card">
        <view class="play-item">
          <view class="play-icon-wrap star-bg">
            <text class="play-icon">🌟</text>
          </view>
          <view class="play-info">
            <text class="play-name">明星脸比对</text>
            <text class="play-desc">上传正脸照，AI帮你找出最像的明星，消耗5积分</text>
          </view>
        </view>
        <view class="play-item">
          <view class="play-icon-wrap couple-bg">
            <text class="play-icon">💑</text>
          </view>
          <view class="play-info">
            <text class="play-name">夫妻相/闺蜜相</text>
            <text class="play-desc">上传双人照，测测你们的缘分指数，消耗5积分</text>
          </view>
        </view>
        <view class="play-item">
          <view class="play-icon-wrap cross-bg">
            <text class="play-icon">🌈</text>
          </view>
          <view class="play-info">
            <text class="play-name">跨性别撞脸</text>
            <text class="play-desc">看看异性明星中谁最像你，消耗5积分，找不到不扣分</text>
          </view>
        </view>
      </view>
    </view>

    <view class="section">
      <view class="section-header">
        <text class="section-icon">📋</text>
        <text class="section-title">温馨提示</text>
      </view>
      <view class="tips-card">
        <text class="tips-item">• 请上传正面清晰的人脸照片，效果更佳</text>
        <text class="tips-item">• 光线均匀、素颜拍摄识别更准确</text>
        <text class="tips-item">• 比对结果仅供娱乐，请勿当真</text>
        <text class="tips-item">• 人脸数据仅用于本次比对，不做他用</text>
        <text class="tips-item">• 如有问题或建议，欢迎反馈vx：cnit6688</text>
      </view>
    </view>

    <view class="about-footer">
      <text class="footer-text">明星脸比对 · 发现你的明星脸</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {}
  }
}
</script>

<style scoped>
.about-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #fff0f5 0%, #f8f0ff 50%, #f0f5ff 100%);
  padding: 30rpx;
  padding-bottom: 60rpx;
}

.about-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40rpx 0 30rpx;
}

.about-logo { font-size: 80rpx; }
.about-title { font-size: 40rpx; font-weight: 700; color: #333; margin-top: 16rpx; }
.about-version { font-size: 24rpx; color: #999; margin-top: 8rpx; }

.section { margin-top: 30rpx; }

.section-header {
  display: flex;
  align-items: center;
  gap: 10rpx;
  margin-bottom: 20rpx;
  padding-left: 10rpx;
}

.section-icon { font-size: 32rpx; }
.section-title { font-size: 30rpx; font-weight: 700; color: #333; }

.rule-card {
  background: #fff;
  border-radius: 24rpx;
  padding: 10rpx 28rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.05);
}

.rule-item {
  display: flex;
  align-items: center;
  padding: 24rpx 0;
}

.rule-left { flex-shrink: 0; }

.rule-num {
   
  color: #c471ed;
  font-size: 24rpx;
  font-weight: 700;
  border-radius: 50%;
}

.rule-right {
  flex: 1;
  margin-left: 20rpx;
  display: flex;
  flex-direction: column;
  gap: 6rpx;
}

.rule-name { font-size: 28rpx; font-weight: 700; color: #333; }
.rule-desc { font-size: 22rpx; color: #999; line-height: 1.5; }

.rule-score { flex-shrink: 0; margin-left: 16rpx; }

.rule-score-text {
  font-size: 28rpx;
  font-weight: 700;
  color: #ff6b9d;
}

.rule-divider {
  height: 1rpx;
  background: #f5f5f5;
}

.play-card {
  background: #fff;
  border-radius: 24rpx;
  padding: 16rpx 28rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.play-item {
  display: flex;
  align-items: center;
}

.play-icon-wrap {
  width: 72rpx;
  height: 72rpx;
  border-radius: 18rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.star-bg { background: linear-gradient(135deg, #ff94d5 0%, #ff7ce3 100%); }
.couple-bg { background: linear-gradient(135deg, #ffe0f0 0%, #e8d0ff 100%); }
.cross-bg { background: linear-gradient(135deg, #e0e8ff 0%, #d0d8ff 100%); }

.play-icon { font-size: 36rpx; }

.play-info {
  flex: 1;
  margin-left: 20rpx;
  display: flex;
  flex-direction: column;
  gap: 6rpx;
}

.play-name { font-size: 28rpx; font-weight: 700; color: #333; }
.play-desc { font-size: 22rpx; color: #999; line-height: 1.5; }

.tips-card {
  background: #fff;
  border-radius: 24rpx;
  padding: 28rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.tips-item {
  font-size: 24rpx;
  color: #666;
  line-height: 1.6;
}

.about-footer {
  margin-top: 50rpx;
  display: flex;
  justify-content: center;
}

.footer-text { font-size: 22rpx; color: #bbb; }
</style>
