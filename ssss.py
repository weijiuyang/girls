
from flask import Flask,request,jsonify
import pymysql
import json
import requests
import urllib.parse

from datetime import datetime, timezone, timedelta
import logging

"""
    获取抖音 获取实时热点词, 需要douyinclient access_token, 详情见下面文档
    https://developer.open-douyin.com/docs/resource/zh-CN/dop/develop/openapi/data-open-service/hot-video-data/get-current-hot-words
"""

url = f'https://xingyunmanager.taiwu.com'
headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763",
            "Referer": "https://www.jpxgmn.com/"}  
response = requests.get(url, headers=headers)
print(url)
result = json.loads(response.text)
print(result)
exit()

url = f'https://xingyunmanager.taiwu.com/add'
url = f'http://10.10.201.24:1314/add'
data = {
    'emp_no': '001',
    'emp_name': 'John Doe',
    'team_no': 'S1',
    'team_name': 'Development',
    'team_role': 'Developer',
    'project_no': 'P001',
    'project_name': 'New Project',
    'phone': '1234567890',
    'password': 'password123'
}

response = requests.post(url, json=data)
print(url)
result = json.loads(response.text)
print(result)
hotlist = result['data']['list']
# exit()




print(len(hotlist))

for hot in hotlist:
    title = hot['sentence']
    original_string = title

    # 转义字符串
    escaped_string = urllib.parse.quote(original_string, safe='')

    print(escaped_string)
    video_url = f'https://open.douyin.com/hotsearch/videos/?hot_sentence={escaped_string}&access_token={access_token}&content-type=application/json'
    
    response = requests.get(video_url)
    print(url)
    result = json.loads(response.text)
    # print(result['data']['list'])
    videolist = result['data']['list']
    for video in videolist:
        print(video['title'])
    print(len(videolist))
    exit()
    
