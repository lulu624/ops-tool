#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@Project : ops-tool
@File    : jumpserver.py
@Author  : JingJun
@Date    : 2023/12/15 17:22
"""
import requests
import json
from utils.read_config import readConfig

class Jumpserver:
    def __init__(self):
        config = readConfig()
        self.url = config['jumpserver']['url']
        self.username = config['jumpserver']['username']
        self.password = config['jumpserver']['password']
        self.token = ""

    def get_token(self):
        url = self.url + '/api/v1/authentication/auth/'
        query_args = {
            "username": self.username,
            "password": self.password,
        }
        response = requests.post(url, data=query_args)
        self.token = json.loads(response.text)['token']
        # return json.loads(response.text)['token']

    def get_assets(self):
        url = self.url + '/api/v1/assets/assets/'

        headers = {
            "Authorization": 'Bearer ' + self.token,
        }
        response = requests.get(url, headers=headers)
        return json.loads(response.text)

    def all_server(self):
        self.get_token()
        assets = self.get_assets()

        # 仅计算活动的linux服务器
        all_list = [asset.get("ip") for asset in assets if
                    asset.get("ip") and asset.get("is_active") == True and asset.get("platform") == "Linux"]
        return all_list

    def physical_server(self):
        self.get_token()
        assets = self.get_assets()
        # 物理机列表
        physical_list = [physical.get("ip") for physical in assets if
                         physical.get("model") and physical.get("model") != "KVM" and physical.get(
                             "vendor") != "Alibaba Cloud" and physical.get("is_active") == True and physical.get(
                             "platform") == "Linux"]

        return physical_list
