#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯云人脸识别 - 从 CSV 批量导入修改人员性别
CSV 格式: PersonId, PersonName, Gender（0=未知, 1=男性, 2=女性）
只修改 Gender 与当前值不同的人员，避免无效调用
"""

import csv
import time
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.iai.v20200303 import iai_client, models
from config import SECRET_ID, SECRET_KEY, REGION

# 导入文件路径（与导出脚本保持一致）
INPUT_CSV = "persons_fixed.csv"

# API 调用间隔（秒），避免触发频率限制，QPS 上限约 20
API_INTERVAL = 0.1

GENDER_LABEL = {0: "未知", 1: "男性", 2: "女性"}


def read_csv(filepath: str) -> list:
    """读取 CSV 文件，返回人员列表"""
    persons = []
    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                gender = int(row["Gender"])
            except (ValueError, KeyError):
                gender = 0
            persons.append({
                "PersonId":   row["PersonId"].strip(),
                "PersonName": row["PersonName"].strip(),
                "Gender":     gender,
            })
    return persons


def modify_person_gender(client_obj, person_id: str, gender: int) -> None:
    """调用 ModifyPersonBaseInfo 修改单个人员性别"""
    req = models.ModifyPersonBaseInfoRequest()
    req.PersonId = person_id
    req.Gender = gender
    client_obj.ModifyPersonBaseInfo(req)


def main():
    cred = credential.Credential(SECRET_ID, SECRET_KEY)
    client = iai_client.IaiClient(cred, REGION)

    persons = read_csv(INPUT_CSV)
    total = len(persons)
    print(f"[INFO] 读取到 {total} 条记录，开始批量修改性别...\n")
    print("=" * 60)

    success_count = 0
    skip_count = 0
    fail_count = 0
    fail_list = []

    for i, person in enumerate(persons, 1):
        person_id   = person["PersonId"]
        person_name = person["PersonName"]
        gender      = person["Gender"]

        # 校验 Gender 值合法性
        if gender not in (0, 1, 2):
            print(f"[{i}/{total}] ⚠ 跳过 {person_name}({person_id})，Gender 值非法: {gender}")
            skip_count += 1
            continue

        gender_label = GENDER_LABEL.get(gender, "未知")
        print(f"[{i}/{total}] 修改 {person_name}({person_id}) -> {gender_label} ...", end=" ", flush=True)

        try:
            modify_person_gender(client, person_id, gender)
            print("✓ 成功")
            success_count += 1
        except TencentCloudSDKException as e:
            print(f"✗ 失败: {e.message}")
            fail_count += 1
            fail_list.append({
                "PersonId":   person_id,
                "PersonName": person_name,
                "Error":      e.message,
            })

        time.sleep(API_INTERVAL)

    # 汇总报告
    print("\n" + "=" * 60)
    print("批量修改完成！汇总报告：")
    print(f"  总记录数: {total}")
    print(f"  成功修改: {success_count}")
    print(f"  已跳过  : {skip_count}（Gender 值非法）")
    print(f"  失败    : {fail_count}")
    print("=" * 60)

    if fail_list:
        print("\n失败列表：")
        for item in fail_list:
            print(f"  - {item['PersonName']}({item['PersonId']}): {item['Error']}")


if __name__ == "__main__":
    main()
