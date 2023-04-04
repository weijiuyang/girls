import os
import shutil

from extend import *
from setting import *


"""
the program offer some webapi about essay and wait

"""
mycursor = mydb.cursor()


""""  girl 详情 """
def getgirl(girl,page):
    print(girl,page)
    
    # return None
    
    sql = "select id, institution,name,address,serial_number,girl,date,photocount,level,keywords,description from albumn where girl = '%s' and is_exist = 1 limit %s,12" % (girl,int(page)*12-12)
    print(sql)
    
    mycursor.execute(sql)
    albumns = mycursor.fetchall()
    print(len(albumns))
    """
        可以优化
    """
    albumns = [list(res) for res in albumns] 
    for albumn in albumns:
        albumn_id, institution,name,address,serial_number,girl,date,photocount,level,keywords,description = albumn
        albumn.append(address+ address.lstrip(girl)+' cover.jpg')
        print(albumn)
        # print(albumn_id, institution,name,address,serial_number,girl,date,photocount,level,keywords,description)
        
    # print(albumns)
    print(len(albumns))


    return albumns


""""  girl 详情 """
def getalbumn(albumn_id):
    sql = "select name,address,serial_number,girl,date,level,keywords,description from image where albumn_id = '%s' and is_exist = 1" % (albumn_id)
    print(sql)
    
    mycursor.execute(sql)
    images = mycursor.fetchall()
    return images





def delete_essay(essay_id):
    sql = "update essay set is_exist = 0 where essay_id=%s" % essay_id
    mycursor.execute(sql)
    mydb.commit()
    
def delete_wait(id):
    sql = "update wait set is_exist = 0 where id=%s" % id
    mycursor.execute(sql)
    mydb.commit()

def save_wait(id):
    sql = "update wait set is_exist = 2 where id=%s" % id
    mycursor.execute(sql)
    mydb.commit()

def coadvance(essay_id):
    sql = "select id,title from essay where series_id = (select series_id from essay\
                where id = %s)" % essay_id
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return result






