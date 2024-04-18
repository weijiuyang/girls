from flask import Flask, render_template, request, jsonify
from multiprocessing import Pool
import redis
import os

path = '/home/weijiuyang/spider/image'
infos = os.listdir(path)
# print(infos)
red = redis.Redis(host='localhost', port=6379, db=10)

# records = red.hgetall(code)
# exit()
for info in infos:
    # print(info, red.get(info))
    if not red.get(info):
        print(info)
        red.set(info, 50)
exit()

for info in infos:
    red.set(info, 50)








