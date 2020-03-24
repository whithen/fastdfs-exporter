#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Auther: Ray
# @Time: 2019/11/5 10:40

from prometheus_client import Gauge, generate_latest, CollectorRegistry
from flask import Response, Flask
import os
import json
import time, datetime
import re

app = Flask(__name__)

# 定义数据仓库
REGISTRY = CollectorRegistry()
fastdfs_tracker_server_info = Gauge('fastdfs_tracker_server_info', "fastdfs_tracker_server_info", ['tracker'],
                                    registry=REGISTRY)
fastdfs_group_info = Gauge('fastdfs_group_info', "fastdfs_group_info", ['group'],
                           registry=REGISTRY)
fastdfs_storage_server_count = Gauge('fastdfs_storage_server_count', "fastdfs_storage_server_count", ['group'],
                                     registry=REGISTRY)
fastdfs_active_server_count = Gauge('fastdfs_active_server_count', "fastdfs_active_server_count", ['group'],
                                    registry=REGISTRY)
fastdfs_disk_total_space = Gauge('fastdfs_disk_total_space', "fastdfs_disk_total_space", ['group'],
                                 registry=REGISTRY)
fastdfs_disk_free_space = Gauge('fastdfs_disk_free_space', "fastdfs_disk_free_space", ['group'],
                                registry=REGISTRY)
fastdfs_storage_server_info = Gauge('fastdfs_storage_server_info', "fastdfs_storage_server_info",
                                    ['group', 'storage', 'ip', 'version'], registry=REGISTRY)
fastdfs_join_time = Gauge('fastdfs_join_time', "fastdfs_join_time", ['group', 'storage', 'ip', 'version'],
                          registry=REGISTRY)
fastdfs_up_time = Gauge('fastdfs_up_time', "fastdfs_up_time", ['group', 'storage', 'ip', 'version'],
                        registry=REGISTRY)
fastdfs_total_storage = Gauge('fastdfs_total_storage', "fastdfs_total_storage",
                              ['group', 'storage', 'ip', 'version'],
                              registry=REGISTRY)
fastdfs_free_storage = Gauge('fastdfs_free_storage', "fastdfs_free_storage",
                             ['group', 'storage', 'ip', 'version'],
                             registry=REGISTRY)
fastdfs_total_upload_count = Gauge('fastdfs_total_upload_count', "fastdfs_total_upload_count",
                                   ['group', 'storage', 'ip', 'version'], registry=REGISTRY)
fastdfs_success_upload_count = Gauge('fastdfs_success_upload_count', "fastdfs_success_upload_count",
                                     ['group', 'storage', 'ip', 'version'], registry=REGISTRY)
fastdfs_total_delete_count = Gauge('fastdfs_total_delete_count', "fastdfs_total_delete_count",
                                   ['group', 'storage', 'ip', 'version'], registry=REGISTRY)
fastdfs_success_delete_count = Gauge('fastdfs_success_delete_count', "fastdfs_success_delete_count",
                                     ['group', 'storage', 'ip', 'version'], registry=REGISTRY)
fastdfs_total_download_count = Gauge('fastdfs_total_download_count', "fastdfs_total_download_count",
                                     ['group', 'storage', 'ip', 'version'], registry=REGISTRY)
fastdfs_success_download_count = Gauge('fastdfs_success_download_count', "fastdfs_success_download_count",
                                       ['group', 'storage', 'ip', 'version'], registry=REGISTRY)
fastdfs_total_upload_bytes = Gauge('fastdfs_total_upload_bytes', "fastdfs_total_upload_bytes",
                                   ['group', 'storage', 'ip', 'version'], registry=REGISTRY)
fastdfs_success_upload_bytes = Gauge('fastdfs_success_upload_bytes', "fastdfs_success_upload_bytes",
                                     ['group', 'storage', 'ip', 'version'], registry=REGISTRY)
fastdfs_total_download_bytes = Gauge('fastdfs_total_download_bytes', "fastdfs_total_download_bytes",
                                     ['group', 'storage', 'ip', 'version'], registry=REGISTRY)
fastdfs_success_download_bytes = Gauge('fastdfs_success_download_bytes', "fastdfs_success_download_bytes",
                                       ['group', 'storage', 'ip', 'version'], registry=REGISTRY)

# 定义tracker/group/storage数据存储字典
trackerServer = dict()
trackerServer['tracker'] = []
tracker = dict()
storageServer = dict()
storageServer["group"] = []
group = dict()
storage = dict()

# 定义fdfs client.conf
client_file = "/etc/fdfs/client.conf"

# 定义查找清单
groupInfolist = ['group name', 'disk total space', 'disk free space', 'storage server count', 'active server count']
storageInfolist = ['id', 'ip_addr', 'version', 'join time', 'up time', 'total storage', 'free storage',
                   'total_upload_count', 'success_upload_count', 'total_delete_count',
                   'success_delete_count',
                   'total_download_count', 'success_download_count', 'total_upload_bytes',
                   'success_upload_bytes',
                   'stotal_download_bytes', 'success_download_bytes', 'last_heart_beat_time',
                   'last_source_update',
                   'last_sync_update', 'last_synced_timestamp']


# 数据格式化
def formatValue(value):
    try:
        # 匹配join time = 2019-04-04 17:00:49
        result = re.findall("(\d+-\d+-\d+ \d+:\d+:\d+)", value)
        if result:
            timeStamp = time.mktime(datetime.datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S").timetuple())
            value = float(timeStamp)
        # 匹配total storage = 1007799 MB
        result = re.findall("(\d+) MB$", value)
        if result: value = float(result[0]) * 1024 * 1024
        # 匹配ip_addr = 10.42.3.244  ACTIVE
        result = re.findall("(\d+\.\d+\.\d+\.\d+).+[A-Z]+", value)
        if result:
            if "ACTIVE" in value:
                value = 1
            else:
                value = 0
        # result = re.findall("(\d+)", value)
        # if result: value = float(value)
    except:
        raise
    finally:
        return value


# sed替换字符串
def cmdSedReplace(trackerList):
    try:
        cmdLine = "sed -i 's/tracker_server=.*/tracker_server=" + trackerList + "/g' " + client_file
        cmdResult = os.popen(cmdLine).readlines()
        print("cmdSedReplace=", cmdResult)
    except:
        raise


# 获取monitor内容并解析
def monitor(TRACKER_SERVER):
    group.clear()
    # 循环TRACKER_SERVER替换写入文件
    for trackerList in TRACKER_SERVER.split(';'):
        tracker = dict()
        tracker['tracker'] = trackerList
        print("trackerList: ", trackerList)
        try:
            cmdSedReplace(trackerList)
            cmdLine = "fdfs_monitor " + client_file
            cmdResult = os.popen(cmdLine).readlines()
            # print("cmdResult=", cmdResult)
            # cmdResult非空则当前tracker正常，解析返回数据
            if "tracker server" in '.'.join(cmdResult):
                print("connect to server ", trackerList, " ok")
                tracker['status'] = 1
                if not group: get_storage(cmdResult)
            else:
                print("connect to server ", trackerList, " fail")
                tracker['status'] = 0
        except:
            raise
        trackerServer['tracker'].append(tracker)


def get_storage(cmdResult):
    group_tag = False
    storage_tag = False
    group_list = []
    storage_list = []
    try:
        for line in cmdResult:
            # 如果解析到 Group 则解析group_list
            result = re.findall("Group (\d+)", line)
            # python2复制list new=old[:]
            # python3复制list new=old.copy()
            if result:
                group_tag = True
                print("Group=", formatValue(result[0]))
                group['group_no'] = formatValue(result[0])
                group["storage"] = []
                group_list = groupInfolist[:]
                continue
            # 如果解析到 Storage 则解析storage_list
            result = re.findall("Storage (\d+)", line)
            if result:
                storage_tag = True
                print("Storage=", formatValue(result[0]))
                storage['storage_name'] = "storage" + str(formatValue(result[0]))
                storage_list = storageInfolist[:]
                continue
            if group_tag:
                for groupInfo in group_list:
                    # 是否查找到key
                    if groupInfo in line:
                        # 删除已找到的key，减少下次循环
                        group_list.remove(groupInfo)
                        # 正则获取对应value
                        result = re.findall("%s = (.+)" % (groupInfo), line)
                        if result:
                            group[groupInfo] = formatValue(result[0])
                        # group_list解析完后，写入字典storageServer并停止解析
                        if 0 == len(group_list):
                            group_tag = False
                            tmp = group.copy()
                            storageServer["group"].append(tmp)
                        break
            if storage_tag:
                for storageInfo in storage_list:
                    if storageInfo in line:
                        storage_list.remove(storageInfo)
                        result = re.findall("%s = (.+)" % (storageInfo), line)
                        if result:
                            storage[storageInfo] = formatValue(result[0])
                        # storage_list解析完后，写入字典group并停止解析
                        if 0 == len(storage_list):
                            storage_tag = False
                            tmp = storage.copy()
                            group["storage"].append(tmp)
                            storage.clear()
                        break
    except:
        raise


def set_tracker():
    for tracker in trackerServer['tracker']:
        fastdfs_tracker_server_info.labels(tracker=tracker['tracker']).set(tracker['status'])


def set_storage():
    for group in storageServer['group']:
        fastdfs_group_info.labels(group=group['group name']).set(group['group_no'])
        fastdfs_storage_server_count.labels(group=group['group name']).set(group['storage server count'])
        fastdfs_active_server_count.labels(group=group['group name']).set(group['active server count'])
        fastdfs_disk_total_space.labels(group=group['group name']).set(group['disk total space'])
        fastdfs_disk_free_space.labels(group=group['group name']).set(group['disk free space'])
        for storage in group['storage']:
            fastdfs_storage_server_info.labels(group=group['group name'],
                                               storage=storage['storage_name'],
                                               ip=storage['id'], version=storage['version']).set(storage['ip_addr'])
            fastdfs_join_time.labels(group=group['group name'], storage=storage['storage_name'],
                                     ip=storage['id'], version=storage['version']).set(storage['join time'])
            if "up time" in storage.keys():
                fastdfs_up_time.labels(group=group['group name'], storage=storage['storage_name'],
                                       ip=storage['id'], version=storage['version']).set(storage['up time'])
            else:
                fastdfs_up_time.labels(group=group['group name'], storage=storage['storage_name'],
                                       ip=storage['id'], version=storage['version']).set(0)
            fastdfs_total_storage.labels(group=group['group name'], storage=storage['storage_name'],
                                         ip=storage['id'], version=storage['version']).set(storage['total storage'])
            fastdfs_free_storage.labels(group=group['group name'], storage=storage['storage_name'],
                                        ip=storage['id'], version=storage['version']).set(storage['free storage'])
            fastdfs_total_upload_count.labels(group=group['group name'],
                                              storage=storage['storage_name'],
                                              ip=storage['id'], version=storage['version']).set(
                storage['total_upload_count'])
            fastdfs_success_upload_count.labels(group=group['group name'],
                                                storage=storage['storage_name'], ip=storage['id'],
                                                version=storage['version']).set(storage['success_upload_count'])
            fastdfs_total_delete_count.labels(group=group['group name'],
                                              storage=storage['storage_name'],
                                              ip=storage['id'], version=storage['version']).set(
                storage['total_delete_count'])
            fastdfs_success_delete_count.labels(group=group['group name'],
                                                storage=storage['storage_name'], ip=storage['id'],
                                                version=storage['version']).set(storage['success_delete_count'])
            fastdfs_total_download_count.labels(group=group['group name'],
                                                storage=storage['storage_name'], ip=storage['id'],
                                                version=storage['version']).set(storage['total_download_count'])
            fastdfs_success_download_count.labels(group=group['group name'],
                                                  storage=storage['storage_name'], ip=storage['id'],
                                                  version=storage['version']).set(
                storage['success_download_count'])
            fastdfs_total_upload_bytes.labels(group=group['group name'],
                                              storage=storage['storage_name'],
                                              ip=storage['id'], version=storage['version']).set(
                storage['total_upload_bytes'])
            fastdfs_success_upload_bytes.labels(group=group['group name'],
                                                storage=storage['storage_name'], ip=storage['id'],
                                                version=storage['version']).set(storage['success_upload_bytes'])
            fastdfs_total_download_bytes.labels(group=group['group name'],
                                                storage=storage['storage_name'], ip=storage['id'],
                                                version=storage['version']).set(
                storage['stotal_download_bytes'])
            fastdfs_success_download_bytes.labels(group=group['group name'],
                                                  storage=storage['storage_name'], ip=storage['id'],
                                                  version=storage['version']).set(
                storage['success_download_bytes'])


@app.route("/metrics")
def ApiResponse():
    TRACKER_SERVER = os.getenv("TRACKER_SERVER")
    # TRACKER_SERVER = "192.168.10.64:22122;192.168.10.65:22122;192.168.10.69:22122;192.168.10.70:22122"
    monitor(TRACKER_SERVER)
    set_tracker()
    set_storage()
    return Response(generate_latest(REGISTRY), mimetype="text/plain")


@app.route('/health')
def index():
    return "FastDFS metrics"

# uwsgi --http :9018 --wsgi-file fastdfs.py --callable app
