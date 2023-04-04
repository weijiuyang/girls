#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 09:02:16 2020

@author: vajorstack
"""

import shutil
import os
import re
import sys

def remove(model, photodir = None):
    #基础配置
    path=r"/home/vajor/images"   
    backpath=r"/home/vajor/backup"  
    dirs=os.listdir(path)
    print(dirs)
    for folder in dirs:
        # print(folder)
        if (len(folder)>10):
            pader=os.path.join(path,folder)
            paders=os.listdir(pader)
            # print(paders)
            num=len(paders)
            reg="[0-9]+P"
            # print(folder)
            pages_group=re.search(reg,folder)
            # print(pages_group)
            page_num = int(pages_group.group()[:-1])
            
            if model == 'delete'or model[0]=='d':
                for name in paders:
                    paders_name=os.path.join(pader,name)
                    # 删掉所有图片
                    if os.path.isfile(paders_name):
                        os.remove(paders_name)   
                #将图片文件夹从image移动到backup
                print('remove '+folder+' to backup')
                shutil.move(pader,os.path.join(backpath,folder))
            elif num + 1 >= int(page_num): 
                print('the current num is %s , the page_num is %s '%(num, page_num) + folder + 'to be hold')
                pass         
                # for name in paders:
                #     paders_name=os.path.join(pader,name)
                #     # 删掉所有图片
                #     if os.path.isfile(paders_name):
                #         os.remove(paders_name)   
                # #将图片文件夹从image移动到backup
                # print('remove '+folder+' to backup')
                # shutil.move(pader,os.path.join(backpath,folder))
            elif model == 'break' or model[0]=='b':
                    print('the current num is %s , the page_num is %s '%(num, page_num))
                    # continue
                    for name in paders:
                        paders_name=os.path.join(pader,name)
                        # 删掉所有图片
                        if os.path.isfile(paders_name):
                            os.remove(paders_name)     
                    print('delete '+folder)
                    os.rmdir(pader) 
                # if model == 'working'or model[0]=='w':
                #     # photodir
                #     pass
                





if __name__ == "__main__":
    model = sys.argv[1]
    remove(model)

    

