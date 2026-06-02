#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯云人脸识别 - 导出人员库人员信息到 CSV
导出字段: PersonId, PersonName, Gender
Gender 说明: 0=未知, 1=男性, 2=女性
"""

import csv
import time
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.iai.v20200303 import iai_client, models
from config import SECRET_ID, SECRET_KEY, REGION, GROUP_ID

# 导出文件路径
OUTPUT_CSV = "persons.csv"


def get_all_persons(client_obj, group_id: str) -> list:
    """分页获取人员库中所有人员信息"""
    persons = []
    offset = 0
    limit = 1000
    print(f"[INFO] 开始获取人员库 '{group_id}' 中的所有人员...")

    while True:
        req = models.GetPersonListRequest()
        req.GroupId = group_id
        req.Offset = offset
        req.Limit = limit

        resp = client_obj.GetPersonList(req)
        batch = resp.PersonInfos or []
        persons.extend(batch)
        print(f"[INFO] 已获取 {len(persons)} 条，本批 {len(batch)} 条")

        if len(batch) < limit:
            break
        offset += limit
        time.sleep(0.1)

    print(f"[INFO] 共获取 {len(persons)} 位人员\n")
    return persons


def main():
    cred = credential.Credential(SECRET_ID, SECRET_KEY)
    client = iai_client.IaiClient(cred, REGION)

    persons = get_all_persons(client, GROUP_ID)

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        # 写表头
        writer.writerow(["PersonId", "PersonName", "Gender"])
        # 写数据
        for p in persons:
            gender = getattr(p, "Gender", 0) or 0
            writer.writerow([p.PersonId, p.PersonName or "", gender])

    print(f"[INFO] 导出完成！共 {len(persons)} 条记录，已保存到 {OUTPUT_CSV}")
    print("[INFO] Gender 说明: 0=未知  1=男性  2=女性")
    print("[INFO] 请在 CSV 中修改 Gender 列后，运行 import_persons.py 导入")


if __name__ == "__main__":
    main()
