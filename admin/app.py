"""
Flask 后台管理服务
提供：创建人员库、添加明星、搜索明星等接口
"""
from flask import Flask, request, jsonify
from tencent_iai import TencentIAI

from config import FLASK_HOST, FLASK_PORT, GROUP_ID, GROUP_NAME
import time
import os
import json
import glob

app = Flask(__name__)
iai = TencentIAI()


def load_stars():
    """从 data/new_cloud 目录读取所有 JSON 文件并合并"""
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "new_cloud")
    stars = []
    for json_file in sorted(glob.glob(os.path.join(data_dir, "*.json"))):
        with open(json_file, "r", encoding="utf-8") as f:
            stars.extend(json.load(f))
    return stars


# 构建明星数据字典，用于搜索时快速查找
STARS = load_stars()
STARS_MAP = {s["person_id"]: s for s in STARS}


# ─────────────────────────────────────────────
# 工具接口
# ─────────────────────────────────────────────

@app.route("/api/health", methods=["GET"])
def health():
    """健康检查"""
    return jsonify({"status": "ok", "time": time.strftime("%Y-%m-%d %H:%M:%S")})


@app.route("/api/group/create", methods=["POST"])
def create_group():
    """创建人员库"""
    result = iai.create_group(GROUP_NAME, tag="明星脸比对专用库")
    return jsonify(result)


@app.route("/api/group/list", methods=["GET"])
def list_groups():
    """获取所有人员库"""
    result = iai.get_group_list()
    return jsonify(result)


@app.route("/api/stars/list", methods=["GET"])
def list_stars():
    """查看已入库明星列表"""
    result = iai.get_person_list(GROUP_ID)
    return jsonify(result)


# ─────────────────────────────────────────────
# 批量添加明星
# ─────────────────────────────────────────────

@app.route("/api/stars/add", methods=["POST"])
def add_star():
    """添加单个明星到人员库"""
    data = request.json
    person_id = data.get("person_id")
    name = data.get("name")
    gender = data.get("gender", 0)
    url = data.get("url")
    remark = data.get("remark", "")

    if not all([person_id, name, url]):
        return jsonify({"error": "缺少必填参数: person_id, name, url"}), 400

    result = iai.create_person(
        group_id=GROUP_ID,
        person_name=name,
        person_id=person_id,
        gender=gender,
        image_url=url,
        remark=remark,
    )
    return jsonify(result)


@app.route("/api/stars/add_batch", methods=["POST"])
def add_stars_batch():
    """
    批量添加明星（从 stars_data.py）
    POST /api/stars/add_batch
    Body: {"start": 0, "end": 100}  可选，默认全部
    """
    data = request.json or {}
    start = data.get("start", 0)
    end = data.get("end", len(STARS))

    stars = STARS[start:end]
    results = []
    for i, star in enumerate(stars):
        print(f"[{i+1}/{len(stars)}] 添加: {star['name']} ...")
        result = iai.create_person(
            group_id=GROUP_ID,
            person_name=star["name"],
            person_id=star["person_id"],
            gender=star["gender"],
            image_url=star["url"],
            remark=star.get("remark", ""),
        )
        # 成功或失败都记录
        if "Error" in result:
            results.append({"star": star["name"], "status": "error", "msg": result["Error"]})
        else:
            results.append({"star": star["name"], "status": "success"})
        time.sleep(0.3)  # 避免请求过快

    success_count = sum(1 for r in results if r["status"] == "success")
    return jsonify({
        "total": len(results),
        "success": success_count,
        "fail": len(results) - success_count,
        "results": results
    })


# ─────────────────────────────────────────────
# 人脸搜索（小程序核心接口）
# ─────────────────────────────────────────────

@app.route("/api/face/search", methods=["POST"])
def search_face():
    """
    人脸搜索 - 小程序调用的核心接口
    POST /api/face/search
    Body: {"image_url": "用户上传图片的公网URL"}
    返回: 相似度最高的明星信息 + 图片URL
    """
    data = request.json
    image_url = data.get("image_url")

    if not image_url:
        return jsonify({"error": "缺少参数: image_url"}), 400

    result = iai.search_faces(GROUP_ID, image_url, top_k=5)

    # 整理返回结果，带上明星图片URL
    if "Response" in result and "Results" in result["Response"]:
        enriched = []
        for item in result["Response"]["Results"]:
            person_id = item["PersonId"]
            # 从STARS_MAP找到对应明星的图片URL
            star_info = STARS_MAP.get(person_id)
            enriched.append({
                "person_id": person_id,
                "name": item.get("Name", ""),
                "score": round(item.get("Score", 0), 2),
                "url": star_info["url"] if star_info else "",
                "remark": star_info.get("remark", "") if star_info else "",
                "gender": star_info.get("gender", 0) if star_info else 0,
            })
        result["Response"]["Results"] = enriched

    return jsonify(result)


# ─────────────────────────────────────────────
# 删除接口
# ─────────────────────────────────────────────

@app.route("/api/star/delete", methods=["POST"])
def delete_star():
    """删除单个明星"""
    data = request.json
    person_id = data.get("person_id")
    if not person_id:
        return jsonify({"error": "缺少参数: person_id"}), 400
    result = iai.delete_person(GROUP_ID, person_id)
    return jsonify(result)


@app.route("/api/group/delete", methods=["POST"])
def delete_group():
    """删除整个人员库（慎用）"""
    result = iai.delete_group(GROUP_ID)
    return jsonify(result)


# ─────────────────────────────────────────────
# 启动
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print(f"=" * 50)
    print(f"明星脸库 Flask 管理服务")
    print(f"=" * 50)
    print(f"服务地址: http://{FLASK_HOST}:{FLASK_PORT}")
    print(f"人员库ID: {GROUP_ID}")
    print(f"明星数量: {len(STARS)} 位 (data/new_cloud)")
    print()
    print(f"接口列表:")
    print(f"  GET  /api/health           - 健康检查")
    print(f"  POST /api/group/create     - 创建人员库")
    print(f"  GET  /api/group/list       - 查看人员库")
    print(f"  POST /api/stars/add        - 添加单个明星")
    print(f"  POST /api/stars/add_batch  - 批量添加明星")
    print(f"  GET  /api/stars/list       - 查看已入库明星")
    print(f"  POST /api/face/search      - 人脸搜索（核心）")
    print(f"  POST /api/star/delete      - 删除明星")
    print(f"  POST /api/group/delete     - 删除人员库")
    print(f"=" * 50)
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)
