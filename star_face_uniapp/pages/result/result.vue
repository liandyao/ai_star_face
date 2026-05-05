<template>
  <view class="container">
    <view class="header">
      <text class="header-title">✨ 比对结果</text>
      <text class="header-subtitle">发现你的明星脸</text>
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
      <text class="result-label">你与 {{ topStar.name }} 最像</text>
      <view class="star-photo-wrap" v-if="topStar.url">
        <image class="star-photo" :src="topStar.url" mode="aspectFill" />
        <view class="score-overlay">
          <text class="score-value">{{ topStar.score }}</text>
          <text class="score-unit">分</text>
        </view>
      </view>
      <view class="star-photo-wrap" v-else>
        <view class="star-photo-placeholder">
          <text class="star-photo-text">{{ topStar.name.substring(0, 1) }}</text>
        </view>
        <view class="score-overlay">
          <text class="score-value">{{ topStar.score }}</text>
          <text class="score-unit">分</text>
        </view>
      </view>
      <text class="star-name">{{ topStar.name }}</text>
      <text class="star-remark" v-if="topStar.remark">{{ topStar.remark }}</text>
      <view class="score-bar-wrap">
        <view class="score-labels">
          <text class="score-label">相似度</text>
          <text class="score-percent">{{ scorePercent }}%</text>
        </view>
        <view class="score-bar-bg">
          <view class="score-bar-fill" :style="{ width: scorePercent + '%' }"></view>
        </view>
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
            <text class="other-remark" v-if="item.remark">{{ item.remark }}</text>
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
        <text class="retest-text">开始比对</text>
      </button>
    </view>
  </view>
</template>

<script>
export default {
  // 页面数据定义
  data() {
    return {
      results: [],         // 所有比对结果数组
      topStar: {},         // 最相似的明星信息
      otherStars: [],      // 其他相似明星列表
      scorePercent: 0,     // 相似度百分比，用于进度条显示
      userPhotoUrl: ''     // 用户上传的照片URL，用于对比展示和分享
    }
  },

  // 页面加载时从本地存储读取比对结果
  onLoad() {
    this.loadResults()
  },

  // 分享给朋友时的配置
  onShareAppMessage() {
    var name = this.topStar.name || '明星'
    var score = this.scorePercent || 0
    return {
      title: '我和' + name + '相似度' + score + '%，快来测测你的明星脸！',
      path: '/pages/index/index',
      imageUrl: this.userPhotoUrl || ''  // 使用用户上传的照片作为分享封面
    }
  },

  // 分享到朋友圈时的配置
  onShareTimeline() {
    var name = this.topStar.name || '明星'
    var score = this.scorePercent || 0
    return {
      title: '我和' + name + '相似度' + score + '%，快来测测你的明星脸！',
      query: '',
      imageUrl: this.userPhotoUrl || ''  // 使用用户上传的照片作为分享封面
    }
  },

  methods: {
    // 从本地存储加载比对结果和用户照片
    loadResults() {
      try {
        // 读取比对结果
        var data = uni.getStorageSync('faceResults')
        if (data && data.length > 0) {
          this.results = data
          this.topStar = data[0]                    // 第一个是最相似的明星
          this.otherStars = data.slice(1)           // 其余的是其他相似明星
          var score = this.topStar.score || 0
          // 将分数转换为百分比，最高100%
          this.scorePercent = score > 100 ? 100 : Math.floor(score)
        } else {
          uni.showToast({ title: '未获取到比对结果', icon: 'none' })
        }

        // 读取用户上传的照片URL
        var photoUrl = uni.getStorageSync('userPhotoUrl')
        if (photoUrl) {
          this.userPhotoUrl = photoUrl
        }
      } catch (e) {
        console.error('读取结果失败', e)
        uni.showToast({ title: '数据加载失败', icon: 'none' })
      }
    },

    // 重新测试：返回首页
    reTest() {
      uni.reLaunch({ url: '/pages/index/index' })
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
  background: linear-gradient(180deg, #fff0f5 0%, #fff5f8 40%, #fafafa 100%);
}

.header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 40rpx;
}

.header-title {
  font-size: 44rpx;
  font-weight: 800;
  color: #ff6b9d;
  margin-bottom: 8rpx;
}

.header-subtitle {
  font-size: 24rpx;
  color: #999;
  letter-spacing: 1rpx;
}

.compare-card {
  width: 560rpx;
  background: #fff;
  border-radius: 40rpx;
  padding: 30rpx;
  box-shadow: 0 12rpx 40rpx rgba(255, 107, 157, 0.2);
  margin-bottom: 30rpx;
}

.compare-title {
  font-size: 28rpx;
  font-weight: 700;
  color: #ff6b9d;
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
  box-shadow: 0 8rpx 24rpx rgba(255, 107, 157, 0.25);
  background-color: #f5f5f5;
}

.compare-photo-placeholder {
  width: 200rpx;
  height: 240rpx;
  border-radius: 24rpx;
  background: linear-gradient(135deg, #ffe0ec 0%, #ffd0e0 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8rpx 24rpx rgba(255, 107, 157, 0.25);
}

.compare-photo-text {
  font-size: 80rpx;
  color: #ff6b9d;
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
  color: #fff1f6;
  background: linear-gradient(135deg, #ff6b9d 0%, #ff4757 100%);
  padding: 12rpx 20rpx;
  border-radius: 50%;
  box-shadow: 0 4rpx 16rpx rgba(255, 71, 87, 0.3);
}

.top-card {
  width: 560rpx;
  background: #fff;
  border-radius: 40rpx;
  padding: 40rpx 30rpx;
  box-shadow: 0 12rpx 40rpx rgba(255, 107, 157, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20rpx;
}

.top-badge {
  background: linear-gradient(135deg, #ff6b9d 0%, #ff4757 100%);
  color: #fff;
  font-size: 24rpx;
  font-weight: 700;
  padding: 10rpx 28rpx;
  border-radius: 36rpx;
  box-shadow: 0 6rpx 20rpx rgba(255, 71, 87, 0.3);
}

.result-label {
  font-size: 32rpx;
  font-weight: 700;
  color: #333;
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
  box-shadow: 0 12rpx 40rpx rgba(255, 107, 157, 0.3);
}

.star-photo-placeholder {
  width: 360rpx;
  height: 440rpx;
  border-radius: 36rpx;
  background: linear-gradient(135deg, #ffe0ec 0%, #ffd0e0 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 12rpx 40rpx rgba(255, 107, 157, 0.3);
}

.star-photo-text {
  font-size: 160rpx;
  color: #ff6b9d;
  font-weight: 800;
}

.score-overlay {
  position: absolute;
  bottom: -20rpx;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, #ff6b9d 0%, #ff4757 100%);
  color: #fff;
  padding: 12rpx 32rpx;
  border-radius: 36rpx;
  display: flex;
  align-items: baseline;
  box-shadow: 0 8rpx 24rpx rgba(255, 71, 87, 0.4);
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
  color: #ff6b9d;
  text-align: center;
  margin-top: 10rpx;
}

.star-remark {
  font-size: 22rpx;
  color: #999;
  text-align: center;
  background: #f5f5f5;
  padding: 8rpx 20rpx;
  border-radius: 24rpx;
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
  color: #ff6b9d;
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
  background: linear-gradient(90deg, #ff6b9d, #ff4757);
  border-radius: 10rpx;
  transition: width 1s ease;
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
  background: linear-gradient(90deg, transparent, #ff6b9d, transparent);
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
  box-shadow: 0 4rpx 16rpx rgba(255, 107, 157, 0.15);
}

.other-photo-placeholder {
  width: 120rpx;
  height: 120rpx;
  border-radius: 20rpx;
  flex-shrink: 0;
  background: linear-gradient(135deg, #ffe0ec 0%, #ffd0e0 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.other-photo-text {
  font-size: 48rpx;
  color: #ff6b9d;
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

.other-remark {
  font-size: 20rpx;
  color: #999;
}

.other-score-wrap {
  display: flex;
  align-items: baseline;
  gap: 4rpx;
}

.other-score-value {
  font-size: 32rpx;
  font-weight: 800;
  color: #ff6b9d;
}

.other-score-unit {
  font-size: 20rpx;
  color: #ff6b9d;
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
  color: #ff6b9d;
  font-size: 30rpx;
  font-weight: 700;
  border-radius: 44rpx;
  border: 3rpx solid #ff6b9d;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10rpx;
  box-shadow: 0 4rpx 16rpx rgba(255, 107, 157, 0.2);
}

.share-icon {
  font-size: 32rpx;
}

.re-test-btn {
  width: 100%;
  height: 88rpx;
  background: linear-gradient(135deg, #ff6b9d 0%, #ff4757 100%);
  color: #fff;
  font-size: 30rpx;
  font-weight: 700;
  border-radius: 44rpx;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10rpx;
  box-shadow: 0 8rpx 24rpx rgba(255, 71, 87, 0.35);
}

.retest-icon {
  font-size: 32rpx;
}
</style>
