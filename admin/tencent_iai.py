# -*- coding: utf8 -*-
"""
腾讯云 IAI 人脸识别 API 封装
基于腾讯云官方 SDK 封装的便捷业务方法
"""
import json
import time
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.iai.v20200303 import iai_client, models
from config import SECRET_ID, SECRET_KEY, REGION


def get_client():
    """获取 IAI 客户端"""
    cred = credential.Credential(SECRET_ID, SECRET_KEY)
    http_profile = HttpProfile()
    http_profile.endpoint = "iai.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    client_profile.signMethod = "TC3-HMAC-SHA256"
    client = iai_client.IaiClient(cred, REGION, client_profile)
    return client


class TencentIAI:
    """腾讯云 IAI 人脸识别 API 封装类（提供便捷的业务方法）"""

    def create_group(self, group_name, tag="", ex_descriptions=None):
        """
        创建人员库
        :param group_name: 人员库名称
        :param tag: 标签
        :param ex_descriptions: 自定义描述字段名称列表，如 ['url', 'remark']
        :return: 创建结果
        """
        client = get_client()
        req = models.CreateGroupRequest()
        req.GroupName = group_name
        req.GroupId = "star_face_group"
        req.FaceModelVersion = "3.0"
        req.Tag = tag
        
        # 设置自定义描述字段
        if ex_descriptions:
            req.GroupExDescriptions = ex_descriptions
        
        try:
            resp = client.CreateGroup(req)
            return {"Response": {"FaceModelVersion": resp.FaceModelVersion, "RequestId": resp.RequestId}}
        except TencentCloudSDKException as e:
            return {"Error": {"Code": e.code, "Message": e.message}}

    def get_group_list(self):
        """获取人员库列表"""
        client = get_client()
        req = models.GetGroupListRequest()
        try:
            resp = client.GetGroupList(req)
            groups = [{"GroupId": g.GroupId, "GroupName": g.GroupName, "Tag": getattr(g, 'Tag', '')} for g in resp.GroupInfos]
            return {"Response": {"GroupInfos": groups, "RequestId": resp.RequestId}}
        except TencentCloudSDKException as e:
            return {"Error": {"Code": e.code, "Message": e.message}}

    def delete_group(self, group_id):
        """删除人员库"""
        client = get_client()
        req = models.DeleteGroupRequest()
        req.GroupId = group_id
        try:
            resp = client.DeleteGroup(req)
            return {"Response": {"RequestId": resp.RequestId}}
        except TencentCloudSDKException as e:
            return {"Error": {"Code": e.code, "Message": e.message}}

    def create_person(self, group_id, person_name, person_id, image_url, gender=0, ex_descriptions=None):
        """
        单个创建人员
        :param group_id: 人员库ID
        :param person_name: 人员名称
        :param person_id: 人员ID（唯一标识）
        :param image_url: 图片URL
        :param gender: 性别（0-未指定，1-男，2-女）
        :param ex_descriptions: 自定义描述字段值列表，与创建人员库时的 GroupExDescriptions 对应
                                 例如：['https://example.com/photo.jpg']
        :return: 创建结果
        """
        client = get_client()
        req = models.CreatePersonRequest()
        req.GroupId = group_id
        req.PersonName = person_name
        req.PersonId = person_id
        req.Gender = gender
        req.Url = image_url
        req.QualityControl = 4  # 宽松质控
        
        # 设置自定义描述字段值
        if ex_descriptions:
            req.PersonExDescriptionInfos = []
            for index, desc_value in enumerate(ex_descriptions):
                desc_info = models.PersonExDescriptionInfo()
                desc_info.PersonExDescriptionIndex = index  # 字段索引（从0开始）
                desc_info.PersonExDescription = desc_value  # 字符串类型，不是数组
                req.PersonExDescriptionInfos.append(desc_info)
        
        try:
            resp = client.CreatePerson(req)
            return {
                "Response": {
                    "FaceId": resp.FaceId,
                    "FaceModelVersion": resp.FaceModelVersion,
                    "RequestId": resp.RequestId
                }
            }
        except TencentCloudSDKException as e:
            return {"Error": {"Code": e.code, "Message": e.message}}

    def create_persons_batch(self, group_id, persons_data):
        """
        批量创建人员
        :param group_id: 人员库ID
        :param persons_data: 人员数据列表，每个元素为字典，包含：
            - person_name: 人员名称
            - person_id: 人员ID（唯一标识）
            - image_url: 图片URL
            - gender: 性别（可选，0-未指定，1-男，2-女）
            - remark: 备注信息（可选）
            - ex_descriptions: 自定义描述字段值列表（可选），与创建人员库时的 GroupExDescriptions 对应
        :return: 批量创建结果，包含成功和失败的人员列表
        """
        results = {
            "success": [],
            "failed": []
        }
        
        for i, person in enumerate(persons_data):
            res = self.create_person(
                group_id=group_id,
                person_name=person.get("person_name"),
                person_id=person.get("person_id"),
                image_url=person.get("image_url"),
                gender=person.get("gender", 0),
                ex_descriptions=person.get("ex_descriptions")
            )
            
            if "Error" in res:
                results["failed"].append({
                    "index": i,
                    "person_name": person.get("person_name"),
                    "person_id": person.get("person_id"),
                    "error": res["Error"]
                })
            else:
                results["success"].append({
                    "index": i,
                    "person_name": person.get("person_name"),
                    "person_id": person.get("person_id"),
                    "face_id": res["Response"]["FaceId"]
                })
            
            # API限流控制，每次请求间隔0.5秒
            time.sleep(0.5)
        
        return results

    def get_person_list(self, group_id, offset=0, limit=100):
        """获取人员列表"""
        client = get_client()
        req = models.GetPersonListRequest()
        req.GroupId = group_id
        req.Offset = offset
        req.Limit = limit
        try:
            resp = client.GetPersonList(req)
            persons = [{
                "PersonName": p.PersonName,
                "PersonId": p.PersonId,
                "Gender": p.Gender,
                "FaceIds": list(p.FaceIds) if p.FaceIds else []
            } for p in resp.PersonInfos]
            return {"Response": {"PersonInfos": persons, "RequestId": resp.RequestId}}
        except TencentCloudSDKException as e:
            return {"Error": {"Code": e.code, "Message": e.message}}

    def delete_person(self, group_id, person_id):
        """删除人员"""
        client = get_client()
        req = models.DeletePersonRequest()
        req.GroupId = group_id
        req.PersonId = person_id
        try:
            resp = client.DeletePerson(req)
            return {"Response": {"RequestId": resp.RequestId}}
        except TencentCloudSDKException as e:
            return {"Error": {"Code": e.code, "Message": e.message}}

    def compare_face(self, image_a, image_b, image_a_type="URL", image_b_type="URL"):
        """
        人脸比对 - 比较两张照片的相似度
        :param image_a: 图片A（URL或Base64）
        :param image_b: 图片B（URL或Base64）
        :param image_a_type: 图片A类型，"URL" 或 "BASE64"
        :param image_b_type: 图片B类型，"URL" 或 "BASE64"
        :return: 比对结果，包含相似度分数
        """
        client = get_client()
        req = models.CompareFaceRequest()
        if image_a_type == "BASE64":
            req.ImageA = image_a
        else:
            req.UrlA = image_a
        if image_b_type == "BASE64":
            req.ImageB = image_b
        else:
            req.UrlB = image_b
        req.QualityControl = 4
        try:
            resp = client.CompareFace(req)
            return {
                "Response": {
                    "Score": round(resp.Score, 2),
                    "FaceModelVersion": resp.FaceModelVersion,
                    "RequestId": resp.RequestId
                }
            }
        except TencentCloudSDKException as e:
            return {"Error": {"Code": e.code, "Message": e.message}}

    def search_faces(self, group_id, image_url, top_k=5):
        """人脸搜索"""
        client = get_client()
        req = models.SearchFacesRequest()
        req.GroupIds = [group_id]
        req.ImageUrl = image_url
        req.TopK = top_k
        req.NeedResultContent = ["URL"]
        req.FaceMatchThreshold = 30.0
        try:
            resp = client.SearchFaces(req)
            results = []
            for r in resp.Results:
                results.append({
                    "PersonId": r.PersonId,
                    "Name": r.PersonName,
                    "Score": round(r.Score, 2),
                })
            return {"Response": {"Results": results, "RequestId": resp.RequestId}}
        except TencentCloudSDKException as e:
            return {"Error": {"Code": e.code, "Message": e.message}}
