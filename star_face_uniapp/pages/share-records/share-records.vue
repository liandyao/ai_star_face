<template>
  <view class="container">
    <view class="header">
      <view class="logo-wrap">
        <text class="logo-icon">📋</text>
      </view>
      <text class="title">分享记录</text>
      <text class="subtitle">查看你的分享得分情况</text>
    </view>

    <view class="score-card">
      <view class="score-card-bg">
        <view class="score-card-top">
          <text class="score-card-label">💎 当前可用积分</text>
        </view>
        <view class="score-card-bottom">
          <text class="score-card-value">{{ score }}</text>
          <text class="score-card-unit">分</text>
        </view>
        <view class="score-card-hint">
          <text class="score-card-hint-text">分享给好友，新用户点击后双方各得5积分</text>
        </view>
      </view>
    </view>

    <view class="tip-bar">
      <text class="tip-icon">🔒</text>
      <text class="tip-text">隐私保护：无法查看对方真实账号，仅展示分享时间与积分</text>
    </view>

    <view class="list-wrap" v-if="records.length > 0">
      <view class="record-card" v-for="(item, index) in records" :key="index">
        <view class="record-top">
          <view class="record-badge">
            <text class="record-badge-text">{{ index + 1 }}</text>
          </view>
          <view class="record-main">
            <text class="record-remark">{{ item.remark || '分享成功' }}</text>
            <view class="record-time-row">
              <text class="record-time-icon">🕐</text>
              <text class="record-time">{{ item.createTime || '无' }}</text>
            </view>
          </view>
          <view class="record-score-wrap">
            <text class="record-score">+5</text>
            <text class="record-score-unit">积分</text>
          </view>
        </view>
      </view>
    </view>

    <view class="empty-wrap" v-if="!loading && records.length === 0">
      <view class="empty-icon-circle">
        <text class="empty-icon">📤</text>
      </view>
      <text class="empty-text">暂无分享记录</text>
      <text class="empty-hint">分享给好友，新用户点击之后双方各得5积分</text>
    </view>

    <view class="loading-wrap" v-if="loading">
      <text class="loading-text">加载中...</text>
    </view>

    <view class="footer" v-if="records.length > 0">
      <view class="privacy-badge">
        <text class="privacy-icon">🔒</text>
        <text class="privacy-text">分享数据仅用于积分记录，结果仅供娱乐！</text>
      </view>
    </view>
  </view>
</template>

<script>
import shareUtil from '@/common/shareUtil.js';

export default {
  data() {
    return {
      records: [],
      loading: false,
      page: 1,
      score: 0
    }
  },

  onLoad() {
    this.getListDatas();
    this.getScore();
  },

  onShow() {
    if (uni.getStorageSync('openid')) {
      this.getScore();
    }
  },

  onShareAppMessage() {
    return shareUtil.getShareConfig('明星脸比对 - 测测你像哪个明星', '/pages/share-records/share-records');
  },

  onShareTimeline() {
    return shareUtil.getTimelineConfig('明星脸比对 - 测测你像哪个明星');
  },

  onReachBottom() {
    this.nextPage();
  },

  methods: {
    getScore() {
      var url = this.$app.apiPath.common.userSurplus;
      this.$app.post(url).then(res => {
        if (res.code == 200) {
          this.score = res.data;
        }
      });
    },

    nextPage() {
      this.page = this.page + 1;
      this.getListDatas();
    },

    getListDatas() {
      var that = this;
      that.loading = true;
      var url = that.$app.apiPath.user.myShare + '?page=' + that.page;
      that.$app.post(url).then(function(res) {
        that.loading = false;
        var list = res.data || [];
        if (list.length > 0) {
          that.records = that.records.concat(list);
        } else {
          if (that.page > 1) {
            uni.showToast({ title: '没有更多数据', icon: 'none' });
          }
        }
      }, function() {
        that.loading = false;
      });
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
  min-height: 100vh;
  box-sizing: border-box;
  background: linear-gradient(180deg, #fff0f5 0%, #fafafa 100%);
}

.header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 32rpx;
}

.logo-wrap {
  width: 100rpx;
  height: 100rpx;
  background: linear-gradient(135deg, #ff6b9d 0%, #ff4757 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8rpx 24rpx rgba(255, 107, 157, 0.3);
  margin-bottom: 16rpx;
}

.logo-icon { font-size: 52rpx; }

.title {
  font-size: 40rpx;
  font-weight: 800;
  color: #333;
  margin-bottom: 8rpx;
}

.subtitle {
  font-size: 24rpx;
  color: #999;
}

.score-card {
  width: 640rpx;
  margin-bottom: 24rpx;
}

.score-card-bg {
  background: linear-gradient(135deg, #ff6b9d 0%, #ff4757 100%);
  border-radius: 28rpx;
  padding: 40rpx 36rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24rpx;
  box-shadow: 0 12rpx 40rpx rgba(255, 107, 157, 0.3);
}

.score-card-top {
  width: 100%;
  text-align: center;
}

.score-card-label {
  font-size: 26rpx;
  color: rgba(255,255,255,0.9);
  font-weight: 500;
}

.score-card-bottom {
  display: flex;
  align-items: baseline;
  gap: 8rpx;
}

.score-card-value {
  font-size: 80rpx;
  font-weight: 800;
  color: #fff;
  line-height: 1;
}

.score-card-unit {
  font-size: 28rpx;
  color: rgba(255,255,255,0.8);
  font-weight: 500;
}

.score-card-hint {
  width: 100%;
  text-align: center;
  padding-top: 16rpx;
  border-top: 1rpx solid rgba(255,255,255,0.2);
}

.score-card-hint-text {
  font-size: 22rpx;
  color: rgba(255,255,255,0.7);
}

.tip-bar {
  width: 640rpx;
  background: #fff;
  border-radius: 16rpx;
  padding: 16rpx 24rpx;
  display: flex;
  align-items: center;
  gap: 10rpx;
  margin-bottom: 28rpx;
  box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04);
}

.tip-icon { font-size: 24rpx; }

.tip-text {
  font-size: 22rpx;
  color: #999;
  line-height: 1.5;
}

.list-wrap {
  width: 640rpx;
}

.record-card {
  background: #fff;
  border-radius: 24rpx;
  padding: 28rpx;
  margin-bottom: 16rpx;
  box-shadow: 0 6rpx 24rpx rgba(0,0,0,0.05);
}

.record-top {
  display: flex;
  align-items: center;
  gap: 20rpx;
}

.record-badge {
  width: 52rpx;
  height: 52rpx;
  background: linear-gradient(135deg, #ff6b9d 0%, #ff4757 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.record-badge-text {
  font-size: 24rpx;
  font-weight: 800;
  color: #fff;
}

.record-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.record-remark {
  font-size: 28rpx;
  font-weight: 600;
  color: #333;
}

.record-time-row {
  display: flex;
  align-items: center;
  gap: 6rpx;
}

.record-time-icon { font-size: 20rpx; }

.record-time {
  font-size: 22rpx;
  color: #bbb;
}

.record-score-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rpx;
  flex-shrink: 0;
}

.record-score {
  font-size: 32rpx;
  font-weight: 800;
  color: #ff6b9d;
}

.record-score-unit {
  font-size: 18rpx;
  color: #ccc;
}

.empty-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16rpx;
  margin-top: 120rpx;
}

.empty-icon-circle {
  width: 120rpx;
  height: 120rpx;
  background: linear-gradient(135deg, #ffe8f0 0%, #ffd0e0 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8rpx;
}

.empty-icon { font-size: 56rpx; }

.empty-text {
  font-size: 30rpx;
  color: #999;
  font-weight: 600;
}

.empty-hint {
  font-size: 24rpx;
  color: #ccc;
}

.loading-wrap {
  padding: 40rpx 0;
}

.loading-text {
  font-size: 26rpx;
  color: #999;
}

.footer {
  margin-top: 40rpx;
  margin-bottom: 60rpx;
}

.privacy-badge {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.privacy-icon { font-size: 22rpx; }

.privacy-text {
  font-size: 20rpx;
  color: #ccc;
}
</style>
