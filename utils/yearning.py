#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@Project : ops-tool
@File    : yearning.py
@Author  : JingJun
@Date    : 2023/12/15 17:57
"""
from utils.read_config import readConfig
import requests


class Yearning:
    def __init__(self):
        config = readConfig()
        self.url = config['yearning']['url']
        self.username = config['yearning']['username']
        self.password = config['yearning']['password']
        self.is_ldap = config['yearning']['is_ldap']
        self.token = ""

    def get_token(self):
        # 获取认证的token
        data = {
            "username": self.username,
            "password": self.password
        }
        headers = {
            "Accept": "application/json"
        }
        request = requests.post(self.url + "/login", data=data, headers=headers)
        request = request.json()
        self.token = request.get('payload').get('token')

    def get_order(self):
        # 获取待处理的查询工单
        self.get_token()
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer" + " " + self.token
        }
        data = {
            "expr": {
                "work_id": "",
                "username": "",
                "status": 7
            },
            "current": 1,
            "pageSize": 20
        }
        request = requests.put(self.url + '/api/v2/audit/query/list?tp=order', json=data, headers=headers)
        response = request.json()
        data = response.get('payload').get('data')

        work_id_list = []
        for i in data:
            if i.get('status') == 1:
                # 1为待审批，2为查询中，3位查询结束
                print("发现待审批的查询工单", i)
                work_id_list.append(i.get('work_id'))

        if len(work_id_list) == 0:
            print("未获取到待处理工单")
            return None
        else:
            return work_id_list

    def order_agree(self, work_id_list):
        """自动处理查询的待审批工单"""
        self.get_token()
        for work_id in work_id_list:
            headers = {
                "Accept": "application/json",
                "Authorization": "Bearer" + " " + self.token
            }
            data = {
                "work_id": work_id
            }

            request = requests.post(self.url + '/api/v2/audit/query/agreed', json=data, headers=headers)
            response = request.json()
            if response.get('code') == 1200:
                print(work_id + response.get('text'))
