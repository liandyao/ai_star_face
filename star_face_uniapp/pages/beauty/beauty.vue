<template>
  <view class="container">
    <view class="header">
      <view class="logo-wrap">
        <text class="logo-icon">🔥</text>
      </view>
      <text class="title">颜值暴击</text>
      <text class="subtitle">上传照片，AI鉴定你的颜值等级</text>
    </view>

    <view class="image-card" @click="showChooseAction">
      <image v-if="hasImage" class="preview-img" :src="tempImagePath" mode="aspectFill"></image>
      <view v-if="!hasImage" class="upload-placeholder">
        <view class="upload-icon-circle">
          <text class="upload-icon">📸</text>
        </view>
        <text class="upload-text">点击上传你的照片</text>
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

    <view class="action-btns" v-if="!hasImage">
      <view class="action-btn camera-btn" @click="takePhoto">
        <text class="action-btn-icon">🤳</text>
        <text class="action-btn-text">自拍</text>
      </view>
      <view class="action-btn album-btn" @click="chooseFromAlbum">
        <text class="action-btn-icon">🖼️</text>
        <text class="action-btn-text">相册选择</text>
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

    <button class="compare-btn" :disabled="loading || !hasImage" @click="startDetect">
      <text v-if="loading">⏳ 正在鉴定中...</text>
      <text v-else>🔥 开始鉴定</text>
    </button>

    <view class="footer">
      <view class="privacy-badge">
        <text class="privacy-icon">🔒</text>
        <text class="privacy-text">人脸数据仅用于本次鉴定，不做他用，结果仅供娱乐！</text>
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

    <canvas canvas-id="beautyCanvas" :style="{width: canvasWidth + 'px', height: canvasHeight + 'px', position: 'fixed', left: '-9999px', top: '-9999px'}"></canvas>
  </view>
</template>

<script>
import AdUtil from '@/common/AdUtil.js';
import shareUtil from '@/common/shareUtil.js';
import mediaCheckUtil from '@/common/mediaCheckUtil.js';

export default {
  data() {
    return {
      tempImagePath: '',
      hasImage: false,
      loading: false,
      score: 0,
      canvasWidth: 800,
      canvasHeight: 800,
      uploadedPhotoUrl: '',
      showScoreModal: false,
      pendingAction: ''
    }
  },

  onLoad(op) {
    let shareId = op ? op.shareId : '';
    const app = getApp();
    if (app.globalData.loginPromise) {
      app.globalData.loginPromise.then(() => { this.getScore(); }).catch(() => { this.getScore(); });
    } else {
      this.getScore();
    }
    this.initAd();
    shareUtil.handleShareBonus(this.$app, shareId);
  },

  onShow() {
    if (uni.getStorageSync("openid")) { this.getScore(); }
  },

  onShareAppMessage() {
    return shareUtil.getShareConfig('颜值暴击 - AI鉴定你的颜值等级', '/pages/beauty/beauty');
  },

  onShareTimeline() {
    return shareUtil.getTimelineConfig('颜值暴击 - AI鉴定你的颜值等级');
  },

  methods: {
    getScore() {
      this.$app.post(this.$app.apiPath.common.userSurplus).then(res => {
        if (res.code == 200) this.score = res.data;
      });
    },

    initAd() {
      let that = this;
      AdUtil.rewarded.load(() => {
        that.$app.post(that.$app.apiPath.common.videoPlus).then(res => {
          if (res.code == 200) { that.score += 5; uni.showToast({ title: '积分+5', icon: 'success' }); }
          that.tryPendingAction();
        }, () => { that.score += 5; that.tryPendingAction(); });
      });
    },

    tryPendingAction() {
      var that = this;
      if (that.pendingAction === 'detect') {
        that.pendingAction = '';
        setTimeout(function() { that.startDetect(); }, 500);
      }
    },

    showAd() {
      uni.showLoading({ title: '正在加载...' });
      AdUtil.rewarded.show();
      setTimeout(() => { uni.hideLoading(); }, 2000);
    },

    showChooseAction() {
      var that = this;
      uni.showActionSheet({
        itemList: ['🤳 自拍', '🖼️ 从相册选择'],
        success: function(res) {
          if (res.tapIndex === 0) that.takePhoto();
          else that.chooseFromAlbum();
        }
      });
    },

    takePhoto() {
      var that = this;
      uni.chooseMedia({
        count: 1, mediaType: ['image'], sourceType: ['camera'], camera: 'front', sizeType: ['compressed'],
        success: function(res) { that.onImageSelected(res.tempFiles[0].tempFilePath); },
        fail: function(err) {
          if (err.errMsg && err.errMsg.indexOf('cancel') === -1) {
            uni.chooseImage({ count: 1, sourceType: ['camera'], sizeType: ['compressed'],
              success: function(res2) { that.onImageSelected(res2.tempFilePaths[0]); }
            });
          }
        }
      });
    },

    chooseFromAlbum() {
      var that = this;
      uni.chooseImage({ count: 1, sourceType: ['album'], sizeType: ['compressed'],
        success: function(res) { that.onImageSelected(res.tempFilePaths[0]); }
      });
    },

    onImageSelected(path) {
      this.tempImagePath = path;
      this.hasImage = true;
      uni.showToast({ title: '照片已选择', icon: 'success', duration: 1500 });
    },

    compressImage(imgPath, callback) {
      var that = this;
      uni.getImageInfo({
        src: imgPath,
        success: function(info) {
          var w = info.width, h = info.height, maxSide = 800;
          if (w <= maxSide && h <= maxSide) {
            uni.compressImage({ src: imgPath, quality: 80,
              success: function(r) { callback(r.tempFilePath); },
              fail: function() { callback(imgPath); }
            });
            return;
          }
          var ratio = Math.min(maxSide / w, maxSide / h);
          var newW = Math.round(w * ratio), newH = Math.round(h * ratio);
          that.canvasWidth = newW; that.canvasHeight = newH;
          setTimeout(function() {
            var ctx = uni.createCanvasContext('beautyCanvas', that);
            ctx.clearRect(0, 0, newW, newH);
            ctx.drawImage(imgPath, 0, 0, newW, newH);
            ctx.draw(false, function() {
              setTimeout(function() {
                uni.canvasToTempFilePath({ canvasId: 'beautyCanvas', x: 0, y: 0, width: newW, height: newH,
                  destWidth: newW, destHeight: newH, quality: 0.8, fileType: 'jpg',
                  success: function(r) { callback(r.tempFilePath); },
                  fail: function() {
                    uni.compressImage({ src: imgPath, quality: 80,
                      success: function(r2) { callback(r2.tempFilePath); },
                      fail: function() { callback(imgPath); }
                    });
                  }
                }, that);
              }, 300);
            });
          }, 100);
        },
        fail: function() { callback(imgPath); }
      });
    },

    startDetect() {
      var that = this;
      if (!that.hasImage) { uni.showToast({ title: '请先上传照片', icon: 'none' }); return; }
      if (that.loading) return;
      if (that.score < 5) { that.pendingAction = 'detect'; that.showScoreModal = true; return; }

      that.loading = true;
      that.compressImage(that.tempImagePath, function(compPath) {
        var fileName = 'beauty_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9) + '.jpg';
        var cloudPath = 'star_user_pic/' + fileName;
        uniCloud.uploadFile({
          filePath: compPath, cloudPath: cloudPath,
          success: function(uploadRes) {
            that.uploadedPhotoUrl = 'https://env-00jy674l53ts.normal.cloudstatic.cn/' + cloudPath;
            that.checkUploadedImage(that.uploadedPhotoUrl, function() {
              that.readImageAndDetect(compPath);
            });
          },
          fail: function() {
            that.loading = false;
            uni.showToast({ title: '上传失败，请重试', icon: 'none' });
          }
        });
      });
    },

    checkUploadedImage(url, successCallback) {
      var that = this;
      mediaCheckUtil.check(url, that.$app).then(function() {
        successCallback();
      }).catch(function(err) {
        that.loading = false;
        uni.showModal({ title: '图片审核失败', content: err.message || '图片暂时无法通过安全校验，请更换照片', showCancel: false });
      });
    },

    readImageAndDetect(imgPath) {
      var that = this;
      try {
        var fs = uni.getFileSystemManager();
        fs.readFile({
          filePath: imgPath, encoding: 'base64',
          success: function(fRes) {
            if (!fRes.data) { that.loading = false; uni.showToast({ title: '图片读取失败', icon: 'none' }); return; }
            that.callCloudDetect(fRes.data);
          },
          fail: function() { that.loading = false; uni.showToast({ title: '图片转换失败', icon: 'none' }); }
        });
      } catch (e) { that.loading = false; uni.showToast({ title: '图片处理异常', icon: 'none' }); }
    },

    callCloudDetect(base64) {
      var that = this;
      uniCloud.callFunction({
        name: 'faceSearch',
        data: { action: 'beautyDetect', image: base64 },
        success: function(res) {
          var result = res.result || {};
          if (result.code !== 0) {
            that.loading = false;
            uni.showModal({ title: '鉴定失败', content: result.message || '请重试', showCancel: false });
            return;
          }
          var data = result.data || {};
          if (!data.hasFace) {
            that.loading = false;
            uni.showModal({ title: '未检测到人脸', content: '请确保照片中包含清晰可见的正面人脸', showCancel: false });
            return;
          }

          that.$app.post(that.$app.apiPath.common.useScore, { score: 5 }).then(function(res2) {
            if (res2.code == 200) that.getScore();
          });

          that.loading = false;
          try {
            uni.setStorageSync('beautyResult', data);
            uni.setStorageSync('beautyPhotoUrl', that.uploadedPhotoUrl || '');
          } catch (e) {}
          uni.navigateTo({ url: '/pages/beauty-result/beauty-result' });
        },
        fail: function() {
          that.loading = false;
          uni.showModal({ title: '服务异常', content: '云服务连接失败，请检查网络后重试', showCancel: false });
        }
      });
    }
  }
}
</script>

<style scoped>
.container {
  display: flex; flex-direction: column; align-items: center;
  padding: 40rpx 30rpx; min-height: 100vh; box-sizing: border-box;
  background: linear-gradient(180deg, #fff8e1 0%, #fff3e0 40%, #fafafa 100%);
}
.header { display: flex; flex-direction: column; align-items: center; margin-bottom: 40rpx; }
.logo-wrap {
  width: 120rpx; height: 120rpx;
  background: linear-gradient(135deg, #ff9500 0%, #ff5e3a 100%);
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  box-shadow: 0 8rpx 32rpx rgba(255, 149, 0, 0.3); margin-bottom: 20rpx;
}
.logo-icon { font-size: 64rpx; }
.title { font-size: 48rpx; font-weight: 800; color: #ff9500; letter-spacing: 2rpx; margin-bottom: 12rpx; }
.subtitle { font-size: 24rpx; color: #999; letter-spacing: 1rpx; }

.image-card {
  width: 500rpx; height: 500rpx; background: #fff; border-radius: 32rpx;
  overflow: hidden; position: relative; margin-bottom: 40rpx;
  box-shadow: 0 8rpx 32rpx rgba(255, 149, 0, 0.15);
}
.preview-img { width: 100%; height: 100%; }
.upload-placeholder {
  width: 100%; height: 100%; display: flex; flex-direction: column;
  align-items: center; justify-content: center; gap: 16rpx;
}
.upload-icon-circle {
  width: 100rpx; height: 100rpx;
  background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
}
.upload-icon { font-size: 48rpx; }
.upload-text { font-size: 28rpx; color: #666; font-weight: 600; }
.upload-tips { display: flex; flex-direction: column; gap: 8rpx; margin-top: 8rpx; }
.upload-tip-item { font-size: 22rpx; color: #999; }
.rechoose-btn {
  position: absolute; bottom: 20rpx; right: 20rpx;
  background: rgba(0,0,0,0.5); padding: 10rpx 24rpx; border-radius: 28rpx;
  display: flex; align-items: center; gap: 6rpx;
}
.rechoose-icon { font-size: 22rpx; }
.rechoose-text { font-size: 22rpx; color: #fff; }

.action-btns { display: flex; gap: 30rpx; margin-bottom: 30rpx; }
.action-btn {
  display: flex; align-items: center; gap: 10rpx;
  padding: 16rpx 36rpx; background: #fff; border-radius: 40rpx;
  box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.06);
}
.action-btn-icon { font-size: 32rpx; }
.action-btn-text { font-size: 26rpx; color: #666; font-weight: 600; }

.score-wrap { margin-bottom: 20rpx; display: flex; align-items: center; gap: 16rpx; }
.score-badge {
  display: flex; align-items: center; gap: 8rpx;
  background: #fff; padding: 12rpx 28rpx; border-radius: 36rpx;
  box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.06);
}
.score-icon { font-size: 28rpx; }
.score-text { font-size: 24rpx; color: #666; font-weight: 600; }
.score-tips { padding: 10rpx 20rpx; background: #fff3e0; border-radius: 20rpx; }
.tips-text { font-size: 22rpx; color: #ff9500; }

.compare-btn {
  width: 560rpx; height: 96rpx;
  background: linear-gradient(135deg, #ff9500 0%, #ff5e3a 100%);
  color: #fff; font-size: 32rpx; font-weight: 700; border-radius: 48rpx; border: none;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 8rpx 32rpx rgba(255, 149, 0, 0.35); margin-bottom: 30rpx;
}
.compare-btn[disabled] { background: #ddd; box-shadow: none; color: #999; }

.footer { margin-top: 20rpx; }
.privacy-badge { display: flex; align-items: center; gap: 8rpx; }
.privacy-icon { font-size: 24rpx; }
.privacy-text { font-size: 22rpx; color: #bbb; }

.score-modal { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.4); z-index: 1001; display: flex; align-items: center; justify-content: center; }
.score-modal-panel { width: 600rpx; background: #fff; border-radius: 28rpx; padding: 40rpx 36rpx; }
.score-modal-title { font-size: 34rpx; font-weight: 700; color: #333; text-align: center; display: block; margin-bottom: 30rpx; }
.score-modal-body { display: flex; flex-direction: column; gap: 20rpx; margin-bottom: 30rpx; }
.score-modal-item { display: flex; align-items: center; padding: 20rpx; background: #fafafa; border-radius: 16rpx; }
.score-modal-item-icon { font-size: 40rpx; flex-shrink: 0; }
.score-modal-item-info { flex: 1; margin-left: 16rpx; display: flex; flex-direction: column; gap: 4rpx; }
.score-modal-item-name { font-size: 28rpx; font-weight: 700; color: #333; }
.score-modal-item-desc { font-size: 22rpx; color: #999; }
.score-modal-item-score { font-size: 30rpx; font-weight: 700; color: #ff9500; flex-shrink: 0; margin-left: 16rpx; }
.score-modal-btns { display: flex; gap: 20rpx; }
.score-modal-btn { flex: 1; height: 80rpx; line-height: 80rpx; font-size: 28rpx; font-weight: 700; border-radius: 40rpx; border: none; padding: 0; margin: 0; }
.share-btn-modal { background: linear-gradient(135deg, #ff9500, #ff5e3a); color: #fff; }
.ad-btn-modal { background: #f5f5f5; color: #666; }
</style>
