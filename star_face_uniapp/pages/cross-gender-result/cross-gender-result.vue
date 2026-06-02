<template>
  <view class="container">
    <view class="header">
      <text class="header-title">✨ 跨性别撞脸结果</text>
      <text class="header-subtitle">{{ subtitleText }}</text>
    </view>

    <view class="compare-card">
      <view class="compare-title">👇 你与明星对比</view>
      <view class="compare-content">
        <view class="compare-item">
          <view class="compare-label">你</view>
          <image v-if="userPhotoUrl" class="compare-photo" :src="userPhotoUrl" mode="aspectFit" />
          <view v-else class="compare-photo-placeholder">
            <text class="compare-photo-text">你</text>
          </view>
        </view>
        <view class="compare-vs">
          <text class="vs-icon">VS</text>
        </view>
        <view class="compare-item">
          <view class="compare-label">{{ topStar.name || '明星' }}</view>
          <image class="compare-photo" v-if="topStar.url" :src="topStar.url" mode="aspectFit" />
          <view v-else class="compare-photo-placeholder">
            <text class="compare-photo-text">{{ topStar.name ? topStar.name.substring(0, 1) : '星' }}</text>
          </view>
        </view>
      </view>
    </view>

    <view class="top-card" v-if="topStar.name">
      <view class="top-badge">🏆 最匹配</view>
      <text class="result-label">{{ resultLabel }}</text>
      <view class="star-photo-wrap" v-if="topStar.url">
        <image class="star-photo" :src="topStar.url" mode="aspectFill" />
        <view class="score-overlay">
          <text class="score-value">{{ topStar.score }}</text>
          <text class="score-unit">分</text>
        </view>
      </view>
      <text class="star-name">{{ topStar.name }}</text>
      <view class="score-bar-wrap">
        <view class="score-labels">
          <text class="score-label">相似度</text>
          <text class="score-percent">{{ scorePercent }}%</text>
        </view>
        <view class="score-bar-bg">
          <view class="score-bar-fill" :style="{ width: scorePercent + '%' }"></view>
        </view>
      </view>
      <view class="fun-text-wrap">
        <text class="fun-text">{{ funText }}</text>
      </view>
    </view>

    <view class="no-result" v-if="!topStar.name">
      <text class="no-result-text">暂无比对结果</text>
    </view>

    <view class="others-section" v-if="otherStars.length > 0">
      <view class="others-header">
        <view class="others-line"></view>
        <text class="others-title">其他相似明星</text>
        <view class="others-line"></view>
      </view>
      <view class="others-list">
        <view v-for="(item, idx) in otherStars" :key="item.person_id" class="other-item">
          <image v-if="item.url" class="other-photo" :src="item.url" mode="aspectFill" />
          <view v-else class="other-photo-placeholder">
            <text class="other-photo-text">{{ (item.name || '').substring(0, 1) }}</text>
          </view>
          <view class="other-info">
            <text class="other-name">{{ item.name }}</text>
          </view>
          <view class="other-score-wrap">
            <text class="other-score-value">{{ item.score }}</text>
            <text class="other-score-unit">分</text>
          </view>
        </view>
      </view>
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
        <view class="more-feature-item" @click="goCouple">
          <view class="more-feature-icon couple-bg">
            <text class="more-feature-emoji">💑</text>
          </view>
          <view class="more-feature-info">
            <text class="more-feature-name">夫妻相/闺蜜相</text>
            <text class="more-feature-desc">测测你们的缘分指数</text>
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
      results: [],
      topStar: {},
      otherStars: [],
      scorePercent: 0,
      userPhotoUrl: '',
      userGender: 1
    }
  },

  computed: {
    subtitleText() {
      if (this.userGender === 1) {
        return '如果你变成女生，会撞脸哪位女星？';
      }
      return '如果你变成男生，会撞脸哪位男星？';
    },

    resultLabel() {
      if (this.userGender === 1) {
        return '如果你是女生，最像 ' + this.topStar.name;
      }
      return '如果你是男生，最像 ' + this.topStar.name;
    },

    funText() {
      var name = this.topStar.name || '';
      var score = this.scorePercent || 0;
      if (this.userGender === 1) {
        if (score >= 70) return '哇！你变成女生简直就是' + name + '本人！这颜值绝了~';
        if (score >= 50) return '你变成女生和' + name + '有几分神似，异性缘一定很好！';
        return '你变成女生有自己的独特气质，和' + name + '有微妙的相似~';
      } else {
        if (score >= 70) return '天哪！你变成男生就是' + name + '翻版！帅气值拉满！';
        if (score >= 50) return '你变成男生和' + name + '颇有几分相似，帅气挡不住！';
        return '你变成男生有自己独特的魅力，和' + name + '有几分神似~';
      }
    }
  },

  onLoad(op) {
    var shareId = op ? op.shareId : '';
    this.loadResults();
    shareUtil.handleShareBonus(this.$app, shareId);
  },

  onShareAppMessage() {
    var name = this.topStar.name || '明星';
    var score = this.scorePercent || 0;
    var title = this.userGender === 1
      ? '如果我变成女生，最像' + name + '（相似度' + score + '%）！快来测测你的跨性别明星脸~'
      : '如果我变成男生，最像' + name + '（相似度' + score + '%）！快来测测你的跨性别明星脸~';
    var config = shareUtil.getShareConfig(title, '/pages/cross-gender/cross-gender');
    if (this.userPhotoUrl) {
      config.imageUrl = this.userPhotoUrl;
    }
    return config;
  },

  onShareTimeline() {
    var name = this.topStar.name || '明星';
    var score = this.scorePercent || 0;
    var title = this.userGender === 1
      ? '如果我变成女生，最像' + name + '（相似度' + score + '%）！'
      : '如果我变成男生，最像' + name + '（相似度' + score + '%）！';
    var config = shareUtil.getTimelineConfig(title);
    if (this.userPhotoUrl) {
      config.imageUrl = this.userPhotoUrl;
    }
    return config;
  },

  methods: {
    loadResults() {
      try {
        var data = uni.getStorageSync('crossGenderResults');
        if (data && data.length > 0) {
          this.results = data;
          this.topStar = data[0];
          this.otherStars = data.slice(1);
          var score = this.topStar.score || 0;
          this.scorePercent = score > 100 ? 100 : Math.floor(score);
        }

        var photoUrl = uni.getStorageSync('crossGenderUserPhoto');
        if (photoUrl) this.userPhotoUrl = photoUrl;

        var gender = uni.getStorageSync('crossGenderUserGender');
        if (gender) this.userGender = gender;
      } catch (e) {
        console.error('读取结果失败', e);
        uni.showToast({ title: '数据加载失败', icon: 'none' });
      }
    },

    reTest() {
      uni.reLaunch({ url: '/pages/cross-gender/cross-gender' });
    },

    goHome() {
      uni.reLaunch({ url: '/pages/index/index' });
    },

    goStarFace() {
      uni.switchTab({ url: '/pages/index/index' });
    },

    goCouple() {
      uni.switchTab({ url: '/pages/couple/couple' });
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
  background: linear-gradient(180deg, #f0f0ff 0%, #fff0f5 40%, #fafafa 100%);
}

.header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30rpx;
}

.header-title {
  font-size: 44rpx;
  font-weight: 800;
  color: #667eea;
  margin-bottom: 8rpx;
}

.header-subtitle {
  font-size: 24rpx;
  color: #764ba2;
  font-weight: 600;
}

.compare-card {
  width: 560rpx;
  background: #fff;
  border-radius: 40rpx;
  padding: 30rpx;
  box-shadow: 0 12rpx 40rpx rgba(102, 126, 234, 0.2);
  margin-bottom: 30rpx;
}

.compare-title {
  font-size: 28rpx;
  font-weight: 700;
  color: #667eea;
  text-align: center;
  margin-bottom: 24rpx;
}

.compare-content {
  display: flex;
  align-items: center;
  justify-content: space-around;
  gap: 20rpx;
}

.compare-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12rpx;
  flex: 1;
}

.compare-label {
  font-size: 24rpx;
  font-weight: 700;
  color: #666;
}

.compare-photo {
  width: 200rpx;
  height: 240rpx;
  border-radius: 24rpx;
  box-shadow: 0 8rpx 24rpx rgba(102, 126, 234, 0.25);
  background-color: #f5f5f5;
}

.compare-photo-placeholder {
  width: 200rpx;
  height: 240rpx;
  border-radius: 24rpx;
  background: linear-gradient(135deg, #e8e0ff 0%, #d0c0ff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8rpx 24rpx rgba(102, 126, 234, 0.25);
}

.compare-photo-text {
  font-size: 80rpx;
  color: #667eea;
  font-weight: 800;
}

.compare-vs {
  display: flex;
  align-items: center;
  justify-content: center;
}

.vs-icon {
  font-size: 28rpx;
  font-weight: 800;
  color: #fff;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 12rpx 20rpx;
  border-radius: 50%;
  box-shadow: 0 4rpx 16rpx rgba(102, 126, 234, 0.3);
}

.top-card {
  width: 560rpx;
  background: #fff;
  border-radius: 40rpx;
  padding: 40rpx 30rpx;
  box-shadow: 0 12rpx 40rpx rgba(102, 126, 234, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20rpx;
}

.top-badge {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  font-size: 24rpx;
  font-weight: 700;
  padding: 10rpx 28rpx;
  border-radius: 36rpx;
  box-shadow: 0 6rpx 20rpx rgba(102, 126, 234, 0.3);
}

.result-label {
  font-size: 30rpx;
  font-weight: 700;
  color: #333;
  text-align: center;
}

.star-photo-wrap {
  width: 360rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.star-photo {
  width: 360rpx;
  height: 440rpx;
  border-radius: 36rpx;
  box-shadow: 0 12rpx 40rpx rgba(102, 126, 234, 0.3);
}

.score-overlay {
  position: absolute;
  bottom: -20rpx;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  padding: 12rpx 32rpx;
  border-radius: 36rpx;
  display: flex;
  align-items: baseline;
  box-shadow: 0 8rpx 24rpx rgba(102, 126, 234, 0.4);
}

.score-value {
  font-size: 40rpx;
  font-weight: 800;
}

.score-unit {
  font-size: 24rpx;
  margin-left: 4rpx;
}

.star-name {
  font-size: 40rpx;
  font-weight: 800;
  color: #667eea;
  text-align: center;
  margin-top: 10rpx;
}

.score-bar-wrap {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 12rpx;
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
  font-size: 24rpx;
  font-weight: 700;
  color: #667eea;
}

.score-bar-bg {
  width: 100%;
  height: 20rpx;
  background: #f0f0f0;
  border-radius: 10rpx;
  overflow: hidden;
}

.score-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 10rpx;
  transition: width 1s ease;
}

.fun-text-wrap {
  width: 100%;
  background: #fafafa;
  border-radius: 24rpx;
  padding: 24rpx;
}

.fun-text {
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

.others-section {
  width: 560rpx;
  margin-top: 40rpx;
}

.others-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20rpx;
  margin-bottom: 24rpx;
}

.others-line {
  width: 60rpx;
  height: 4rpx;
  background: linear-gradient(90deg, transparent, #667eea, transparent);
  border-radius: 2rpx;
}

.others-title {
  font-size: 28rpx;
  font-weight: 700;
  color: #666;
}

.others-list {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.other-item {
  display: flex;
  align-items: center;
  gap: 20rpx;
  background: #fff;
  border-radius: 24rpx;
  padding: 20rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.06);
}

.other-photo {
  width: 120rpx;
  height: 120rpx;
  border-radius: 20rpx;
  flex-shrink: 0;
  box-shadow: 0 4rpx 16rpx rgba(102, 126, 234, 0.15);
}

.other-photo-placeholder {
  width: 120rpx;
  height: 120rpx;
  border-radius: 20rpx;
  flex-shrink: 0;
  background: linear-gradient(135deg, #e8e0ff 0%, #d0c0ff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.other-photo-text {
  font-size: 48rpx;
  color: #667eea;
  font-weight: 800;
}

.other-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.other-name {
  font-size: 28rpx;
  font-weight: 700;
  color: #333;
}

.other-score-wrap {
  display: flex;
  align-items: baseline;
  gap: 4rpx;
}

.other-score-value {
  font-size: 32rpx;
  font-weight: 800;
  color: #667eea;
}

.other-score-unit {
  font-size: 20rpx;
  color: #667eea;
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
  color: #667eea;
  font-size: 30rpx;
  font-weight: 700;
  border-radius: 44rpx;
  border: 3rpx solid #667eea;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10rpx;
  box-shadow: 0 4rpx 16rpx rgba(102, 126, 234, 0.2);
}

.re-test-btn {
  width: 100%;
  height: 88rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  font-size: 30rpx;
  font-weight: 700;
  border-radius: 44rpx;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10rpx;
  box-shadow: 0 8rpx 24rpx rgba(102, 126, 234, 0.35);
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
  background: linear-gradient(90deg, transparent, #667eea, transparent);
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

.couple-bg {
  background: linear-gradient(135deg, #ffe0f0 0%, #e8d0ff 100%);
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
