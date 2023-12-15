#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@Project : ops-tool
@File    : read_config.py
@Author  : JingJun
@Date    : 2023/12/15 17:48
"""
import yaml
import os


def readConfig():
    # 获取当前脚本所在的目录（即当前文件所在的目录）
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 获取项目根目录（上一级目录）
    root_dir = os.path.dirname(current_dir)

    # 拼接配置文件的完整路径
    config_file_path = os.path.join(root_dir, 'config.yaml')

    # 读取YAML配置文件
    with open(config_file_path, 'r') as stream:
        try:
            # 使用yaml.safe_load()加载YAML内容
            config_data = yaml.safe_load(stream)

            # 现在，config_data变量包含了YAML文件中的数据，可以按照字典的方式访问它
            return config_data

        except yaml.YAMLError as e:
            print(f"Error while loading YAML file: {e}")
