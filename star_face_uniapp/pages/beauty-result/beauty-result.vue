<template>
  <view class="container">
    <view class="result-header">
      <text class="result-emoji">{{ analysis.emoji }}</text>
      <text class="result-level">{{ analysis.level }}</text>
    </view>

    <view class="score-circle-wrap">
      <view class="score-circle" :style="{ background: scoreGradient }">
        <text class="score-number">{{ scoreInt }}</text>
        <text class="score-label">颜值分</text>
      </view>
    </view>

    <view class="photo-card">
      <image v-if="photoUrl" class="photo-img" :src="photoUrl" mode="aspectFill"></image>
    </view>

    <view class="analysis-card">
      <text class="analysis-text">{{ analysis.text }}</text>
    </view>

    <view class="share-section">
      <button class="share-btn" open-type="share">
        <text class="share-btn-text">📤 分享给好友</text>
      </button>
    </view>

    <view class="other-plays">
      <view class="other-plays-header">
        <view class="other-plays-line"></view>
        <text class="other-plays-title">其他玩法</text>
        <view class="other-plays-line"></view>
      </view>
      <view class="other-plays-list">
        <view class="other-plays-item" @click="goStarFace">
          <view class="other-plays-icon star-bg"><text class="other-plays-emoji">🌟</text></view>
          <view class="other-plays-info">
            <text class="other-plays-name">明星脸比对</text>
            <text class="other-plays-desc">看看你和哪位明星最像</text>
          </view>
          <text class="other-plays-arrow">›</text>
        </view>
        <view class="other-plays-divider"></view>
        <view class="other-plays-item" @click="goCouple">
          <view class="other-plays-icon couple-bg"><text class="other-plays-emoji">💑</text></view>
          <view class="other-plays-info">
            <text class="other-plays-name">夫妻相/闺蜜相</text>
            <text class="other-plays-desc">测测你们的缘分指数</text>
          </view>
          <text class="other-plays-arrow">›</text>
        </view>
        <view class="other-plays-divider"></view>
        <view class="other-plays-item" @click="goCrossGender">
          <view class="other-plays-icon cross-bg"><text class="other-plays-emoji">🌈</text></view>
          <view class="other-plays-info">
            <text class="other-plays-name">跨性别撞脸</text>
            <text class="other-plays-desc">看看异性明星中谁最像你</text>
          </view>
          <text class="other-plays-arrow">›</text>
        </view>
        <view class="other-plays-divider"></view>
        <view class="other-plays-item" @click="goBeautyPk">
          <view class="other-plays-icon pk-bg"><text class="other-plays-emoji">⚔️</text></view>
          <view class="other-plays-info">
            <text class="other-plays-name">颜值PK</text>
            <text class="other-plays-desc">和好友比比谁的颜值更高</text>
          </view>
          <text class="other-plays-arrow">›</text>
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
      analysis: { level: '', emoji: '', text: '' },
      photoUrl: ''
    }
  },

  computed: {
    scoreGradient() {
      var s = this.scoreInt;
      if (s >= 88) return 'linear-gradient(135deg, #ff5e3a, #ff2d55)';
      if (s >= 72) return 'linear-gradient(135deg, #ff9500, #ff5e3a)';
      if (s >= 58) return 'linear-gradient(135deg, #ffb340, #ff9500)';
      if (s >= 40) return 'linear-gradient(135deg, #ffc940, #ffb340)';
      return 'linear-gradient(135deg, #c8c8c8, #a0a0a0)';
    }
  },

  onLoad() {
    try {
      var result = uni.getStorageSync('beautyResult') || {};
      this.scoreInt = result.scoreInt || 0;
      this.analysis = result.analysis || { level: '未知', emoji: '❓', text: '鉴定结果异常' };
      this.photoUrl = uni.getStorageSync('beautyPhotoUrl') || '';
    } catch (e) {}
  },

  onShareAppMessage() {
    return shareUtil.getShareConfig('我的颜值鉴定结果：' + this.analysis.level + ' ' + this.scoreInt + '分！', '/pages/beauty/beauty');
  },

  onShareTimeline() {
    return shareUtil.getTimelineConfig('我的颜值鉴定结果：' + this.analysis.level + ' ' + this.scoreInt + '分！');
  },

  methods: {
    goStarFace() { uni.switchTab({ url: '/pages/index/index' }); },
    goCouple() { uni.switchTab({ url: '/pages/couple/couple' }); },
    goCrossGender() { uni.navigateTo({ url: '/pages/cross-gender/cross-gender' }); },
    goBeautyPk() { uni.switchTab({ url: '/pages/beauty-pk/beauty-pk' }); }
  }
}
</script>

<style scoped>
.container {
  display: flex; flex-direction: column; align-items: center;
  padding: 40rpx 30rpx; min-height: 100vh; box-sizing: border-box;
  background: linear-gradient(180deg, #fff8e1 0%, #fff3e0 40%, #fafafa 100%);
}
.result-header { display: flex; flex-direction: column; align-items: center; margin-bottom: 30rpx; }
.result-emoji { font-size: 80rpx; margin-bottom: 10rpx; }
.result-level { font-size: 40rpx; font-weight: 800; color: #ff9500; }

.score-circle-wrap { margin-bottom: 30rpx; }
.score-circle {
  width: 220rpx; height: 220rpx; border-radius: 50%;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  box-shadow: 0 8rpx 32rpx rgba(255, 149, 0, 0.3);
}
.score-number { font-size: 72rpx; font-weight: 800; color: #fff; line-height: 1; }
.score-label { font-size: 22rpx; color: rgba(255,255,255,0.8); margin-top: 4rpx; }

.photo-card {
  width: 240rpx; height: 240rpx; border-radius: 50%; overflow: hidden;
  border: 6rpx solid #ff9500; margin-bottom: 30rpx;
  box-shadow: 0 8rpx 24rpx rgba(255, 149, 0, 0.2);
}
.photo-img { width: 100%; height: 100%; }

.analysis-card {
  width: 600rpx; background: #fff; border-radius: 24rpx; padding: 30rpx;
  margin-bottom: 30rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.06);
}
.analysis-text { font-size: 28rpx; color: #666; line-height: 1.6; text-align: center; }

.share-section { margin-bottom: 40rpx; }
.share-btn {
  width: 400rpx; height: 80rpx;
  background: linear-gradient(135deg, #ff9500, #ff5e3a);
  color: #fff; font-size: 28rpx; font-weight: 700; border-radius: 40rpx; border: none;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 6rpx 24rpx rgba(255, 149, 0, 0.3);
}
.share-btn-text { color: #fff; }

.other-plays { width: 100%; }
.other-plays-header { display: flex; align-items: center; gap: 20rpx; margin-bottom: 20rpx; }
.other-plays-line { flex: 1; height: 1rpx; background: #e0e0e0; }
.other-plays-title { font-size: 26rpx; color: #999; }
.other-plays-list { background: #fff; border-radius: 24rpx; overflow: hidden; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.06); }
.other-plays-item { display: flex; align-items: center; padding: 24rpx 28rpx; }
.other-plays-icon { width: 64rpx; height: 64rpx; border-radius: 16rpx; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.other-plays-emoji { font-size: 32rpx; }
.star-bg { background: #fff0f5; }
.couple-bg { background: #f5eaff; }
.cross-bg { background: #eef0ff; }
.pk-bg { background: #fff3e0; }
.other-plays-info { flex: 1; margin-left: 16rpx; display: flex; flex-direction: column; gap: 4rpx; }
.other-plays-name { font-size: 28rpx; font-weight: 700; color: #333; }
.other-plays-desc { font-size: 22rpx; color: #999; }
.other-plays-arrow { font-size: 36rpx; color: #ccc; margin-left: 10rpx; }
.other-plays-divider { height: 1rpx; background: #f0f0f0; margin: 0 28rpx; }
</style>
