<template>
  <view class="container">
    <view class="header">
      <view class="logo-wrap">
        <text class="logo-icon">🌟</text>
      </view>
      <text class="title">明星脸比对</text>
      <text class="subtitle">上传正脸照/侧脸照，发现你的明星脸</text>
    </view>

    <view class="image-card" @click="showChooseAction">
      <image v-if="hasImage" class="preview-img" :src="tempImagePath" mode="aspectFill" @click.stop=""></image>
      <view v-if="!hasImage" class="upload-placeholder">
        <view class="upload-icon-circle">
          <text class="upload-icon">📸</text>
        </view>
        <text class="upload-text">点击上传正脸照/侧脸照</text>
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
      <view class="score-tips" @click="showScoreTips">
        <text class="tips-text">如何获取积分？</text>
      </view>
    </view>


    <button class="compare-btn" :disabled="loading || !hasImage" @click="startCompare">
      <text v-if="loading">⏳ 正在比对中...</text>
      <text v-else-if="score < 5">💎 积分不足(需要5积分)</text>
      <text v-else>🔍 开始比对(消耗5积分)</text>
    </button>

    <view class="footer">
      <view class="privacy-badge">
        <text class="privacy-icon">🔒</text>
        <text class="privacy-text">人脸数据仅用于本次比对，不做他用</text>
      </view>
      <text class="disclaimer-text">比对结果仅供娱乐</text>
    </view>

    <view class="float-ball" @click="toggleFeatureMenu">
      <text class="float-ball-icon">🎮</text>
      <text class="float-ball-text">更多玩法</text>
    </view>
    <view class="feature-menu" v-if="showFeatureMenu" @click="closeFeatureMenu">
      <view class="feature-menu-panel" @click.stop="">
        <view class="feature-menu-item" @click="goCrossGender">
          <view class="feature-menu-icon cross-bg">
            <text class="feature-menu-emoji">🌈</text>
          </view>
          <view class="feature-menu-info">
            <text class="feature-menu-name">跨性别撞脸</text>
            <text class="feature-menu-desc">看看异性明星中谁最像你</text>
          </view>
          <text class="feature-menu-arrow">›</text>
        </view>
        <view class="feature-menu-divider"></view>
        <view class="feature-menu-item" @click="goAbout">
          <view class="feature-menu-icon about-bg">
            <text class="feature-menu-emoji">💡</text>
          </view>
          <view class="feature-menu-info">
            <text class="feature-menu-name">关于</text>
            <text class="feature-menu-desc">积分规则与玩法介绍</text>
          </view>
          <text class="feature-menu-arrow">›</text>
        </view>
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
              <text class="score-modal-item-desc">好友打开后双方各得5积分</text>
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

    <!-- 用于图片压缩的隐藏canvas -->
    <canvas canvas-id="resizeCanvas" :style="{width: canvasWidth + 'px', height: canvasHeight + 'px', position: 'fixed', left: '-9999px', top: '-9999px'}"></canvas>
  </view>
</template>

<script>
import AdUtil from '@/common/AdUtil.js';
import shareUtil from '@/common/shareUtil.js';

export default {
  // 页面数据定义
  data() {
    return {
      tempImagePath: '',           // 用户选择的图片临时路径
      hasImage: false,             // 是否已选择图片
      loading: false,              // 是否正在处理中
      tipText: '让生活多一点乐趣',  // 提示文本
      uploadedPhotoUrl: '',        // 上传到云存储后的图片URL，用于结果页展示和分享
      canvasWidth: 800,            // canvas宽度，动态设置
      canvasHeight: 800,           // canvas高度，动态设置
      score: 0,
      isFirstShow: true,
      showFeatureMenu: false,
      showScoreModal: false
    }
  },

  // 页面加载时触发
  onLoad(op) {
    let shareId = op ? op.shareId : '';
    console.info('是否分享:', shareId);
    
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
    // 页面显示时刷新积分（跳过首次，因为onLoad已经处理）
    if (!this.isFirstShow && uni.getStorageSync("openid")) {
      this.getScore();
    }
    this.isFirstShow = false;
  },

  // 分享给朋友时的配置
  onShareAppMessage() {
    return shareUtil.getShareConfig('明星脸比对 - 看看你和哪位明星最像', '/pages/index/index');
  },

  onShareTimeline() {
    return shareUtil.getTimelineConfig('明星脸比对 - 看看你和哪位明星最像');
  },

  methods: {
    // 微信小程序登录
    login() {
      return this.$app.miniAppLogin();
    },

    // 查询用户积分
    getScore() {
      let url = this.$app.apiPath.common.userSurplus;
      //console.info('===>', url);
      this.$app.post(url).then(res => {
        if (res.code == 200) {
          this.score = res.data;
          console.info('后台获取积分', this.score);
        }
      });
    },

    // 显示积分获取提示
    showScoreTips() {
      this.showScoreModal = true
    },

    // 初始化激励视频广告
    initAd() {
      let that = this;
      AdUtil.rewarded.load(() => {
        let url = that.$app.apiPath.common.videoPlus;
        that.$app.post(url).then(res => {
          if (res.code == 200) {
            that.score = that.score + 5;
            console.log('成功修改');
            uni.showToast({
              title: '积分+5',
              icon: 'success'
            });
          } else {
            console.log('后台报错500');
          }
        }, err => {
          console.log('后台报错...');
          that.score = that.score + 5;
        });
      });
    },

    // 显示广告获取积分
    showAd() {
      uni.showLoading({
        title: '正在加载...'
      });
      AdUtil.rewarded.show();
      setTimeout(() => {
        uni.hideLoading();
      }, 2000);
    },

    // 显示选择图片方式的底部弹窗
    showChooseAction() {
      var that = this
      uni.showActionSheet({
        itemList: ['🤳 自拍', '🖼️ 从相册选择'],
        success: function(res) {
          if (res.tapIndex === 0) {
            that.takePhoto()
          } else {
            that.chooseFromAlbum()
          }
        }
      })
    },

    // 调用相机拍照
    takePhoto() {
      var that = this
      uni.chooseMedia({
        count: 1,
        mediaType: ['image'],
        sourceType: ['camera'],
        camera: 'front',
        sizeType: ['compressed'],
        success: function(res) {
          var tempFile = res.tempFiles[0]
          that.onImageSelected(tempFile.tempFilePath)
        },
        fail: function(err) {
          // 如果不是用户取消，则降级使用 chooseImage 作为兼容方案
          if (err.errMsg && err.errMsg.indexOf('cancel') === -1) {
            uni.chooseImage({
              count: 1,
              sourceType: ['camera'],
              sizeType: ['compressed'],
              success: function(res2) {
                that.onImageSelected(res2.tempFilePaths[0])
              },
              fail: function() {
                uni.showToast({ title: '拍照失败', icon: 'none' })
              }
            })
          }
        }
      })
    },

    // 从相册选择图片
    chooseFromAlbum() {
      var that = this
      uni.chooseImage({
        count: 1,
        sourceType: ['album'],
        sizeType: ['compressed'],
        success: function(res) {
          that.onImageSelected(res.tempFilePaths[0])
        },
        fail: function(err) {
          // 如果不是用户取消，则显示错误提示
          if (err.errMsg && err.errMsg.indexOf('cancel') === -1) {
            uni.showToast({ title: '选择图片失败', icon: 'none' })
          }
        }
      })
    },

    // 图片选择成功后的处理
    onImageSelected(path) {
      this.tempImagePath = path
      this.hasImage = true
      this.tipText = '照片已选择，点击「开始比对」看看结果'
      uni.showToast({ title: '照片已选择', icon: 'success', duration: 1500 })
    },

    // 开始比对：检查积分后启动压缩流程
    startCompare() {
      var that = this

      if (!that.hasImage) {
        uni.showToast({ title: '请先上传照片', icon: 'none' })
        return
      }
      if (that.loading) return

      // 检查积分
      if (that.score < 5) {
        that.showScoreModal = true
        return
      }

      that.loading = true
      that.tipText = '正在处理，请稍候...'
      that.compressImage(that.tempImagePath)
    },

    // 压缩图片：使用uni.compressImage API压缩，保持原始宽高比，质量80，节省云存储资源
    compressImage(imgPath) {
      var that = this
      
      // 先获取图片信息
      uni.getImageInfo({
        src: imgPath,
        success: function(info) {
          var w = info.width
          var h = info.height
          var maxSide = 800

          // 如果图片尺寸已经在限制范围内，则只需要压缩质量，不使用canvas避免比例问题
          if (w <= maxSide && h <= maxSide) {
            uni.compressImage({
              src: imgPath,
              quality: 80,
              success: function(compressRes) {
                that.onImageCompressed(compressRes.tempFilePath)
              },
              fail: function() {
                that.onImageCompressed(imgPath)
              }
            })
            return
          }

          // 图片过大，需要使用canvas进行尺寸压缩
          var ratio = Math.min(maxSide / w, maxSide / h)
          var newW = Math.round(w * ratio)
          var newH = Math.round(h * ratio)

          // 动态设置canvas尺寸，确保与图片比例一致
          that.canvasWidth = newW
          that.canvasHeight = newH

          // 等待canvas尺寸更新后再绘制
          setTimeout(function() {
            // 使用canvas进行等比例压缩，保持宽高比
            var ctx = uni.createCanvasContext('resizeCanvas', that)
            
            // 清空canvas
            ctx.clearRect(0, 0, newW, newH)
            // 绘制图片，保持原始宽高比
            ctx.drawImage(imgPath, 0, 0, newW, newH)
            
            ctx.draw(false, function() {
              setTimeout(function() {
                uni.canvasToTempFilePath({
                  canvasId: 'resizeCanvas',
                  x: 0,
                  y: 0,
                  width: newW,
                  height: newH,
                  destWidth: newW,
                  destHeight: newH,
                  quality: 0.8,
                  fileType: 'jpg',
                  success: function(canvasRes) {
                    that.onImageCompressed(canvasRes.tempFilePath)
                  },
                  fail: function() {
                    // canvas压缩失败，尝试质量压缩
                    uni.compressImage({
                      src: imgPath,
                      quality: 80,
                      success: function(compressRes) {
                        that.onImageCompressed(compressRes.tempFilePath)
                      },
                      fail: function() {
                        that.onImageCompressed(imgPath)
                      }
                    })
                  }
                }, that)
              }, 300)
            })
          }, 100)
        },
        fail: function() {
          // 获取图片信息失败则使用原图
          that.onImageCompressed(imgPath)
        }
      })
    },

    // 图片压缩完成后，上传到云存储
    onImageCompressed(compressedPath) {
      var that = this
      // 生成唯一文件名，避免冲突
      var fileName = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9) + '.jpg'
      var cloudPath = 'star_user_pic/' + fileName

      uniCloud.uploadFile({
        filePath: compressedPath,
        cloudPath: cloudPath,
        success: function(uploadRes) {
          // 支付宝云存储：文件权限为公共读时，直接拼接永久URL
          // 格式：https://环境ID.normal.cloudstatic.cn/文件路径
          that.uploadedPhotoUrl = 'https://env-00jy674l53ts.normal.cloudstatic.cn/' + cloudPath
          that.readImageAndSearch(compressedPath)
        },
        fail: function(err) {
          console.error('上传到云存储失败:', err)
          // 上传失败仍然继续比对，只是结果页无法显示用户照片
          that.readImageAndSearch(compressedPath)
        }
      })
    },

    // 读取压缩后的图片为base64，然后调用云函数进行人脸搜索
    readImageAndSearch(imgPath) {
      var that = this
      try {
        var fs = uni.getFileSystemManager()
        fs.readFile({
          filePath: imgPath,
          encoding: 'base64',
          success: function(fRes) {
            var base64 = fRes.data
            if (!base64) {
              that.resetState()
              uni.showToast({ title: '图片读取失败', icon: 'none' })
              return
            }

            that.tipText = '正在检测人脸...'
            that.callCloudSearch(base64)
          },
          fail: function(fErr) {
            console.error('base64失败:', fErr)
            that.resetState()
            uni.showToast({ title: '图片转换失败', icon: 'none' })
          }
        })
      } catch (e) {
        console.error('文件系统异常:', e)
        that.resetState()
        uni.showToast({ title: '图片处理异常', icon: 'none' })
      }
    },

    // 调用云函数进行人脸检测和搜索（带质量检测）
    callCloudSearch(base64) {
      var that = this

      uniCloud.callFunction({
        name: 'faceSearch',
        data: {
          action: 'detectAndSearch',
          image: base64
        },
        success: function(res) {
          var result = res.result || {}
          if (result.code !== 0) {
            that.resetState()
            uni.showModal({
              title: '操作失败',
              content: result.message || '请重试',
              showCancel: false
            })
            return
          }

          var data = result.data || {}
          var faceResult = data.faceResult || {}
          var searchResult = data.searchResult || []

          // 未检测到人脸
          if (!faceResult.hasFace) {
            that.resetState()
            uni.showModal({
              title: '未检测到人脸',
              content: '请确保照片中包含清晰可见的正面人脸',
              showCancel: false
            })
            return
          }

          // 照片质量不佳，询问用户是否继续
          if (data.needConfirm) {
            uni.showModal({
              title: '照片质量提示',
              content: faceResult.message + '，是否继续比对？',
              confirmText: '继续比对',
              cancelText: '重新选择',
              success: function(modalRes) {
                if (modalRes.confirm) {
                  that.callCloudSearchForce(base64)
                } else {
                  that.resetState()
                }
              }
            })
            return
          }

          that.handleSearchResult(searchResult)
        },
        fail: function(err) {
          console.error('云函数调用失败:', err)
          that.resetState()
          uni.showModal({
            title: '服务异常',
            content: '云服务连接失败，请检查网络后重试',
            showCancel: false
          })
        }
      })
    },

    // 强制调用云函数进行人脸搜索（跳过质量检测）
    callCloudSearchForce(base64) {
      var that = this
      that.tipText = '正在比对人脸...'

      uniCloud.callFunction({
        name: 'faceSearch',
        data: {
          action: 'search',
          image: base64
        },
        success: function(res) {
          var result = res.result || {}
          if (result.code !== 0) {
            that.resetState()
            uni.showModal({
              title: '比对失败',
              content: result.message || '请重试',
              showCancel: false
            })
            return
          }
          that.handleSearchResult(result.data || [])
        },
        fail: function(err) {
          console.error('云函数调用失败:', err)
          that.resetState()
          uni.showModal({
            title: '服务异常',
            content: '云服务连接失败，请检查网络后重试',
            showCancel: false
          })
        }
      })
    },

    // 处理云函数返回的搜索结果
    handleSearchResult(searchResult) {
      var that = this
      if (!searchResult || searchResult.length === 0) {
        that.resetState()
        uni.showModal({
          title: '未找到相似明星',
          content: '没有匹配到相似的明星，试试其他照片',
          showCancel: false
        })
        return
      }

      // 比对成功，调用后端扣分
      let openid = uni.getStorageSync("openid");
      let url = that.$app.apiPath.common.makePhoto + '?openid=' + openid;
      that.$app.post(url).then(res => {
        if (res.code == 200) {
          console.info('用户积分-5成功');
          that.getScore();
        }
      });

      that.loading = false
      that.tipText = '照片已选择，点击「开始比对」看看结果'
      try {
        // 将搜索结果和用户照片URL存储到本地，供结果页使用
        uni.setStorageSync('faceResults', searchResult)
        uni.setStorageSync('userPhotoUrl', that.uploadedPhotoUrl || '')
      } catch (e) {
        console.error('存储结果失败:', e)
      }
      uni.navigateTo({
        url: '/pages/result/result'
      })
    },

    // 重置页面状态
    resetState() {
      this.loading = false
      this.tipText = '照片已选择，点击「开始比对」看看结果'
    },

    goCrossGender() {
      this.showFeatureMenu = false
      uni.navigateTo({ url: '/pages/cross-gender/cross-gender' })
    },

    goAbout() {
      this.showFeatureMenu = false
      uni.navigateTo({ url: '/pages/about/about' })
    },

    toggleFeatureMenu() {
      this.showFeatureMenu = !this.showFeatureMenu
    },

    closeFeatureMenu() {
      this.showFeatureMenu = false
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
  background: linear-gradient(180deg, #fff0f5 0%, #fff5f8 40%, #fafafa 100%);
}

.header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 50rpx;
}

.logo-wrap {
  width: 120rpx;
  height: 120rpx;
  background: linear-gradient(135deg, #ff6b9d 0%, #ff4757 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8rpx 32rpx rgba(255, 107, 157, 0.3);
  margin-bottom: 20rpx;
}

.logo-icon { font-size: 64rpx; }

.title {
  font-size: 52rpx;
  font-weight: 800;
  color: #ff6b9d;
  letter-spacing: 2rpx;
  margin-bottom: 12rpx;
}

.subtitle {
  font-size: 26rpx;
  color: #999;
  letter-spacing: 1rpx;
}

.image-card {
  width: 520rpx;
  height: 600rpx;
  background: #fff;
  border-radius: 36rpx;
  box-shadow: 0 12rpx 40rpx rgba(255, 107, 157, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.preview-img {
  width: 100%;
  height: 100%;
  border-radius: 36rpx;
}

.rechoose-btn {
  position: absolute;
  bottom: 30rpx;
  right: 30rpx;
  background: rgba(0, 0, 0, 0.6);
  color: #fff;
  font-size: 24rpx;
  padding: 14rpx 28rpx;
  border-radius: 36rpx;
  display: flex;
  align-items: center;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.2);
}

.rechoose-icon { font-size: 28rpx; margin-right: 8rpx; }
.rechoose-text { font-size: 24rpx; }

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20rpx;
}

.upload-icon-circle {
  width: 140rpx;
  height: 140rpx;
  background: linear-gradient(135deg, #ff6b9d20 0%, #ff475720 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10rpx;
}

.upload-icon { font-size: 72rpx; opacity: 0.8; }
.upload-text { font-size: 32rpx; color: #ff6b9d; font-weight: 600; }

.upload-tips {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
}

.upload-tip-item { font-size: 22rpx; color: #bbb; }

.action-btns {
  width: 520rpx;
  display: flex;
  gap: 20rpx;
  margin-top: 30rpx;
}

.action-btn {
  flex: 1;
  height: 100rpx;
  border-radius: 24rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12rpx;
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.1);
}

.camera-btn {
  background: linear-gradient(135deg, #ff6b9d 0%, #ff4757 100%);
}

.album-btn {
  background: #fff;
  border: 3rpx solid #ff6b9d;
}

.action-btn-icon { font-size: 40rpx; }

.action-btn-text {
  font-size: 30rpx;
  font-weight: 700;
}

.camera-btn .action-btn-text { color: #fff; }
.album-btn .action-btn-text { color: #ff6b9d; }

.score-wrap {
  width: 520rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 30rpx 0;
  padding: 24rpx 30rpx;
  background: #fff;
  border-radius: 24rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.06);
}

.score-badge {
  display: flex;
  align-items: center;
  gap: 10rpx;
}

.score-icon { font-size: 32rpx; }
.score-text { font-size: 28rpx; color: #ff6b9d; font-weight: 700; }

.score-tips {
  padding: 10rpx 20rpx;
  background: #fff0f5;
  border-radius: 20rpx;
}

.tips-text { font-size: 22rpx; color: #ff6b9d; }

.tip-wrap {
  width: 520rpx;
  padding: 24rpx 30rpx;
  margin: 30rpx 0;
  background: #fff;
  border-radius: 24rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.06);
}

.tip-text { font-size: 26rpx; color: #666; text-align: center; line-height: 1.6; }

.compare-btn {
  width: 520rpx;
  height: 100rpx;
  background: linear-gradient(135deg, #ff6b9d 0%, #ff4757 100%);
  color: #fff;
  font-size: 36rpx;
  font-weight: 700;
  border-radius: 50rpx;
  border: none;
  box-shadow: 0 12rpx 32rpx rgba(255, 71, 87, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 20rpx;
}

.compare-btn[disabled] {
  background: #ddd;
  box-shadow: none;
  color: #999;
}

.footer { margin-top: 50rpx; display: flex; flex-direction: column; align-items: center; gap: 12rpx; }

.privacy-badge {
  display: flex;
  align-items: center;
  padding: 16rpx 28rpx;
  background: #f5f5f5;
  border-radius: 36rpx;
}

.privacy-icon { font-size: 24rpx; margin-right: 10rpx; }
.privacy-text { font-size: 20rpx; color: #999; }

.disclaimer-text { font-size: 20rpx; color: #bbb; }

.float-ball {
  position: fixed;
  right: 10rpx;
  top: 100rpx;
  padding: 6rpx 14rpx 6rpx 18rpx;
  border-radius: 50rpx;
  background: linear-gradient(135deg, #ff6b9d 0%, #c471ed 100%);
  box-shadow: 0 8rpx 30rpx rgba(255, 107, 157, 0.5);
  display: flex;
  align-items: center;
  gap: 8rpx;
  z-index: 999;
}

.float-ball-icon { font-size: 30rpx; }

.float-ball-text { font-size: 22rpx; color: #fff; font-weight: 700; white-space: nowrap; }

.feature-menu {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 1000;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 200rpx;
}

.feature-menu-panel {
  width: 600rpx;
  background: #fff;
  border-radius: 28rpx;
  padding: 16rpx 0;
  box-shadow: 0 16rpx 60rpx rgba(0, 0, 0, 0.2);
}

.feature-menu-item {
  display: flex;
  align-items: center;
  padding: 28rpx 32rpx;
}

.feature-menu-icon {
  width: 72rpx;
  height: 72rpx;
  border-radius: 18rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.about-bg {
  background: linear-gradient(135deg, #fff5e0 0%, #ffe8d0 100%);
}

.cross-bg {
  background: linear-gradient(135deg, #e0e8ff 0%, #d0d8ff 100%);
}

.feature-menu-emoji { font-size: 36rpx; }

.feature-menu-info {
  flex: 1;
  margin-left: 20rpx;
  display: flex;
  flex-direction: column;
  gap: 6rpx;
}

.feature-menu-name {
  font-size: 30rpx;
  font-weight: 700;
  color: #333;
}

.feature-menu-desc {
  font-size: 22rpx;
  color: #999;
}

.feature-menu-arrow {
  font-size: 36rpx;
  color: #ccc;
  font-weight: 300;
  margin-left: 10rpx;
}

.feature-menu-divider {
  height: 1rpx;
  background: #f0f0f0;
  margin: 0 32rpx;
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
.score-modal-item-score { font-size: 30rpx; font-weight: 700; color: #ff6b9d; flex-shrink: 0; margin-left: 16rpx; }

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
  background: linear-gradient(135deg, #ff6b9d, #c471ed);
  color: #fff;
}

.ad-btn-modal {
  background: #f5f5f5;
  color: #666;
}
</style>
