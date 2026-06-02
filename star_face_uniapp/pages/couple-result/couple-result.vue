<template>
  <view class="container">
    <view class="header">
      <text class="header-title">✨ 缘分比对结果</text>
    </view>

    <view class="compare-card">
      <view class="compare-content">
        <view class="compare-item">
          <image v-if="photoA" class="compare-photo" :src="photoA" mode="aspectFill" />
          <view v-else class="compare-photo-placeholder">
            <text class="placeholder-text">你</text>
          </view>
        </view>
        <view class="heart-divider">
          <text class="heart-icon">💕</text>
        </view>
        <view class="compare-item">
          <image v-if="photoB" class="compare-photo" :src="photoB" mode="aspectFill" />
          <view v-else class="compare-photo-placeholder">
            <text class="placeholder-text">TA</text>
          </view>
        </view>
      </view>
    </view>

    <view class="score-card" v-if="analysis">
      <view class="score-ring-wrap">
        <view class="score-ring">
          <text class="score-emoji">{{ analysis.emoji }}</text>
        </view>
        <view class="score-number-wrap">
          <text class="score-number">{{ scoreInt }}</text>
          <text class="score-unit">分</text>
        </view>
      </view>

      <view class="level-badge">
        <text class="level-text">{{ analysis.level }}</text>
      </view>

      <view class="score-bar-wrap">
        <view class="score-bar-bg">
          <view class="score-bar-fill" :style="{ width: scoreInt + '%' }"></view>
        </view>
        <view class="score-labels">
          <text class="score-label">夫妻相指数</text>
          <text class="score-percent">{{ scoreInt }}%</text>
        </view>
      </view>

      <view class="analysis-text-wrap">
        <text class="analysis-text">{{ analysis.text }}</text>
      </view>
    </view>

    <view class="no-result" v-if="!analysis">
      <text class="no-result-text">暂无比对结果</text>
    </view>

    <view class="actions">
      <button class="share-btn" open-type="share">
        <text class="share-icon">📤</text>
        <text class="share-text">分享结果</text>
      </button>
      <button class="re-test-btn" @tap="reTest">
        <text class="retest-icon">🔄</text>
        <text class="retest-text">再测一次</text>
      </button>
      <button class="home-btn" @tap="goHome">
        <text class="home-icon">🏠</text>
        <text class="home-text">返回首页</text>
      </button>
    </view>

    <view class="more-features">
      <view class="more-features-title">
        <view class="more-features-line"></view>
        <text class="more-features-text">其他玩法</text>
        <view class="more-features-line"></view>
      </view>
      <view class="more-features-list">
        <view class="more-feature-item" @click="goStarFace">
          <view class="more-feature-icon star-bg">
            <text class="more-feature-emoji">🌟</text>
          </view>
          <view class="more-feature-info">
            <text class="more-feature-name">明星脸比对</text>
            <text class="more-feature-desc">看看你和哪位明星最像</text>
          </view>
          <text class="more-feature-arrow">›</text>
        </view>
        <view class="more-feature-item" @click="goCrossGender">
          <view class="more-feature-icon cross-bg">
            <text class="more-feature-emoji">🌈</text>
          </view>
          <view class="more-feature-info">
            <text class="more-feature-name">跨性别撞脸</text>
            <text class="more-feature-desc">看看异性明星中谁最像你</text>
          </view>
          <text class="more-feature-arrow">›</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import shareUtil from '@/common/shareUtil.js';
export default {
  data() {
    return {
      scoreInt: 0,
      analysis: null,
      photoA: '',
      photoB: ''
    }
  },

  onLoad(op) {
    var shareId = op ? op.shareId : '';
    this.loadResults();
    shareUtil.handleShareBonus(this.$app, shareId);
  },

  onShareAppMessage() {
    var level = this.analysis ? this.analysis.level : '夫妻相';
    var score = this.scoreInt || 0;
    var config = shareUtil.getShareConfig('我们的夫妻相指数' + score + '分，「' + level + '」！快来测测你们的缘分~', '/pages/couple/couple');
    if (this.photoA) {
      config.imageUrl = this.photoA;
    }
    return config;
  },

  onShareTimeline() {
    var level = this.analysis ? this.analysis.level : '夫妻相';
    var score = this.scoreInt || 0;
    var config = shareUtil.getTimelineConfig('我们的夫妻相指数' + score + '分，「' + level + '」！快来测测你们的缘分~');
    if (this.photoA) {
      config.imageUrl = this.photoA;
    }
    return config;
  },

  methods: {
    loadResults() {
      try {
        var data = uni.getStorageSync('coupleResult');
        if (data) {
          this.scoreInt = data.scoreInt || data.score || 0;
          this.analysis = data.analysis || null;
        }

        var photoA = uni.getStorageSync('couplePhotoA');
        var photoB = uni.getStorageSync('couplePhotoB');
        if (photoA) this.photoA = photoA;
        if (photoB) this.photoB = photoB;
      } catch (e) {
        console.error('读取结果失败', e);
        uni.showToast({ title: '数据加载失败', icon: 'none' });
      }
    },

    reTest() {
      uni.reLaunch({ url: '/pages/couple/couple' });
    },

    goHome() {
      uni.reLaunch({ url: '/pages/index/index' });
    },

    goStarFace() {
      uni.switchTab({ url: '/pages/index/index' });
    },

    goCrossGender() {
      uni.navigateTo({ url: '/pages/cross-gender/cross-gender' });
    }
  }
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40rpx 30rpx;
  box-sizing: border-box;
  min-height: 100vh;
  background: linear-gradient(180deg, #fff0f5 0%, #f0f0ff 40%, #fafafa 100%);
}

.header {
  margin-bottom: 30rpx;
}

.header-title {
  font-size: 44rpx;
  font-weight: 800;
  color: #c471ed;
}

.compare-card {
  width: 560rpx;
  background: #fff;
  border-radius: 40rpx;
  padding: 30rpx;
  box-shadow: 0 12rpx 40rpx rgba(196, 113, 237, 0.2);
  margin-bottom: 30rpx;
}

.compare-content {
  display: flex;
  align-items: center;
  justify-content: space-around;
}

.compare-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.compare-photo {
  width: 200rpx;
  height: 240rpx;
  border-radius: 24rpx;
  box-shadow: 0 8rpx 24rpx rgba(196, 113, 237, 0.25);
}

.compare-photo-placeholder {
  width: 200rpx;
  height: 240rpx;
  border-radius: 24rpx;
  background: linear-gradient(135deg, #ffe0f0 0%, #e8d0ff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-text {
  font-size: 48rpx;
  color: #c471ed;
  font-weight: 800;
}

.heart-divider {
  display: flex;
  align-items: center;
  justify-content: center;
}

.heart-icon {
  font-size: 48rpx;
}

.score-card {
  width: 560rpx;
  background: #fff;
  border-radius: 40rpx;
  padding: 40rpx 30rpx;
  box-shadow: 0 12rpx 40rpx rgba(196, 113, 237, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24rpx;
}

.score-ring-wrap {
  position: relative;
  width: 200rpx;
  height: 200rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.score-ring {
  width: 200rpx;
  height: 200rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, #ff6b9d 0%, #c471ed 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8rpx 32rpx rgba(196, 113, 237, 0.4);
}

.score-emoji {
  font-size: 80rpx;
}

.score-number-wrap {
  position: absolute;
  bottom: -16rpx;
  left: 50%;
  transform: translateX(-50%);
  background: #fff;
  padding: 8rpx 24rpx;
  border-radius: 36rpx;
  display: flex;
  align-items: baseline;
  box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.1);
}

.score-number {
  font-size: 40rpx;
  font-weight: 800;
  color: #c471ed;
}

.score-unit {
  font-size: 22rpx;
  color: #999;
  margin-left: 4rpx;
}

.level-badge {
  background: linear-gradient(135deg, #ff6b9d 0%, #c471ed 100%);
  padding: 12rpx 40rpx;
  border-radius: 36rpx;
  box-shadow: 0 6rpx 20rpx rgba(196, 113, 237, 0.3);
}

.level-text {
  font-size: 32rpx;
  font-weight: 800;
  color: #fff;
}

.score-bar-wrap {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.score-bar-bg {
  width: 100%;
  height: 24rpx;
  background: #f0f0f0;
  border-radius: 12rpx;
  overflow: hidden;
}

.score-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #ff6b9d, #c471ed);
  border-radius: 12rpx;
  transition: width 1s ease;
}

.score-labels {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.score-label {
  font-size: 22rpx;
  color: #999;
}

.score-percent {
  font-size: 26rpx;
  font-weight: 700;
  color: #c471ed;
}

.analysis-text-wrap {
  width: 100%;
  background: #fafafa;
  border-radius: 24rpx;
  padding: 24rpx;
}

.analysis-text {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
}

.no-result {
  width: 560rpx;
  padding: 80rpx 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.no-result-text {
  font-size: 30rpx;
  color: #999;
}

.actions {
  width: 560rpx;
  margin-top: 40rpx;
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.share-btn {
  width: 100%;
  height: 88rpx;
  background: #fff;
  color: #c471ed;
  font-size: 30rpx;
  font-weight: 700;
  border-radius: 44rpx;
  border: 3rpx solid #c471ed;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10rpx;
  box-shadow: 0 4rpx 16rpx rgba(196, 113, 237, 0.2);
}

.re-test-btn {
  width: 100%;
  height: 88rpx;
  background: linear-gradient(135deg, #ff6b9d 0%, #c471ed 100%);
  color: #fff;
  font-size: 30rpx;
  font-weight: 700;
  border-radius: 44rpx;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10rpx;
  box-shadow: 0 8rpx 24rpx rgba(196, 113, 237, 0.35);
}

.home-btn {
  width: 100%;
  height: 88rpx;
  background: #fff;
  color: #999;
  font-size: 28rpx;
  font-weight: 600;
  border-radius: 44rpx;
  border: 2rpx solid #eee;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10rpx;
}

.more-features {
  width: 560rpx;
  margin-top: 40rpx;
}

.more-features-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20rpx;
  margin-bottom: 24rpx;
}

.more-features-line {
  width: 60rpx;
  height: 4rpx;
  background: linear-gradient(90deg, transparent, #c471ed, transparent);
  border-radius: 2rpx;
}

.more-features-text {
  font-size: 28rpx;
  font-weight: 700;
  color: #666;
}

.more-features-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.more-feature-item {
  display: flex;
  align-items: center;
  padding: 24rpx 28rpx;
  background: #fff;
  border-radius: 20rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.06);
}

.more-feature-icon {
  width: 80rpx;
  height: 80rpx;
  border-radius: 20rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20rpx;
  flex-shrink: 0;
}

.star-bg {
  background: linear-gradient(135deg, #fff0f5 0%, #ffe0ea 100%);
}

.cross-bg {
  background: linear-gradient(135deg, #e0e8ff 0%, #d0d8ff 100%);
}

.more-feature-emoji { font-size: 36rpx; }

.more-feature-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6rpx;
}

.more-feature-name {
  font-size: 28rpx;
  font-weight: 700;
  color: #333;
}

.more-feature-desc {
  font-size: 22rpx;
  color: #999;
}

.more-feature-arrow {
  font-size: 36rpx;
  color: #ccc;
  font-weight: 300;
  margin-left: 10rpx;
}
</style>
