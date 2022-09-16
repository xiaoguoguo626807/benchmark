#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python

import re
import sys
import json
import os

def analyze(model_name, batch_size, log_file, res_log_file, device_num):
    time_pat = re.compile(r"ips: (.*) images/s")
    
    logs = open(log_file).readlines()
    logs = ";".join(logs)
    time_res = time_pat.findall(logs)

    print("---device_num: ", device_num)
    index_c = device_num.index('C')
    print("---index_c: ", index_c)
    gpu_num = int(device_num[index_c + 1:len(device_num)])
    print("-----gpu_num: ", gpu_num)

    fail_flag = 0
    fp_item = "fp32"
    ips = 0

    if time_res == []:
        fail_flag = 1
    else:
        skip_num = 4
        total_ips = 0
        for i in range(skip_num, len(time_res)):
            total_ips += float(time_res[i])
        ips = total_ips / (len(time_res) - skip_num)
    info = {    "model_branch": os.getenv('model_branch'),
                "model_commit": os.getenv('model_commit'),
                "model_name": model_name,
                "batch_size": batch_size,
                "fp_item": fp_item,
                "run_mode": "DP",
                "convergence_value": 0,
                "convergence_key": "",
                "ips": ips * gpu_num,
                "speed_unit":"images/s",
                "device_num": device_num,
                "model_run_time": os.getenv('model_run_time'),
                "frame_commit": "",
                "frame_version": os.getenv('frame_version'),
        }
    json_info = json.dumps(info)
    with open(res_log_file, "w") as of:
        of.write(json_info)

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage:" + sys.argv[0] + " model_name path/to/log/file path/to/res/log/file")
        sys.exit()

    model_name = sys.argv[1]
    batch_size = sys.argv[2]
    log_file = sys.argv[3]
    res_log_file = sys.argv[4]
    device_num = sys.argv[5]

    analyze(model_name, batch_size, log_file, res_log_file, device_num) 