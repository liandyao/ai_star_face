<template>
  <view class="container">
    <view class="header">
      <view class="logo-wrap">
        <text class="logo-icon">💑</text>
      </view>
      <text class="title">夫妻相/闺蜜相</text>
      <text class="subtitle">上传两张照片，测测你们的缘分指数</text>
    </view>

    <view class="upload-area">
      <view class="upload-card" @click="chooseImage('a')">
        <image v-if="imageA" class="preview-img" :src="imageA" mode="aspectFill"></image>
        <view v-else class="upload-placeholder">
          <view class="upload-icon-circle">
            <text class="upload-icon">📸</text>
          </view>
          <text class="upload-text">上传第一张</text>
          <text class="upload-hint">你的照片</text>
        </view>
        <view v-if="imageA" class="rechoose-badge" @click.stop="chooseImage('a')">
          <text class="rechoose-text">换一张</text>
        </view>
      </view>

      <view class="vs-divider">
        <view class="vs-line"></view>
        <view class="vs-circle">
          <text class="vs-text">VS</text>
        </view>
        <view class="vs-line"></view>
      </view>

      <view class="upload-card" @click="chooseImage('b')">
        <image v-if="imageB" class="preview-img" :src="imageB" mode="aspectFill"></image>
        <view v-else class="upload-placeholder">
          <view class="upload-icon-circle">
            <text class="upload-icon">📸</text>
          </view>
          <text class="upload-text">上传第二张</text>
          <text class="upload-hint">TA的照片</text>
        </view>
        <view v-if="imageB" class="rechoose-badge" @click.stop="chooseImage('b')">
          <text class="rechoose-text">换一张</text>
        </view>
      </view>
    </view>

    <view class="score-wrap">
      <view class="score-badge">
        <text class="score-icon">💎</text>
        <text class="score-text">剩余积分：{{ score }}</text>
      </view>
      <view class="score-tips" @click="showScoreModal = true">
        <text class="tips-text">如何获取积分？</text>
      </view>
    </view>

    <view class="tip-wrap">
      <text class="tip-text">{{ tipText }}</text>
    </view>

    <button class="compare-btn" :disabled="loading || !imageA || !imageB" @click="startCompare">
      <text v-if="loading">⏳ 正在比对中...</text>
      <text v-else>💕 开始比对</text>
    </button>

    <view class="footer">
      <view class="privacy-badge">
        <text class="privacy-icon">🔒</text>
        <text class="privacy-text">人脸数据仅用于本次比对，不做他用，结果仅供娱乐！</text>
      </view>
      <view class="pk-link" @click="goBeautyPk">
        <text class="pk-link-icon">⚔️</text>
        <text class="pk-link-text">还想比颜值？试试颜值PK →</text>
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

    <canvas canvas-id="coupleCanvas" :style="{width: canvasWidth + 'px', height: canvasHeight + 'px', position: 'fixed', left: '-9999px', top: '-9999px'}"></canvas>
  </view>
</template>

<script>
import AdUtil from '@/common/AdUtil.js';
import shareUtil from '@/common/shareUtil.js';
import mediaCheckUtil from '@/common/mediaCheckUtil.js';

export default {
  data() {
    return {
      imageA: '',
      imageB: '',
      loading: false,
      tipText: '让生活多一点乐趣',
      score: 0,
      canvasWidth: 800,
      canvasHeight: 800,
      currentChoose: 'a',
      uploadedUrlA: '',
      uploadedUrlB: '',
      showScoreModal: false,
      pendingAction: ''
    }
  },

  onLoad(op) {
    let shareId = op ? op.shareId : '';
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
    shareUtil.handleShareBonus(this.$app, shareId);
  },

  onShow() {
    if (uni.getStorageSync("openid")) {
      this.getScore();
    }
  },

  onShareAppMessage() {
    return shareUtil.getShareConfig('夫妻相/闺蜜相测试 - 测测你们的缘分指数', '/pages/couple/couple');
  },

  onShareTimeline() {
    return shareUtil.getTimelineConfig('夫妻相/闺蜜相测试 - 测测你们的缘分指数');
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

    goBeautyPk() {
      uni.switchTab({ url: '/pages/beauty-pk/beauty-pk' });
    },

    chooseImage(side) {
      var that = this;
      this.currentChoose = side;
      uni.showActionSheet({
        itemList: ['🤳 自拍', '🖼️ 从相册选择'],
        success: function(res) {
          if (res.tapIndex === 0) {
            that.takePhoto(side);
          } else {
            that.chooseFromAlbum(side);
          }
        }
      });
    },

    takePhoto(side) {
      var that = this;
      uni.chooseMedia({
        count: 1,
        mediaType: ['image'],
        sourceType: ['camera'],
        camera: 'front',
        sizeType: ['compressed'],
        success: function(res) {
          that.onImageSelected(side, res.tempFiles[0].tempFilePath);
        },
        fail: function(err) {
          if (err.errMsg && err.errMsg.indexOf('cancel') === -1) {
            uni.chooseImage({
              count: 1,
              sourceType: ['camera'],
              sizeType: ['compressed'],
              success: function(res2) {
                that.onImageSelected(side, res2.tempFilePaths[0]);
              }
            });
          }
        }
      });
    },

    chooseFromAlbum(side) {
      var that = this;
      uni.chooseImage({
        count: 1,
        sourceType: ['album'],
        sizeType: ['compressed'],
        success: function(res) {
          that.onImageSelected(side, res.tempFilePaths[0]);
        }
      });
    },

    onImageSelected(side, path) {
      if (side === 'a') {
        this.imageA = path;
      } else {
        this.imageB = path;
      }
      this.tipText = '照片已选择，点击「开始比对」测测缘分';
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
            var ctx = uni.createCanvasContext('coupleCanvas', that);
            ctx.clearRect(0, 0, newW, newH);
            ctx.drawImage(imgPath, 0, 0, newW, newH);
            ctx.draw(false, function() {
              setTimeout(function() {
                uni.canvasToTempFilePath({
                  canvasId: 'coupleCanvas',
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

    uploadImage(imgPath, side) {
      return new Promise(function(resolve, reject) {
        var fileName = 'couple_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9) + '.jpg';
        var cloudPath = 'star_user_pic/' + fileName;

        uniCloud.uploadFile({
          filePath: imgPath,
          cloudPath: cloudPath,
          success: function(uploadRes) {
            var url = 'https://env-00jy674l53ts.normal.cloudstatic.cn/' + cloudPath;
            resolve(url);
          },
          fail: function(err) {
            reject(err);
          }
        });
      });
    },

    checkUploadedImage(url) {
      return mediaCheckUtil.check(url, this.$app);
    },

    startCompare() {
      var that = this;

      if (!that.imageA || !that.imageB) {
        uni.showToast({ title: '请上传两张照片', icon: 'none' });
        return;
      }
      if (that.loading) return;

      if (that.score < 5) {
        that.pendingAction = 'compare';
        that.showScoreModal = true;
        return;
      }

      that.loading = true;
      that.tipText = '正在处理，请稍候...';

      var compressedA, compressedB;

      that.compressImage(that.imageA, function(compA) {
        compressedA = compA;
        that.compressImage(that.imageB, function(compB) {
          compressedB = compB;

          Promise.all([
            that.uploadImage(compressedA, 'a'),
            that.uploadImage(compressedB, 'b')
          ]).then(function(urls) {
            that.uploadedUrlA = urls[0];
            that.uploadedUrlB = urls[1];
            return Promise.all([
              that.checkUploadedImage(urls[0]),
              that.checkUploadedImage(urls[1])
            ]).then(function() {
              return urls;
            });
          }).then(function(urls) {
            that.callCompare(urls[0], urls[1]);
          }).catch(function(err) {
            console.error('上传或审核失败:', err);
            that.loading = false;
            that.tipText = '上传失败，请重试';
            uni.showModal({
              title: '图片审核失败',
              content: err.message || '图片暂时无法通过安全校验，请更换照片',
              showCancel: false
            });
          });
        });
      });
    },

    callCompare(urlA, urlB) {
      var that = this;
      that.tipText = '正在比对人脸...';

      uniCloud.callFunction({
        name: 'faceSearch',
        data: {
          action: 'compare',
          image_a_url: urlA,
          image_b_url: urlB
        },
        success: function(res) {
          var result = res.result || {};
          if (result.code !== 0) {
            that.loading = false;
            that.tipText = '上传两张正脸照，测测你们的夫妻相指数';
            uni.showModal({
              title: '比对失败',
              content: result.message || '请重试',
              showCancel: false
            });
            return;
          }

          var data = result.data || {};

          let scoreUrl = that.$app.apiPath.common.useScore;
          that.$app.post(scoreUrl, { score: 5 }).then(function(res2) {
            if (res2.code == 200) {
              that.getScore();
            }
          });

          that.loading = false;
          that.tipText = '上传两张正脸照，测测你们的夫妻相指数';

          try {
            uni.setStorageSync('coupleResult', data);
            uni.setStorageSync('couplePhotoA', that.uploadedUrlA || '');
            uni.setStorageSync('couplePhotoB', that.uploadedUrlB || '');
          } catch (e) {
            console.error('存储结果失败:', e);
          }

          uni.navigateTo({
            url: '/pages/couple-result/couple-result'
          });
        },
        fail: function(err) {
          console.error('云函数调用失败:', err);
          that.loading = false;
          that.tipText = '上传两张正脸照，测测你们的夫妻相指数';
          uni.showModal({
            title: '服务异常',
            content: '云服务连接失败，请检查网络后重试',
            showCancel: false
          });
        }
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
  background: linear-gradient(180deg, #fff0f5 0%, #f0f0ff 40%, #fafafa 100%);
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
  background: linear-gradient(135deg, #ff6b9d 0%, #c471ed 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8rpx 32rpx rgba(196, 113, 237, 0.3);
  margin-bottom: 20rpx;
}

.logo-icon { font-size: 64rpx; }

.title {
  font-size: 48rpx;
  font-weight: 800;
  color: #c471ed;
  letter-spacing: 2rpx;
  margin-bottom: 12rpx;
}

.subtitle {
  font-size: 24rpx;
  color: #999;
  letter-spacing: 1rpx;
}

.upload-area {
  display: flex;
  align-items: center;
  gap: 16rpx;
  margin-bottom: 40rpx;
}

.upload-card {
  width: 280rpx;
  height: 340rpx;
  background: #fff;
  border-radius: 32rpx;
  overflow: hidden;
  position: relative;
  box-shadow: 0 8rpx 32rpx rgba(196, 113, 237, 0.15);
}

.preview-img {
  width: 100%;
  height: 100%;
}

.upload-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16rpx;
}

.upload-icon-circle {
  width: 80rpx;
  height: 80rpx;
  background: linear-gradient(135deg, #ffe0f0 0%, #e8d0ff 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-icon { font-size: 40rpx; }

.upload-text {
  font-size: 26rpx;
  color: #666;
  font-weight: 600;
}

.upload-hint {
  font-size: 22rpx;
  color: #999;
}

.rechoose-badge {
  position: absolute;
  bottom: 16rpx;
  right: 16rpx;
  background: rgba(0,0,0,0.5);
  padding: 8rpx 20rpx;
  border-radius: 24rpx;
}

.rechoose-text {
  color: #fff;
  font-size: 22rpx;
}

.vs-divider {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
}

.vs-line {
  width: 4rpx;
  height: 60rpx;
  background: linear-gradient(180deg, transparent, #c471ed, transparent);
  border-radius: 2rpx;
}

.vs-circle {
  width: 56rpx;
  height: 56rpx;
  background: linear-gradient(135deg, #ff6b9d 0%, #c471ed 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4rpx 16rpx rgba(196, 113, 237, 0.4);
}

.vs-text {
  font-size: 22rpx;
  font-weight: 800;
  color: #fff;
}

.score-wrap {
  margin-bottom: 20rpx;
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

.score-text {
  font-size: 24rpx;
  color: #666;
  font-weight: 600;
}

.score-tips {
  padding: 10rpx 20rpx;
  background: #f5eaff;
  border-radius: 20rpx;
}

.tips-text { font-size: 22rpx; color: #c471ed; }

.tip-wrap {
  margin-bottom: 30rpx;
}

.tip-text {
  font-size: 24rpx;
  color: #999;
}

.compare-btn {
  width: 560rpx;
  height: 96rpx;
  background: linear-gradient(135deg, #ff6b9d 0%, #c471ed 100%);
  color: #fff;
  font-size: 32rpx;
  font-weight: 700;
  border-radius: 48rpx;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8rpx 32rpx rgba(196, 113, 237, 0.35);
  margin-bottom: 30rpx;
}

.compare-btn[disabled] {
  background: #ddd;
  box-shadow: none;
  color: #999;
}

.footer {
  margin-top: 20rpx;
}

.privacy-badge {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.privacy-icon { font-size: 24rpx; }

.privacy-text {
  font-size: 22rpx;
  color: #bbb;
}

.pk-link {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8rpx;
  margin-top: 16rpx;
  padding: 12rpx 24rpx;
  background: linear-gradient(135deg, #ffebee 0%, #fce4ec 100%);
  border-radius: 28rpx;
}

.pk-link-icon { font-size: 24rpx; }

.pk-link-text {
  font-size: 22rpx;
  color: #ff4757;
  font-weight: 600;
}

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
.score-modal-item-score { font-size: 30rpx; font-weight: 700; color: #c471ed; flex-shrink: 0; margin-left: 16rpx; }

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
  background: linear-gradient(135deg, #c471ed, #ff6b9d);
  color: #fff;
}

.ad-btn-modal {
  background: #f5f5f5;
  color: #666;
}
</style>
