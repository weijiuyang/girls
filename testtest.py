from flask import Flask, render_template, request, jsonify
from multiprocessing import Pool
import redis
import os,datetime

path = '/home/vajor/t7/albumn'
infos = os.listdir(path)
# print(infos)
red = redis.Redis(host='localhost', port=6379, db=10)
red9 = redis.Redis(host='localhost', port=6379, db=9)

red11 = redis.Redis(host='localhost', port=6379, db=11)

nowdate = datetime.datetime.now().date().strftime("%Y%m%d")
 
# 检查现有的键类型
key_type = red9.type(nowdate).decode('utf-8')
print(f"当前键 '{nowdate}' 的类型是: {key_type}")

# 如果键的类型不是 list，删除该键
if key_type != 'set':
    print(f"删除键 '{nowdate}'，因为其类型是 {key_type}。")
    red9.delete(nowdate)


for info in infos:
    # print(info, red.get(info))
    red9.sadd(nowdate, info)

    print(red11.get(info))
    # print(red.get(info))
    if not red.get(info):
        print(info)
        # red.set(info, 50)
        # red11.set(info, 'xgmn')








