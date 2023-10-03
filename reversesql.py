import os
import os 
from setting import *
import cv2
from PIL import Image
from extend import *
import shutil
from retrying import retry

mycursor = mydb.cursor()

girl = '发条少女'
sql = "select * from girl where name = '%s' " % girl
sql = "select address, photocount,id from albumn where girl = '%s' and is_exist=1" % girl
mycursor.execute(sql)
result = mycursor.fetchall()

# print(result)
# print(sql)
# exit(result)
for one in result:
    # print(one)
    path = os.path.join(girl_path,one[0])
    # print(path)
    if os.path.isdir(path) == False :
        print('tt')
        # exit()
        print(os.path.isdir(path))
        sql = "update albumn set is_exist = 0 where id = %s " % one[2]
        mycursor.execute(sql)
    mydb.commit()

sql = 'SELECT id FROM girls.albumn where is_exist=0;'

mycursor.execute(sql)
result = mycursor.fetchall()
for one in result:
    print(one)
    sql = "update image set is_exist = 0 where albumn_id = %s " % one[0]
    mycursor.execute(sql)
mydb.commit()




