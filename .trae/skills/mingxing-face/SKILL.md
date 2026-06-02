---
name: "mingxing-face"
description: "明星脸比对小程序项目上下文技能。当用户在此项目中开发、调试、修改功能时调用，提供项目架构、技术栈、关键文件、接口规范、业务逻辑等完整上下文信息。"
---

# 明星脸比对 - 项目上下文

## 项目概览

- **项目名称**：明星脸比对（微信小程序）
- **项目路径**：`d:\03project\00小程序\mingxing_face`
- **前端框架**：UniApp (Vue 2) 微信小程序
- **后端技术**：uniCloud 云函数 + 腾讯云 IAI SDK
- **管理后台**：Flask (app.py)，仅用于管理 IAI 明星数据，不处理业务逻辑
- **云存储**：支付宝云存储
- **数据**：3000+ 张明星人脸照片

## 核心架构

### 前端目录结构

```
star_face_uniapp/
├── common/
│   ├── AdUtil.js          # 广告封装（插屏广告 + 激励视频）
│   └── shareUtil.js       # 分享加分封装（handleShareBonus / getShareConfig / getTimelineConfig）
├── request/
│   └── request.js         # 网络请求封装，Vue.prototype.$app = request
├── pages/
│   ├── index/index.vue           # 首页 - 明星脸比对
│   ├── couple/couple.vue         # 夫妻相/闺蜜相比对
│   ├── cross-gender/cross-gender.vue  # 跨性别撞脸
│   ├── result/result.vue         # 明星脸比对结果页
│   ├── couple-result/couple-result.vue  # 夫妻相结果页
│   ├── cross-gender-result/cross-gender-result.vue  # 跨性别结果页
│   └── about/about.vue          # 关于页面（积分规则与玩法介绍）
├── static/tab/             # tabBar 图标
├── pages.json              # 页面路由 + tabBar 配置
└── main.js                 # 入口，Vue.prototype.$app = request
```

### 云函数

```
uniCloud-alipay/cloudfunctions/faceSearch/index.js
```

**Actions**：
- `detectAndSearch`：检测人脸 + 搜索明星（首页）
- `search`：搜索明星（首页重试）
- `searchGender`：跨性别搜索（搜索异性明星）
- `compare`：夫妻相比对（DetectFaceSimilarity 接口）

### 管理后台

```
admin/app.py  — 仅用于管理 IAI 明星数据（增删改查）
admin/persons_fixed.csv  — 明星数据（person_id, name, gender）
```

## 底部 TabBar 配置

| Tab | 页面 | 文字 |
|-----|------|------|
| 1 | pages/index/index | 明星脸 |
| 2 | pages/couple/couple | 夫妻相 |

图标路径：`static/tab/star.png` / `star_active.png` / `couple.png` / `couple_active.png`

## 腾讯云 IAI 接口

| 功能 | 接口 | 说明 |
|------|------|------|
| 明星脸搜索 | SearchFaces | 在指定 Group 中搜索相似人脸 |
| 夫妻相比对 | DetectFaceSimilarity | 两张人脸相似度比对 |
| 跨性别搜索 | SearchFaces | 搜索异性 Group（Group 按性别区分） |

### 明星数据分组

- 明星按地区分类：内地/港台/日韩/欧美
- gender 字段：1=男, 2=女
- 跨性别搜索时：用户男→搜索女明星Group，用户女→搜索男明星Group

### 质量控制

- `SearchFaces`：不设置 QualityControl
- `DetectFaceSimilarity`：QualityControl 设为 0（不控制，避免普通照片被拒绝）

## 分数映射策略

原始 API 分数太严格，通过非线性映射提升娱乐性：

### 夫妻相分数映射（mapCoupleScore）

| 原始分数 | 映射后 | 等级 |
|---------|--------|------|
| 0 | 35~40 | 🤝 萍水相逢 |
| 0~5 | 40~55 | 👀 似曾相识 |
| 5~15 | 55~70 | 💫 心有灵犀 |
| 15~30 | 70~85 | 💕 天生一对 |
| 30~50 | 85~95 | 👑 灵魂双生 |
| 50~100 | 95~100 | 👑 灵魂双生 |

### 跨性别搜索分数映射（mapSearchScore）

| 原始分数 | 映射后 |
|---------|--------|
| 0 | 30~40 |
| 0~30 | 40~60 |
| 30~50 | 60~75 |
| 50~70 | 75~85 |
| 70~100 | 85~100 |

## 积分系统

### 积分规则

| 操作 | 积分 |
|------|------|
| 分享给好友（好友打开后） | 双方各 +5 |
| 观看视频广告 | +5 |
| 明星脸比对 | -5 |
| 夫妻相比对 | -5 |
| 跨性别比对 | -5 |

### 积分接口

- 查询积分：`apiPath.common.userSurplus`
- 扣减积分：`apiPath.common.makePhoto`
- 分享加分：`apiPath.common.shareUser`
- 视频加分：`apiPath.common.videoPlus`

## 分享加分机制

### 封装：common/shareUtil.js

```js
// 在 Vue 组件中调用（必须传 this.$app）
shareUtil.handleShareBonus(this.$app, shareId, delay)

// 生成分享配置
shareUtil.getShareConfig(title, path)    // 自动拼接 shareId
shareUtil.getTimelineConfig(title)        // 自动拼接 shareId
```

### 重要注意事项

- `this.$app` 是通过 `Vue.prototype.$app = request` 挂载的，**只在 Vue 组件实例上可用**
- 独立 JS 模块中不能用 `getApp().$app`，必须由调用方传入 `this.$app`
- `request.js` 使用 `export default`（ES module），`require` 无法正确导入
- 所有 6 个页面（3个操作页 + 3个结果页）都需要处理分享加分

### 分享链接格式

所有分享链接必须带 `shareId` 参数：
- 好友分享：`path: '/pages/xxx/xxx?shareId=xxx'`
- 朋友圈分享：`query: 'shareId=xxx'`

## 广告系统

### 封装：common/AdUtil.js

```js
// 插屏广告
AdUtil.interstitial.load('广告ID')   // 初始化
AdUtil.interstitial.show()           // 显示

// 激励视频
AdUtil.rewarded.load(callback)       // 初始化，callback 为看完视频后的回调
AdUtil.rewarded.show()               // 显示
```

### 广告 ID

| 类型 | ID |
|------|-----|
| 激励视频 | adunit-22a1ee4156c3ba71 |
| 插屏广告 | adunit-ce26991cb47c9e83 |

### 插屏广告使用场景

- 跨性别比对成功后 1 秒弹出

### 开发者工具限制

- 插屏广告在微信开发者工具中通常**无法预览**，需真机测试
- 激励视频同理

## 跨性别比对特殊逻辑

### 三次失败限制

- 每次比对失败（未找到明星/接口报错/网络异常）累加 `failCount`
- 存储到 `uni.setStorageSync('crossGenderFailCount')` 和 `crossGenderFailDate`
- 达到 3 次后禁用比对按钮，提示"今日比对次数已用完"
- **次日自动重置**（通过日期判断）

## 更多玩法菜单

### 首页悬浮球菜单（2个入口）

1. 🌈 跨性别撞脸 → `/pages/cross-gender/cross-gender`
2. 💡 关于 → `/pages/about/about`

### 结果页底部其他玩法（2个入口，排除当前功能）

| 结果页 | 其他玩法 1 | 其他玩法 2 |
|--------|-----------|-----------|
| 明星脸结果 | 💑 夫妻相/闺蜜相 | 🌈 跨性别撞脸 |
| 夫妻相结果 | 🌟 明星脸比对 | 🌈 跨性别撞脸 |
| 跨性别结果 | 🌟 明星脸比对 | 💑 夫妻相/闺蜜相 |

### 跳转方式

- TabBar 页面（首页/夫妻相）→ `uni.switchTab`
- 普通页面（跨性别）→ `uni.navigateTo`

## UI 提示文案

- 上传处理中：`正在处理，请稍候...`
- 检测人脸：`正在检测人脸...`
- 比对人脸：`正在比对人脸...`
- 隐私提示：`人脸数据仅用于本次比对，不做他用`
- 娱乐提示：`比对结果仅供娱乐`

## 积分弹窗

- 三个操作页（首页/夫妻相/跨性别）都有"如何获取积分？"按钮
- 点击弹出积分获取弹窗，包含 `open-type="share"` 的分享按钮
- 点击分享按钮时**立即关闭弹窗**（`@click="showScoreModal = false"`），避免分享截图包含弹窗

## 小程序名称

**明星脸比对**（不是"明星撞脸"）

## 全局样式

- 导航栏背景色：`#ff6b9d`
- 导航栏文字：白色
- 页面背景色：`#fff0f5`
- tabBar 选中色：`#ff6b9d`
