# 明星撞脸 - Star Face

> 上传照片，AI 找出和你最像的明星！前端直调腾讯云 IAI，零中转延迟；Flask 后台仅用于批量管理人员库。

## 项目结构

```
mingxing_face/
├── admin/                              # 后台管理（仅用于初始化/管理人员库）
│   ├── app.py                          # Flask 管理服务（人员库CRUD、批量导入等）
│   ├── config.py                       # 腾讯云 API 配置
│   ├── tencent_iai.py                  # 腾讯云 IAI SDK 封装
│   ├── add_stars.py                    # 一键初始化 IAI 人员库
│   ├── scrape_category.py              # 明星数据爬取脚本
│   └── data/                           # 明星数据与图片
│       └── new_cloud/                  # JSON 格式明星数据
│
├── star_face_uniapp/                   # UniApp 前端（微信小程序）
│   ├── pages/
│   │   ├── index/index.vue             # 首页：拍照/选图 → 前端直调 IAI 人脸搜索
│   │   └── result/result.vue           # 结果页：展示 Top5 相似明星
│   └── uniCloud-alipay/cloudfunctions/ # 云函数（仅存储密钥）
│
└── .gitignore
```

## 核心流程

```
用户拍照/选图
    │
    ▼
小程序前端（index.vue）
  1. 压缩图片 → base64
  2. 云函数获取腾讯云密钥（getSecret）
  3. 前端本地完成 TC3-HMAC-SHA256 签名
  4. 前端直调腾讯云 IAI SearchFaces 接口
    │
    ▼
腾讯云 IAI（前端直连，不经后台中转）
  5. 在人员库中匹配，返回 Top5 候选明星
    │
    ▼
小程序前端（result.vue）
  6. 展示相似明星列表（头像、姓名、相似度）
```

**关键架构**：前端直调腾讯云 IAI，云函数仅存储密钥，API 签名在前端完成，不经过后台中转，零额外延迟。Flask 后台仅用于批量管理人员库数据。

## 快速开始

### 1. 环境准备

```bash
cd admin
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install tencentcloud-sdk-python flask requests beautifulsoup4 pypinyin
```

### 2. 配置腾讯云密钥

编辑 `admin/config.py`，填入你的腾讯云 SecretId 和 SecretKey：

```python
SECRET_ID = "你的SecretId"
SECRET_KEY = "你的SecretKey"
REGION = "ap-guangzhou"
GROUP_ID = "star_face_group"
GROUP_NAME = "star_face_group"
```

### 3. 初始化人员库（一次性）

```bash
python add_stars.py
```

该脚本会自动创建人员库并批量导入 `data/new_cloud/` 下的明星数据。

### 4. 运行小程序

用 HBuilderX 打开 `star_face_uniapp/` 目录，运行到微信开发者工具。

## API 接口（后台管理，可选）

Flask 后台提供人员库管理接口，非小程序运行必需：

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/health` | 健康检查 |
| POST | `/api/group/create` | 创建人员库 |
| GET | `/api/group/list` | 查看人员库列表 |
| POST | `/api/stars/add` | 添加单个明星 |
| POST | `/api/stars/add_batch` | 批量添加明星 |
| GET | `/api/stars/list` | 查看已入库明星 |
| POST | `/api/face/search` | 人脸搜索（核心接口） |
| POST | `/api/star/delete` | 删除单个明星 |
| POST | `/api/group/delete` | 删除人员库 |

### 人脸搜索示例

```bash
curl -X POST http://localhost:5000/api/face/search \
  -H "Content-Type: application/json" \
  -d '{"image_url": "https://example.com/photo.jpg"}'
```

返回结果：

```json
{
  "Response": {
    "Results": [
      {
        "person_id": "xxx",
        "name": "明星名",
        "score": 85.5,
        "url": "https://xxx/star.jpg",
        "remark": "",
        "gender": 1
      }
    ]
  }
}
```

## 爬取明星数据

```bash
# 爬取日韩明星
python scrape_category.py 0003 rihan

# 爬取欧美明星
python scrape_category.py 0004 oumei
```

支持分步执行：`python scrape_category.py 0003 rihan list`（仅收集链接）或 `detail`（仅爬取详情）。

## 添加新明星

1. 将明星数据 JSON 放入 `admin/data/new_cloud/` 目录
2. 运行 `python add_stars.py` 重新初始化人员库
3. 或通过 API 单个添加：`POST /api/stars/add`

## 技术栈

- **前端**：UniApp + Vue.js（微信小程序，直调腾讯云 IAI）
- **后台**：Flask (Python)（仅批量管理人员库）
- **人脸识别**：腾讯云 IAI（人脸搜索 3.0）
- **数据爬取**：BeautifulSoup + pypinyin

## 后续扩展
- 人脸试妆产品正式上线，欢迎接入美颜、试唇色等AI能力。
- 人像变换产品正式上线，欢迎接入动漫化、人像渐变、变老变年轻、变性别等AI能力。
