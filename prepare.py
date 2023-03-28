import os 
from setting import *
import cv2
from PIL import Image
from extend import *

def getmainimg():
    girls = os.listdir(girl_path)
    for girl in girls:
        girlpath = os.path.join(girl_path,girl)
        print(girlpath)
        mainimgpath = os.path.join(girlpath,"mainimg")
        if not os.path.isdir(mainimgpath):
            os.mkdir(mainimgpath)
        mainimgs = os.listdir(mainimgpath)
        for onemainimg in  mainimgs:
            onemainimgpathold = os.path.join(mainimgpath,onemainimg)
            # print(onemainimgpath)
            onemainimgpathnew = onemainimgpathold.replace(' ','_')
            onemainimgpathnew = onemainimgpathnew.replace('(','')
            onemainimgpathnew = onemainimgpathnew.replace(')','')

            os.rename(onemainimgpathold,onemainimgpathnew)
            image = Image.open(onemainimgpathnew)


            # 缩小图片尺寸
            width, height = image.size
            while width > 1600:
                width = int(width * 0.5)
                height = int(height * 0.5)
                resized_image = image.resize((width, height))

                # 保存缩小后的图片文件
                resized_image.save(onemainimgpathnew)



            # 获取文件大小（以字节为单位）
            file_size = os.stat(onemainimgpathnew).st_size

            # 将字节数转换为Kilobytes并打印
            print("File size is:", round(file_size/1024, 2), "KB")


    print(girls)
    # girls = ""
    return girls



# print(getmainimg())


def createalbum(girl = None):
    if girl == None:
        girls = os.listdir(girl_path)
        pass
    else:

        sql = "select * from girl where name = '%s' " % girl
        mycursor.execute(sql)
        result = mycursor.fetchall()
        if not result:
            sql = "insert into girl (name) values ('%s')" % (girl)
            print(sql)
            mycursor.execute(sql)
            mydb.commit()
        # exit()
        albumns = os.listdir(os.path.join(girl_path,girl))
        albumns = [ _ for _ in albumns if not _[0] == '.']
        print(albumns)
        for albumn in albumns:
            albumpath = os.path.join(girl_path,girl,albumn)
            print(albumpath)
            address = albumpath.lstrip(girl_path)
            print(address)
            # exit()
            institution,date,serial_number,name, photocount = parsealbumn(albumn,girl)
            print(institution,date,serial_number,name,photocount)
            print()
            sql = "select id from albumn where institution = '%s' and serial_number = '%s'" % (institution,serial_number)
            print(sql)
            mycursor.execute(sql)
            result = mycursor.fetchall()
            if not result:
                sql = "insert into albumn (institution,name,address,serial_number,girl,date,photocount,keywords,description)\
                      values ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
                        (institution,name,address,serial_number,girl, date,photocount,"","")
                # print(sql)
                # print(date)
                mycursor.execute(sql)
                mydb.commit()
                sql = "select id from albumn where institution = '%s' and serial_number = '%s'" % (institution,serial_number)
                # print(sql)
                mycursor.execute(sql)
                result = mycursor.fetchall()
                albumn_id = result[0][0]
                # print(albumn_id)
                print("1111")
            else:
                # print(result)
                albumn_id = result[0][0]
                # print(albumn_id)
                # print("2222")
                # exit()
                # pass
                # continue
                # sql = "update albumn set name = '%s',address = '%s',serial_number ='%s',girl = '%s',date = '%s',photocount ='%s',\
                #       keywords ='%s',description ='%s'" %(name,address,serial_number,girl,date,photocount,"","")
                # mycursor.execute(sql)
            # exit()
 


            print("333")
            photos = os.listdir(albumpath)
            print(photos)
            # exit()
            for photo in photos:
                photopath = os.path.join(albumpath,photo)
                print(photopath)
                if photopath[-4:] == '.txt':
                    os.remove(photopath)
                    continue
                serial_number,imagename = parsephoto(photo,albumn,girl)
                print(os.path.join(albumpath,imagename))
                # exit()
                os.rename(photopath,os.path.join(albumpath,imagename))
                print(serial_number,imagename)
                address = os.path.join(albumpath,imagename).lstrip(girl_path)
                # exit()
                print(address)
                # exit()
                
                print()
                sql = "select id from image where albumn_id = %s and serial_number = %s" % (albumn_id,serial_number)
                print(sql)
                mycursor.execute(sql)
                print("ssss")

                result = mycursor.fetchall()
                if not result:
                    sql = "insert into image (name,address,albumn_id,serial_number,girl,date,keywords,description)\
                        values ('%s','%s',%s,%s,'%s','%s','%s','%s')" % \
                            (name,address,albumn_id,serial_number,girl, date,"","")
                    print(sql)
                    print(date)
                    print("ssss")
                    mycursor.execute(sql)
                else:
                    print(result)
                mydb.commit()
                print("Ssss")
                
                # exit()

        


if __name__ == "__main__":
    mycursor = mydb.cursor()
    createalbum("鱼子酱")
    pass

