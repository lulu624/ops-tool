#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@Project : ops-tool
@File    : main.py.py
@Author  : JingJun
@Date    : 2023/12/15 16:16
"""
import click
from utils.jumpserver import Jumpserver
from utils.yearning import Yearning


@click.group()
def main():
    """欢迎使用opt-tool运维工具箱v0.0.1版本"""


@main.group()
def server():
    """服务器管理"""


@server.command('list')
def get_server_list():
    """列出全部物理机列表"""
    server_list = Jumpserver().physical_server()
    for server in server_list:
        print(server)


@main.group()
def yearning():
    """yearning管理"""


@yearning.command("auto")
def yearning_auto_select():
    work_id_list = Yearning().get_order()
    if work_id_list is not None:
        print("开始自动处理工单")
        Yearning().order_agree(work_id_list)


if __name__ == '__main__':
    main()
