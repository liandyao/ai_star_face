<template>
  <view class="container">
    <view class="header">
      <view class="logo-wrap">
        <text class="logo-icon">🌈</text>
      </view>
      <text class="title">跨性别撞脸</text>
      <text class="subtitle">{{ subtitleText }}</text>
    </view>

    <view class="gender-select">
      <view class="gender-card" :class="{ active: userGender === 1 }" @click="selectGender(1)">
        <text class="gender-emoji">👨</text>
        <text class="gender-label">我是男生</text>
        <text class="gender-hint">测测你的女星脸</text>
      </view>
      <view class="gender-card" :class="{ active: userGender === 2 }" @click="selectGender(2)">
        <text class="gender-emoji">👩</text>
        <text class="gender-label">我是女生</text>
        <text class="gender-hint">测测你的男星脸</text>
      </view>
    </view>

    <view class="image-card" @click="showChooseAction" v-if="userGender > 0">
      <image v-if="hasImage" class="preview-img" :src="tempImagePath" mode="aspectFill" @click.stop=""></image>
      <view v-if="!hasImage" class="upload-placeholder">
        <view class="upload-icon-circle">
          <text class="upload-icon">📸</text>
        </view>
        <text class="upload-text">点击上传正脸照</text>
        <view class="upload-tips">
          <text class="upload-tip-item">✨ 正面拍摄效果更佳</text>
          <text class="upload-tip-item">✨ 光线均匀，素颜更佳</text>
        </view>
      </view>
      <view v-if="hasImage" class="rechoose-btn" @click.stop="showChooseAction">
        <text class="rechoose-icon">📷</text>
        <text class="rechoose-text">重新上传</text>
      </view>
    </view>

    <view class="target-hint" v-if="userGender > 0">
      <text class="target-text">{{ targetHintText }}</text>
    </view>

    <view class="score-wrap" v-if="userGender > 0">
      <view class="score-badge">
        <text class="score-icon">💎</text>
        <text class="score-text">剩余积分：{{ score }}</text>
      </view>
      <view class="score-tips" @click="showScoreModal = true">
        <text class="tips-text">如何获取积分？</text>
      </view>
    </view>

    <view class="tip-wrap" v-if="userGender > 0">
      <text class="tip-text">{{ tipText }}</text>
    </view>

    <button class="compare-btn" v-if="userGender > 0" :disabled="loading || !hasImage || failCount >= 3" @click="startCompare">
      <text v-if="failCount >= 3">🥲 愿君明日再来</text>
      <text v-else-if="loading">⏳ 正在比对中...</text>
      <text v-else>🌈 开始比对</text>
    </button>

    <view class="fail-hint" v-if="failCount >= 3 && userGender > 0">
      <text class="fail-hint-icon">🌙</text>
      <text class="fail-hint-text">今日比对次数已用完，明日再来试试吧~</text>
    </view>

    <view class="footer">
      <view class="privacy-badge">
        <text class="privacy-icon">🔒</text>
        <text class="privacy-text">人脸数据仅用于本次比对，不做他用，结果仅供娱乐</text>
      </view>
    </view>

    <view class="score-modal" v-if="showScoreModal" @click="showScoreModal = false">
      <view class="score-modal-panel" @click.stop="">
        <text class="score-modal-title">获取积分</text>
        <view class="score-modal-body">
          <view class="score-modal-item">
            <text class="score-modal-item-icon">📤</text>
            <view class="score-modal-item-info">
              <text class="score-modal-item-name">分享给好友</text>
              <text class="score-modal-item-desc">新用户点击之后双方各得5积分</text>
            </view>
            <text class="score-modal-item-score">+5</text>
          </view>
          <view class="score-modal-item">
            <text class="score-modal-item-icon">🎬</text>
            <view class="score-modal-item-info">
              <text class="score-modal-item-name">观看视频广告</text>
              <text class="score-modal-item-desc">观看短视频即可获得5积分</text>
            </view>
            <text class="score-modal-item-score">+5</text>
          </view>
        </view>
        <view class="score-modal-btns">
          <button class="score-modal-btn share-btn-modal" open-type="share" @click="showScoreModal = false">分享好友</button>
          <button class="score-modal-btn ad-btn-modal" @click="showScoreModal = false; showAd()">观看视频</button>
        </view>
      </view>
    </view>

    <canvas canvas-id="crossCanvas" :style="{width: canvasWidth + 'px', height: canvasHeight + 'px', position: 'fixed', left: '-9999px', top: '-9999px'}"></canvas>
  </view>
</template>

<script>
import AdUtil from '@/common/AdUtil.js';
import shareUtil from '@/common/shareUtil.js';
import mediaCheckUtil from '@/common/mediaCheckUtil.js';

export default {
  data() {
    return {
      userGender: 0,
      tempImagePath: '',
      hasImage: false,
      loading: false,
      tipText: '让生活多一点乐趣',
      score: 0,
      canvasWidth: 800,
      canvasHeight: 800,
      uploadedPhotoUrl: '',
      showScoreModal: false,
      failCount: 0,
      pendingAction: ''
    }
  },

  computed: {
    subtitleText() {
      if (this.userGender === 1) {
        return '如果你变成女生，会撞脸哪位女星？';
      } else if (this.userGender === 2) {
        return '如果你变成男生，会撞脸哪位男星？';
      }
      return '选择性别，发现你的异性明星脸';
    },

    targetHintText() {
      if (this.userGender === 1) {
        return '🎯 将为你匹配女明星库';
      } else if (this.userGender === 2) {
        return '🎯 将为你匹配男明星库';
      }
      return '';
    }
  },

  onLoad(op) {
    var shareId = op ? op.shareId : '';
    var storedFailCount = uni.getStorageSync('crossGenderFailCount') || 0;
    var storedFailDate = uni.getStorageSync('crossGenderFailDate') || '';
    var today = new Date().toISOString().substring(0, 10);
    if (storedFailDate === today) {
      this.failCount = storedFailCount;
    } else {
      this.failCount = 0;
      uni.setStorageSync('crossGenderFailCount', 0);
      uni.setStorageSync('crossGenderFailDate', today);
    }

    const app = getApp();
    if (app.globalData.loginPromise) {
      app.globalData.loginPromise.then(() => {
        this.getScore();
      }).catch(() => {
        this.getScore();
      });
    } else {
      this.getScore();
    }
    this.initAd();
    this.initInterstitialAd();
    shareUtil.handleShareBonus(this.$app, shareId);
  },

  onShow() {
    if (uni.getStorageSync("openid")) {
      this.getScore();
    }
  },

  onShareAppMessage() {
    return shareUtil.getShareConfig('跨性别撞脸 - ' + this.subtitleText, '/pages/cross-gender/cross-gender');
  },

  onShareTimeline() {
    return shareUtil.getTimelineConfig('跨性别撞脸 - ' + this.subtitleText);
  },

  methods: {
    getScore() {
      let url = this.$app.apiPath.common.userSurplus;
      this.$app.post(url).then(res => {
        if (res.code == 200) {
          this.score = res.data;
        }
      });
    },

    initAd() {
      let that = this;
      AdUtil.rewarded.load(() => {
        let url = that.$app.apiPath.common.videoPlus;
        that.$app.post(url).then(res => {
          if (res.code == 200) {
            that.score = that.score + 5;
            uni.showToast({ title: '积分+5', icon: 'success' });
          }
          that.tryPendingAction();
        }, err => {
          that.score = that.score + 5;
          that.tryPendingAction();
        });
      });
    },

    tryPendingAction() {
      var that = this;
      if (that.pendingAction === 'compare') {
        that.pendingAction = '';
        setTimeout(function() { that.startCompare(); }, 500);
      }
    },

    showAd() {
      uni.showLoading({ title: '正在加载...' });
      AdUtil.rewarded.show();
      setTimeout(() => { uni.hideLoading(); }, 2000);
    },

    selectGender(g) {
      this.userGender = g;
      this.hasImage = false;
      this.tempImagePath = '';
      this.tipText = '让生活多一点乐趣';
    },

    showChooseAction() {
      var that = this;
      uni.showActionSheet({
        itemList: ['🤳 自拍', '🖼️ 从相册选择'],
        success: function(res) {
          if (res.tapIndex === 0) {
            that.takePhoto();
          } else {
            that.chooseFromAlbum();
          }
        }
      });
    },

    takePhoto() {
      var that = this;
      uni.chooseMedia({
        count: 1,
        mediaType: ['image'],
        sourceType: ['camera'],
        camera: 'front',
        sizeType: ['compressed'],
        success: function(res) {
          that.onImageSelected(res.tempFiles[0].tempFilePath);
        },
        fail: function(err) {
          if (err.errMsg && err.errMsg.indexOf('cancel') === -1) {
            uni.chooseImage({
              count: 1,
              sourceType: ['camera'],
              sizeType: ['compressed'],
              success: function(res2) {
                that.onImageSelected(res2.tempFilePaths[0]);
              }
            });
          }
        }
      });
    },

    chooseFromAlbum() {
      var that = this;
      uni.chooseImage({
        count: 1,
        sourceType: ['album'],
        sizeType: ['compressed'],
        success: function(res) {
          that.onImageSelected(res.tempFilePaths[0]);
        }
      });
    },

    onImageSelected(path) {
      this.tempImagePath = path;
      this.hasImage = true;
      this.tipText = '照片已选择，点击「开始比对」看看结果';
      uni.showToast({ title: '照片已选择', icon: 'success', duration: 1500 });
    },

    compressImage(imgPath, callback) {
      var that = this;
      uni.getImageInfo({
        src: imgPath,
        success: function(info) {
          var w = info.width;
          var h = info.height;
          var maxSide = 800;

          if (w <= maxSide && h <= maxSide) {
            uni.compressImage({
              src: imgPath,
              quality: 80,
              success: function(compressRes) {
                callback(compressRes.tempFilePath);
              },
              fail: function() {
                callback(imgPath);
              }
            });
            return;
          }

          var ratio = Math.min(maxSide / w, maxSide / h);
          var newW = Math.round(w * ratio);
          var newH = Math.round(h * ratio);
          that.canvasWidth = newW;
          that.canvasHeight = newH;

          setTimeout(function() {
            var ctx = uni.createCanvasContext('crossCanvas', that);
            ctx.clearRect(0, 0, newW, newH);
            ctx.drawImage(imgPath, 0, 0, newW, newH);
            ctx.draw(false, function() {
              setTimeout(function() {
                uni.canvasToTempFilePath({
                  canvasId: 'crossCanvas',
                  x: 0, y: 0,
                  width: newW, height: newH,
                  destWidth: newW, destHeight: newH,
                  quality: 0.8,
                  fileType: 'jpg',
                  success: function(canvasRes) {
                    callback(canvasRes.tempFilePath);
                  },
                  fail: function() {
                    uni.compressImage({
                      src: imgPath,
                      quality: 80,
                      success: function(compressRes) {
                        callback(compressRes.tempFilePath);
                      },
                      fail: function() {
                        callback(imgPath);
                      }
                    });
                  }
                }, that);
              }, 300);
            });
          }, 100);
        },
        fail: function() {
          callback(imgPath);
        }
      });
    },

    startCompare() {
      var that = this;

      if (that.failCount >= 3) {
        uni.showModal({
          title: '今日比对次数已用完',
          content: '明日再来试试吧，也许下次就能找到你的异性明星脸~',
          showCancel: false,
          confirmText: '好的'
        });
        return;
      }

      if (!that.hasImage) {
        uni.showToast({ title: '请先上传照片', icon: 'none' });
        return;
      }
      if (that.loading) return;

      if (that.score < 5) {
        that.pendingAction = 'compare';
        that.showScoreModal = true
        return
      }

      that.loading = true;
      that.tipText = '正在处理，请稍候...';
      that.compressImage(that.tempImagePath, function(compressedPath) {
        that.uploadAndSearch(compressedPath);
      });
    },

    uploadAndSearch(compressedPath) {
      var that = this;
      var fileName = 'cross_user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9) + '.jpg';
      var cloudPath = 'star_user_pic/' + fileName;

      uniCloud.uploadFile({
        filePath: compressedPath,
        cloudPath: cloudPath,
        success: function(uploadRes) {
          that.uploadedPhotoUrl = 'https://env-00jy674l53ts.normal.cloudstatic.cn/' + cloudPath;
          that.checkUploadedImage(that.uploadedPhotoUrl, function() {
            that.readImageAndSearch(compressedPath);
          });
        },
        fail: function(err) {
          that.resetState();
          uni.showToast({ title: '上传失败，请重试', icon: 'none' });
        }
      });
    },

    checkUploadedImage(url, successCallback) {
      var that = this;
      mediaCheckUtil.check(url, that.$app).then(function() {
        successCallback();
      }).catch(function(err) {
        that.resetState();
        uni.showModal({
          title: '图片审核失败',
          content: err.message || '图片暂时无法通过安全校验，请更换照片',
          showCancel: false
        });
      });
    },

    readImageAndSearch(imgPath) {
      var that = this;
      try {
        var fs = uni.getFileSystemManager();
        fs.readFile({
          filePath: imgPath,
          encoding: 'base64',
          success: function(fRes) {
            var base64 = fRes.data;
            if (!base64) {
              that.resetState();
              uni.showToast({ title: '图片读取失败', icon: 'none' });
              return;
            }
            that.tipText = '正在检测人脸...';
            that.callCloudSearch(base64);
          },
          fail: function() {
            that.resetState();
            uni.showToast({ title: '图片转换失败', icon: 'none' });
          }
        });
      } catch (e) {
        that.resetState();
        uni.showToast({ title: '图片处理异常', icon: 'none' });
      }
    },

    callCloudSearch(base64) {
      var that = this;
      that.tipText = '正在比对人脸...';

      setTimeout(function() {
        that.showInterstitialAd();
      }, 1000);

      uniCloud.callFunction({
        name: 'faceSearch',
        data: {
          action: 'searchGender',
          image: base64,
          userGender: that.userGender
        },
        success: function(res) {
          var result = res.result || {};
          if (result.code !== 0) {
            that.onFailCount();
            that.resetState();
            uni.showModal({
              title: '操作失败',
              content: result.message || '请重试',
              showCancel: false
            });
            return;
          }

          var searchResult = result.data || [];
          if (!searchResult || searchResult.length === 0) {
            that.onFailCount();
            that.resetState();
            uni.showModal({
              title: '未找到相似明星',
              content: '没有匹配到相似的异性明星，试试其他照片',
              showCancel: false
            });
            return;
          }

          let url = that.$app.apiPath.common.useScore;
          that.$app.post(url, { score: 5 }).then(function(res2) {
            if (res2.code == 200) {
              that.getScore();
            }
          });

          that.loading = false;
          that.tipText = '照片已选择，点击「开始比对」看看结果';

          try {
            uni.setStorageSync('crossGenderResults', searchResult);
            uni.setStorageSync('crossGenderUserPhoto', that.uploadedPhotoUrl || '');
            uni.setStorageSync('crossGenderUserGender', that.userGender);
          } catch (e) {
            console.error('存储结果失败:', e);
          }

          

          uni.navigateTo({
            url: '/pages/cross-gender-result/cross-gender-result'
          });
        },
        fail: function(err) {
          console.error('云函数调用失败:', err);
          that.onFailCount();
          that.resetState();
          uni.showModal({
            title: '服务异常',
            content: '云服务连接失败，请检查网络后重试',
            showCancel: false
          });
        }
      });
    },

    resetState() {
      this.loading = false;
      this.tipText = '照片已选择，点击「开始比对」看看结果';
    },

    onFailCount() {
      this.failCount++;
      var today = new Date().toISOString().substring(0, 10);
      uni.setStorageSync('crossGenderFailCount', this.failCount);
      uni.setStorageSync('crossGenderFailDate', today);
    },

    initInterstitialAd() {
      AdUtil.interstitial.load('adunit-ce26991cb47c9e83');
    },

    showInterstitialAd() {
      AdUtil.interstitial.show();
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
  background: linear-gradient(180deg, #f0f0ff 0%, #fff0f5 40%, #fafafa 100%);
}

.header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 40rpx;
}

.logo-wrap {
  width: 120rpx;
  height: 120rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8rpx 32rpx rgba(102, 126, 234, 0.3);
  margin-bottom: 20rpx;
}

.logo-icon { font-size: 64rpx; }

.title {
  font-size: 48rpx;
  font-weight: 800;
  color: #667eea;
  letter-spacing: 2rpx;
  margin-bottom: 12rpx;
}

.subtitle {
  font-size: 26rpx;
  color: #764ba2;
  font-weight: 600;
  letter-spacing: 1rpx;
}

.gender-select {
  display: flex;
  gap: 24rpx;
  margin-bottom: 40rpx;
}

.gender-card {
  width: 280rpx;
  padding: 30rpx 20rpx;
  background: #fff;
  border-radius: 32rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12rpx;
  box-shadow: 0 8rpx 32rpx rgba(0,0,0,0.08);
  border: 3rpx solid transparent;
  transition: all 0.3s;
}

.gender-card.active {
  border-color: #667eea;
  box-shadow: 0 8rpx 32rpx rgba(102, 126, 234, 0.25);
}

.gender-emoji { font-size: 64rpx; }

.gender-label {
  font-size: 28rpx;
  font-weight: 700;
  color: #333;
}

.gender-hint {
  font-size: 22rpx;
  color: #999;
}

.image-card {
  width: 520rpx;
  height: 600rpx;
  background: #fff;
  border-radius: 36rpx;
  overflow: hidden;
  position: relative;
  box-shadow: 0 12rpx 40rpx rgba(102, 126, 234, 0.15);
  margin-bottom: 24rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.preview-img {
  width: 100%;
  height: 100%;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20rpx;
}

.upload-icon-circle {
  width: 100rpx;
  height: 100rpx;
  background: linear-gradient(135deg, #e8e0ff 0%, #d0c0ff 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-icon { font-size: 48rpx; }

.upload-text {
  font-size: 28rpx;
  color: #666;
  font-weight: 600;
}

.upload-tips {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.upload-tip-item {
  font-size: 22rpx;
  color: #999;
}

.rechoose-btn {
  position: absolute;
  bottom: 20rpx;
  right: 20rpx;
  background: rgba(0,0,0,0.5);
  padding: 10rpx 24rpx;
  border-radius: 28rpx;
  display: flex;
  align-items: center;
  gap: 6rpx;
}

.rechoose-icon { font-size: 24rpx; }
.rechoose-text { color: #fff; font-size: 22rpx; }

.target-hint {
  margin-bottom: 16rpx;
}

.target-text {
  font-size: 24rpx;
  color: #667eea;
  font-weight: 600;
}

.score-wrap {
  margin-bottom: 16rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16rpx;
}

.score-badge {
  display: flex;
  align-items: center;
  gap: 8rpx;
  background: #fff;
  padding: 12rpx 28rpx;
  border-radius: 36rpx;
  box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.06);
}

.score-icon { font-size: 28rpx; }
.score-text { font-size: 24rpx; color: #666; font-weight: 600; }

.score-tips {
  padding: 10rpx 20rpx;
  background: #eef0ff;
  border-radius: 20rpx;
}

.tips-text { font-size: 22rpx; color: #667eea; }

.tip-wrap { margin-bottom: 24rpx; }
.tip-text { font-size: 24rpx; color: #999; }

.compare-btn {
  width: 560rpx;
  height: 96rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  font-size: 32rpx;
  font-weight: 700;
  border-radius: 48rpx;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8rpx 32rpx rgba(102, 126, 234, 0.35);
  margin-bottom: 30rpx;
}

.compare-btn[disabled] {
  background: #ddd;
  box-shadow: none;
  color: #999;
}

.footer { margin-top: 20rpx; }

.fail-hint {
  display: flex;
  align-items: center;
  gap: 12rpx;
  margin-top: 16rpx;
  padding: 20rpx 32rpx;
  background: linear-gradient(135deg, #fff8f0 0%, #fff0e8 100%);
  border-radius: 20rpx;
}

.fail-hint-icon { font-size: 32rpx; }

.fail-hint-text {
  font-size: 24rpx;
  color: #e67e22;
  font-weight: 600;
  line-height: 1.5;
}

.privacy-badge {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.privacy-icon { font-size: 24rpx; }
.privacy-text { font-size: 22rpx; color: #bbb; }

.score-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 1001;
  display: flex;
  align-items: center;
  justify-content: center;
}

.score-modal-panel {
  width: 600rpx;
  background: #fff;
  border-radius: 28rpx;
  padding: 40rpx 36rpx;
}

.score-modal-title {
  font-size: 34rpx;
  font-weight: 700;
  color: #333;
  text-align: center;
  display: block;
  margin-bottom: 30rpx;
}

.score-modal-body {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
  margin-bottom: 30rpx;
}

.score-modal-item {
  display: flex;
  align-items: center;
  padding: 20rpx;
  background: #fafafa;
  border-radius: 16rpx;
}

.score-modal-item-icon { font-size: 40rpx; flex-shrink: 0; }

.score-modal-item-info {
  flex: 1;
  margin-left: 16rpx;
  display: flex;
  flex-direction: column;
  gap: 4rpx;
}

.score-modal-item-name { font-size: 28rpx; font-weight: 700; color: #333; }
.score-modal-item-desc { font-size: 22rpx; color: #999; }
.score-modal-item-score { font-size: 30rpx; font-weight: 700; color: #667eea; flex-shrink: 0; margin-left: 16rpx; }

.score-modal-btns {
  display: flex;
  gap: 20rpx;
}

.score-modal-btn {
  flex: 1;
  height: 80rpx;
  line-height: 80rpx;
  font-size: 28rpx;
  font-weight: 700;
  border-radius: 40rpx;
  border: none;
  padding: 0;
  margin: 0;
}

.share-btn-modal {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
}

.ad-btn-modal {
  background: #f5f5f5;
  color: #666;
}
</style>
