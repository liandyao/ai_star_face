"""
一键添加明星脚本 - 自动创建人员库并批量导入明星
"""
import sys
import os
import json
import glob

# 添加 admin 目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tencent_iai import TencentIAI
from config import GROUP_ID, GROUP_NAME


def load_stars():
    """从 data/new_cloud 目录读取所有 JSON 文件并合并"""
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "new_cloud")
    stars = []
    for json_file in sorted(glob.glob(os.path.join(data_dir, "*.json"))):
        with open(json_file, "r", encoding="utf-8") as f:
            items = json.load(f)
            print(f"  读取 {os.path.basename(json_file)}: {len(items)} 条")
            stars.extend(items)
    return stars

iai = TencentIAI()


def main():
    print("=" * 60)
    print("  Star Face Database - One-Click Init")
    print("=" * 60)
    print()

    # Step 1: Delete old group if exists, then create new one
    print("[Step 1] 删除旧人员库并创建新的人员库...")
    
    # 先尝试删除旧的人员库（如果存在）
    print("  检查是否已存在人员库...")
    delete_res = iai.delete_group(GROUP_ID)
    if "Error" not in delete_res:
        print("  [OK] 旧人员库已删除")
    else:
        err_code = delete_res["Error"].get("Code", "")
        if "GroupNotExists" in err_code or "InvalidParameter.GroupId" in err_code:
            print("  [SKIP] 人员库不存在，将创建新的")
        else:
            print(f"  [WARN] 删除失败: {delete_res['Error']}")
    
    # 创建新的人员库，设置自定义描述字段
    print("  创建新的人员库...")
    res = iai.create_group(GROUP_NAME, tag="star face comparison", ex_descriptions=["url"])
    if "Error" in res:
        print(f"  [FAIL] {res['Error']}")
        return
    else:
        print("  [OK] 人员库创建成功，自定义字段: url")

    # Step 2: 加载明星数据并批量添加
    print()
    print("[Step 2] 加载明星数据...")
    STARS = load_stars()
    print(f"  共加载 {len(STARS)} 位明星")
    print()
    print(f"[Step 3] 批量添加 {len(STARS)} 位明星...")
    print("-" * 60)

    success = 0
    failed = []
    import time

    for i, star in enumerate(STARS):
        gender_str = "女" if star["gender"] == 2 else "男"
        star_name = star["name"]
        print(f"  [{i+1:>3}/{len(STARS)}] {star_name} ({gender_str}) ...")

        # 将照片URL作为自定义描述字段传入
        res = iai.create_person(
            group_id=GROUP_ID,
            person_name=star["name"],
            person_id=star["person_id"],
            gender=star["gender"],
            image_url=star["url"],
            ex_descriptions=[star["url"]]  # 将URL存入自定义字段
        )

        if "Error" in res:
            err_msg = res["Error"].get("Message", "")
            print(f"    [FAIL] {err_msg}")
            failed.append({"name": star_name, "error": res["Error"]})
        else:
            print(f"    [OK]")
            success += 1

        time.sleep(0.5)  # 避免API限流

    # Step 4: Summary
    print()
    print("=" * 60)
    print(f"  DONE! Success: {success}/{len(STARS)}, Failed: {len(failed)}")
    print("=" * 60)

    if failed:
        print()
        print("Failed list:")
        for f in failed:
            print(f"  - {f['name']}: {f['error'].get('Message', '')}")

    print()
    print("Next steps:")
    print("  1. python app.py")
    print("  2. http://localhost:5000/api/stars/list")


def add_one_test():
    print("=" * 60)
    print("  Star Face Database - One-Click Init")
    print("=" * 60)
    print()

    # Step 1: Delete old group if exists, then create new one
    print("[Step 1] 删除旧人员库并创建新的人员库...")

    # 先尝试删除旧的人员库（如果存在）
    print("  检查是否已存在人员库...")
    delete_res = iai.delete_group(GROUP_ID)
    if "Error" not in delete_res:
        print("  [OK] 旧人员库已删除")
    else:
        err_code = delete_res["Error"].get("Code", "")
        if "GroupNotExists" in err_code or "InvalidParameter.GroupId" in err_code:
            print("  [SKIP] 人员库不存在，将创建新的")
        else:
            print(f"  [WARN] 删除失败: {delete_res['Error']}")

    # 创建新的人员库，设置自定义描述字段
    print("  创建新的人员库...")
    res = iai.create_group(GROUP_NAME, tag="star face comparison", ex_descriptions=["url"])
    if "Error" in res:
        print(f"  [FAIL] {res['Error']}")
        return
    else:
        print("  [OK] 人员库创建成功，自定义字段: url")
    """添加一条测试明星数据"""
    test_star = {
        "name": "测试明星",
        "person_id": "test_star_001",
        "gender": 1,
        "url": "https://env-00jy674l53ts.normal.cloudstatic.cn/star-face-img/neidi/zhou_mei_yi.jpg",
    }
    gender_str = "女" if test_star["gender"] == 2 else "男"
    print(f"  {test_star['name']} ({gender_str}) ...")

    res = iai.create_person(
        group_id=GROUP_ID,
        person_name=test_star["name"],
        person_id=test_star["person_id"],
        gender=test_star["gender"],
        image_url=test_star["url"],
        ex_descriptions=[test_star["url"]]
    )

    if "Error" in res:
        print(f"  [FAIL] {res['Error'].get('Message', '')}")
    else:
        print(f"  [OK] 添加成功!")





def add_more():
    """从 data/new_cloud/补充/more_star.json 读取补充明星并添加到已有人员库"""
    json_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "new_cloud", "补充", "more_star.json")
    with open(json_file, "r", encoding="utf-8") as f:
        stars = json.load(f)

    print(f"加载补充明星 {len(stars)} 位，开始添加到人员库 {GROUP_ID}...")
    print("-" * 60)

    import time
    success = 0
    failed = []

    for i, star in enumerate(stars):
        gender_str = "女" if star["gender"] == 2 else "男"
        star_name = star["name"]
        print(f"  [{i+1}/{len(stars)}] {star_name} ({gender_str}) ...")

        res = iai.create_person(
            group_id=GROUP_ID,
            person_name=star["name"],
            person_id=star["person_id"],
            gender=star["gender"],
            image_url=star["url"],
            ex_descriptions=[star["url"]]
        )

        if "Error" in res:
            err_msg = res["Error"].get("Message", "")
            print(f"    [FAIL] {err_msg}")
            failed.append({"name": star_name, "error": res["Error"]})
        else:
            print(f"    [OK]")
            success += 1

        time.sleep(0.5)

    print()
    print("=" * 60)
    print(f"  DONE! Success: {success}/{len(stars)}, Failed: {len(failed)}")
    print("=" * 60)

    if failed:
        print("Failed list:")
        for f in failed:
            print(f"  - {f['name']}: {f['error'].get('Message', '')}")

if __name__ == "__main__":

    add_more()