<template>
  <view class="container">
    <view class="result-header">
      <text class="result-emoji">{{ pkAnalysis.emoji }}</text>
      <text class="result-level">{{ pkAnalysis.level }}</text>
    </view>

    <view class="pk-area">
      <view class="pk-card" :class="{ 'winner': winner === 'A' }">
        <view v-if="winner === 'A'" class="crown-badge"><text class="crown-text">👑</text></view>
        <image v-if="photoA" class="pk-photo" :src="photoA" mode="aspectFill"></image>
        <view class="pk-score-wrap">
          <text class="pk-score">{{ scoreIntA }}</text>
          <text class="pk-score-label">颜值分</text>
        </view>
        <text class="pk-level">{{ analysisA.level }}</text>
      </view>

      <view class="pk-vs">
        <view class="pk-vs-line"></view>
        <view class="pk-vs-circle">
          <text class="pk-vs-text">VS</text>
        </view>
        <view class="pk-vs-line"></view>
      </view>

      <view class="pk-card" :class="{ 'winner': winner === 'B' }">
        <view v-if="winner === 'B'" class="crown-badge"><text class="crown-text">👑</text></view>
        <image v-if="photoB" class="pk-photo" :src="photoB" mode="aspectFill"></image>
        <view class="pk-score-wrap">
          <text class="pk-score">{{ scoreIntB }}</text>
          <text class="pk-score-label">颜值分</text>
        </view>
        <text class="pk-level">{{ analysisB.level }}</text>
      </view>
    </view>

    <view class="analysis-card">
      <text class="analysis-text">{{ pkAnalysis.text }}</text>
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
        <view class="other-plays-item" @click="goBeauty">
          <view class="other-plays-icon beauty-bg"><text class="other-plays-emoji">🔥</text></view>
          <view class="other-plays-info">
            <text class="other-plays-name">颜值暴击</text>
            <text class="other-plays-desc">AI鉴定你的颜值等级</text>
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
      scoreIntA: 0, scoreIntB: 0,
      analysisA: { level: '', emoji: '', text: '' },
      analysisB: { level: '', emoji: '', text: '' },
      pkAnalysis: { level: '', emoji: '', text: '', diff: 0, winner: 'A' },
      winner: 'A',
      photoA: '', photoB: ''
    }
  },

  onLoad() {
    try {
      var result = uni.getStorageSync('beautyPkResult') || {};
      this.scoreIntA = result.scoreIntA || 0;
      this.scoreIntB = result.scoreIntB || 0;
      this.analysisA = result.analysisA || { level: '未知', emoji: '❓', text: '' };
      this.analysisB = result.analysisB || { level: '未知', emoji: '❓', text: '' };
      this.pkAnalysis = result.pkAnalysis || { level: '未知', emoji: '❓', text: '', diff: 0, winner: 'A' };
      this.winner = this.pkAnalysis.winner || 'A';
      this.photoA = uni.getStorageSync('beautyPkPhotoA') || '';
      this.photoB = uni.getStorageSync('beautyPkPhotoB') || '';
    } catch (e) {}
  },

  onShareAppMessage() {
    var winSide = this.winner === 'A' ? '左' : '右';
    return shareUtil.getShareConfig('颜值PK结果：' + winSide + '方以' + this.pkAnalysis.diff + '分优势胜出！', '/pages/beauty-pk/beauty-pk');
  },

  onShareTimeline() {
    var winSide = this.winner === 'A' ? '左' : '右';
    return shareUtil.getTimelineConfig('颜值PK结果：' + winSide + '方以' + this.pkAnalysis.diff + '分优势胜出！');
  },

  methods: {
    goStarFace() { uni.switchTab({ url: '/pages/index/index' }); },
    goCouple() { uni.switchTab({ url: '/pages/couple/couple' }); },
    goCrossGender() { uni.navigateTo({ url: '/pages/cross-gender/cross-gender' }); },
    goBeauty() { uni.navigateTo({ url: '/pages/beauty/beauty' }); }
  }
}
</script>

<style scoped>
.container {
  display: flex; flex-direction: column; align-items: center;
  padding: 40rpx 30rpx; min-height: 100vh; box-sizing: border-box;
  background: linear-gradient(180deg, #ffebee 0%, #fce4ec 40%, #fafafa 100%);
}
.result-header { display: flex; flex-direction: column; align-items: center; margin-bottom: 30rpx; }
.result-emoji { font-size: 80rpx; margin-bottom: 10rpx; }
.result-level { font-size: 40rpx; font-weight: 800; color: #ff4757; }

.pk-area { display: flex; align-items: center; gap: 16rpx; margin-bottom: 30rpx; }
.pk-card {
  width: 260rpx; background: #fff; border-radius: 24rpx; padding: 24rpx;
  display: flex; flex-direction: column; align-items: center; gap: 12rpx;
  box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.06); position: relative;
}
.pk-card.winner { border: 3rpx solid #ff4757; box-shadow: 0 8rpx 32rpx rgba(255, 71, 87, 0.2); }
.crown-badge { position: absolute; top: -20rpx; left: 50%; transform: translateX(-50%); }
.crown-text { font-size: 40rpx; }
.pk-photo { width: 160rpx; height: 160rpx; border-radius: 50%; }
.pk-score-wrap { display: flex; flex-direction: column; align-items: center; }
.pk-score { font-size: 56rpx; font-weight: 800; color: #ff4757; line-height: 1; }
.pk-score-label { font-size: 20rpx; color: #999; margin-top: 4rpx; }
.pk-level { font-size: 24rpx; font-weight: 700; color: #ff9500; }

.pk-vs { display: flex; flex-direction: column; align-items: center; gap: 8rpx; }
.pk-vs-line { width: 4rpx; height: 60rpx; background: linear-gradient(180deg, transparent, #ff4757, transparent); border-radius: 2rpx; }
.pk-vs-circle {
  width: 56rpx; height: 56rpx;
  background: linear-gradient(135deg, #ff4757, #ff6b81);
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
}
.pk-vs-text { font-size: 22rpx; font-weight: 800; color: #fff; }

.analysis-card {
  width: 600rpx; background: #fff; border-radius: 24rpx; padding: 30rpx;
  margin-bottom: 30rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.06);
}
.analysis-text { font-size: 28rpx; color: #666; line-height: 1.6; text-align: center; }

.share-section { margin-bottom: 40rpx; }
.share-btn {
  width: 400rpx; height: 80rpx;
  background: linear-gradient(135deg, #ff4757, #ff6b81);
  color: #fff; font-size: 28rpx; font-weight: 700; border-radius: 40rpx; border: none;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 6rpx 24rpx rgba(255, 71, 87, 0.3);
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
.beauty-bg { background: #fff3e0; }
.other-plays-info { flex: 1; margin-left: 16rpx; display: flex; flex-direction: column; gap: 4rpx; }
.other-plays-name { font-size: 28rpx; font-weight: 700; color: #333; }
.other-plays-desc { font-size: 22rpx; color: #999; }
.other-plays-arrow { font-size: 36rpx; color: #ccc; margin-left: 10rpx; }
.other-plays-divider { height: 1rpx; background: #f0f0f0; margin: 0 28rpx; }
</style>
