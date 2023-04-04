import os 
from setting import *
import cv2
from PIL import Image
from extend import *
import shutil
from retrying import retry

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


@retry
def getalbumncover():
    sql = "select address, photocount,id from albumn"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    print(result)
    for albumn in result:
        print(albumn)
        allpath = os.path.join(girl_path,albumn[0])
        if not os.path.exists(allpath):
            continue
                # print(os.path.join(allpath,albumn[0].split('/')[-1] + ' ' + 'cover.jpg'))
        coverpath = os.path.join(allpath,albumn[0].split('/')[-1] + ' ' + 'cover.jpg')
        if os.path.isfile(coverpath):
            print(True,albumn)

            image = Image.open(coverpath)
            if image.mode == "RGBA":
                image = image.convert("RGB")
            # 缩小图片尺寸
            width, height = image.size
            if width > 1066:
                while width > 1066:
                    width = int(width * 0.5)
                    height = int(height * 0.5)
                resized_image = image.resize((width, height))

                # 保存缩小后的图片文件
                resized_image.save(coverpath)
        elif os.path.exists(os.path.join(allpath,albumn[0].split('/')[-1] + ' ' + '1.jpg')):
            if os.path.isfile(os.path.join(allpath,albumn[0].split('/')[-1] + ' ' + '%s.jpg'%str(int(albumn[1])+1))):
                shutil.copy(os.path.join(allpath,albumn[0].split('/')[-1] + ' ' + '%s.jpg'%str(int(albumn[1])+1)),os.path.join(allpath,albumn[0].split('/')[-1] + ' ' + 'cover.jpg'))
            elif os.path.exists(os.path.join(allpath,albumn[0].split('/')[-1] + ' ' + '%s.jpg'% albumn[1])) and os.path.getsize(os.path.join(allpath,albumn[0].split('/')[-1] + ' ' + '%s.jpg'% albumn[1])) < os.path.getsize(os.path.join(allpath,albumn[0].split('/')[-1] + ' ' + '1.jpg')):
                shutil.copy(os.path.join(allpath,albumn[0].split('/')[-1] + ' ' + '%s.jpg'% albumn[1]),os.path.join(allpath,albumn[0].split('/')[-1] + ' ' + 'cover.jpg'))
            else:
                shutil.copy(os.path.join(allpath,albumn[0].split('/')[-1] + ' ' + '1.jpg'),os.path.join(allpath,albumn[0].split('/')[-1] + ' ' + 'cover.jpg'))

def createthumbnail(girl = None):
    if girl == None:
        sql = "select address, photocount,id from albumn where is_exist = 1"
    else:
        sql = "select address, photocount,id from albumn where girl = '%s' and is_exist = 1" % girl
    mycursor.execute(sql)
    result = mycursor.fetchall()
    print(result)
    for albumn in result:
        print(albumn)
        albumn_path = os.path.join(girl_path,albumn[0])
        thumbnail_albumn_path = os.path.join(girl_thumbnail_path,albumn[0])
        if not os.path.exists(thumbnail_albumn_path):
            os.makedirs(thumbnail_albumn_path)

        if not os.path.exists(albumn_path):
            continue
                # print(os.path.join(allpath,albumn[0].split('/')[-1] + ' ' + 'cover.jpg'))
        photos = os.listdir(albumn_path)
        print(photos)
        for photo in photos:
            print(photo)
            photopath = os.path.join(albumn_path,photo)
            print(photopath)
            if os.path.isdir(photopath):
                continue

            thumbnail_photo_path = os.path.join(thumbnail_albumn_path,photo)
            if not os.path.exists(thumbnail_photo_path):
                image = Image.open(photopath)
                if image.mode == "RGBA":
                    image = image.convert("RGB")
                # 缩小图片尺寸
                width, height = image.size
                if width > 200:
                    while width > 200:
                        width = int(width * 0.5)
                        height = int(height * 0.5)
                    resized_image = image.resize((width, height))

                    # 保存缩小后的图片文件
                    resized_image.save(thumbnail_photo_path)



# print(getmainimg())

def createalbum(girl = None):
    if girl == None:
        girls = os.listdir(girl_path)
        createthumbnail()
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
        one_albumns = os.listdir(os.path.join(girl_path,girl))
        print(one_albumns)
        # exit()
        albumns = []
        for albumn in one_albumns:
            temppath = os.path.join(girl_path,girl,albumn)
            if albumn[0] == '.' and not os.path.isdir(temppath):
                os.remove(temppath)
                # print(photo,'zzzzz')
            elif albumn == '_gsdata_':
                shutil.rmtree(temppath)
            else:
                albumns.append(albumn)
        albumns = [ _ for _ in albumns if not _[0] == '.']
        print(albumns)
        # exit()
        for albumn in albumns:
            albumpath = os.path.join(girl_path,girl,albumn)
            print(albumpath)
            address = albumpath.lstrip(girl_path)
            print(address)

                # exit()
            institution,date,serial_number,name, photocount = parsealbumn(albumn,girl)
            print(institution,date,serial_number,name,photocount)
            # exit()
            print()
            sql = "select id from albumn where institution = '%s' and serial_number = '%s'" % (institution,serial_number)
            print(sql)
            mycursor.execute(sql)
            result = mycursor.fetchall()
            if not result:
                sql = "insert into albumn (institution,name,address,serial_number,girl,date,photocount,keywords,description)\
                      values ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
                        (institution,name,address,serial_number,girl, date,photocount,"","")
                print(sql)
                # exit()
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

                sql = "update albumn set photocount = %s  where institution = '%s' and serial_number = '%s'"% (photocount,institution,int(serial_number))
                print(sql)
                mycursor.execute(sql)
                mydb.commit()
            
                # pass
                # continue
                # sql = "update albumn set name = '%s',address = '%s',serial_number ='%s',girl = '%s',date = '%s',photocount ='%s',\
                #       keywords ='%s',description ='%s'" %(name,address,serial_number,girl,date,photocount,"","")
                # mycursor.execute(sql)
            photos = os.listdir(albumpath)
            print(photos)
            # exit()
            for photo in photos:
                photopath = os.path.join(albumpath,photo)
                print(photopath)
                if os.path.isdir(photopath):
                    print(photopath,'album, not a photo,have passed')
                    continue
                if photo[0] == '.':
                    os.remove(photopath)
                    print(photo,'hiddenfile, have delete ')

                    continue
                if photopath[-4:] == '.txt' or photopath[-4:] == '.url':
                    print(photopath,'other file, have delete ')
                    os.remove(photopath)
                    continue
                
                serial_number,imagename = parsephoto(photo,albumn,girl)
                print(os.path.join(albumpath,imagename))
                # exit()
                os.rename(photopath,os.path.join(albumpath,imagename))
                print(serial_number,imagename)
                address = os.path.join(albumpath,imagename).lstrip(girl_path)

                sql = "select id from image where name = '%s' and serial_number = %s" % (name,serial_number)
                print(sql)
                mycursor.execute(sql)
                result = mycursor.fetchall()
                if not result:
                    sql = "insert into image (name,address,albumn_id,serial_number,girl,date,keywords,description)\
                        values ('%s','%s',%s,%s,'%s','%s','%s','%s')" % \
                            (name,address,albumn_id,serial_number,girl, date,"","")
                    print(sql)
                    print(date)
                    mycursor.execute(sql)
                else:
                    print(result)
                    sql = "update image set albumn_id = %s where address = '%s' "% (albumn_id,address)
                    print(sql)
                    mycursor.execute(sql)

                mydb.commit()
        createthumbnail(girl)
                
                # exit()

        


if __name__ == "__main__":
    mycursor = mydb.cursor()
    createalbum("蠢沫沫")
    # pass
    # getalbumncover()
    # createthumbnail('蠢沫沫')

