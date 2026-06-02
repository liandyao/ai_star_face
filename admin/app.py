"""
Flask 后台管理服务
仅用于管理腾讯云 IAI 明星人员库（增删查）
业务逻辑（人脸搜索、比对等）由 uniCloud 云函数 faceSearch 处理
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


STARS = load_stars()
STARS_MAP = {s["person_id"]: s for s in STARS}


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "time": time.strftime("%Y-%m-%d %H:%M:%S")})


@app.route("/api/group/create", methods=["POST"])
def create_group():
    result = iai.create_group(GROUP_NAME, tag="明星脸比对专用库")
    return jsonify(result)


@app.route("/api/group/list", methods=["GET"])
def list_groups():
    result = iai.get_group_list()
    return jsonify(result)


@app.route("/api/stars/list", methods=["GET"])
def list_stars():
    result = iai.get_person_list(GROUP_ID)
    return jsonify(result)


@app.route("/api/stars/add", methods=["POST"])
def add_star():
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
        if "Error" in result:
            results.append({"star": star["name"], "status": "error", "msg": result["Error"]})
        else:
            results.append({"star": star["name"], "status": "success"})
        time.sleep(0.3)

    success_count = sum(1 for r in results if r["status"] == "success")
    return jsonify({
        "total": len(results),
        "success": success_count,
        "fail": len(results) - success_count,
        "results": results
    })


@app.route("/api/star/delete", methods=["POST"])
def delete_star():
    data = request.json
    person_id = data.get("person_id")
    if not person_id:
        return jsonify({"error": "缺少参数: person_id"}), 400
    result = iai.delete_person(GROUP_ID, person_id)
    return jsonify(result)


@app.route("/api/group/delete", methods=["POST"])
def delete_group():
    result = iai.delete_group(GROUP_ID)
    return jsonify(result)


@app.route("/api/stars/data", methods=["GET"])
def get_stars_data():
    """获取本地明星数据（供管理后台使用）"""
    category = request.args.get("category", "")
    gender = request.args.get("gender", 0, type=int)

    stars = STARS
    if category:
        stars = [s for s in stars if category in s.get("person_id", "")]
    if gender:
        stars = [s for s in stars if s.get("gender") == gender]

    return jsonify({
        "total": len(STARS),
        "filtered": len(stars),
        "stars": stars
    })


if __name__ == "__main__":
    print(f"=" * 50)
    print(f"明星脸库 Flask 管理服务（仅管理，不含业务接口）")
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
    print(f"  GET  /api/stars/data       - 获取本地明星数据")
    print(f"  POST /api/star/delete      - 删除明星")
    print(f"  POST /api/group/delete     - 删除人员库")
    print(f"=" * 50)
    print(f"业务接口已迁移至 uniCloud 云函数 faceSearch:")
    print(f"  action=detectAndSearch - 人脸检测+搜索")
    print(f"  action=search          - 人脸搜索（跳过质量检测）")
    print(f"  action=compare         - 夫妻相/闺蜜相比对(DetectFaceSimilarity)")
    print(f"  action=searchGender    - 跨性别明星脸搜索")
    print(f"  action=getStars        - 获取明星图鉴数据")
    print(f"=" * 50)
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)
