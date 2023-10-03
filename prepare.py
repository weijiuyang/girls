import os 
from setting import *
import cv2
from PIL import Image
from extend import *
import shutil
from retrying import retry
import subprocess


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
            return_code = subprocess.run(['heif-enc', onemainimgpathnew])
            print("return code:", return_code)
            onemainimgpathnew = onemainimgpathnew.split('.')[0] + '.heic'
    return girls


@retry
def getalbumncover(girl = None):
    if girl == None:
        sql = "select address, photocount,id from albumn where is_exist = 1"
    else:
        sql = "select address, photocount,id from albumn where girl = '%s' and is_exist = 1" % girl
    # sql = "select address, photocount,id from albumn"
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
            if os.path.isdir(photopath) or 'mov' in photo.lower() or 'mp4' in photo.lower():
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
                    # maybe a gif or animate jpeg
                    try:
                        resized_image.save(thumbnail_photo_path)
                    except:
                        pass


def createalbum(girl = None,albumn = None):
    if girl == None:
        girls = os.listdir(girl_path)
        createthumbnail()
        pass
    else:
        sql = "select * from girl where name = '%s' " % girl
        # print(sql)
        # exit()
        mycursor.execute(sql)
        result = mycursor.fetchall()
        if not result:
            sql = "insert into girl (name) values ('%s')" % (girl)
            print(sql)
            mycursor.execute(sql)
            mydb.commit()

        albumns = []
        if albumn == None:
            one_albumns = os.listdir(os.path.join(girl_path,girl))
            one_albumns.sort()
            print(one_albumns)
            for albumn in one_albumns:
                temppath = os.path.join(girl_path,girl,albumn)
                if albumn[0] == '.' and not os.path.isdir(temppath):
                    os.remove(temppath)
                    # print(photo,'zzzzz')
                elif albumn == '_gsdata_':
                    shutil.rmtree(temppath)
                elif albumn == '.mainimg':
                    continue
                else:
                    albumns.append(albumn)
        else:
            albumns.append(albumn)
        print(albumns)
        # exit()
        for albumn in albumns:
            albumpath = os.path.join(girl_path,girl,albumn)
            print(albumpath)
            address = albumpath.lstrip(girl_path)
            print(address)
            institution,date,serial_number,name, photocount = parsealbumn(albumn,girl)
            print(institution,date,serial_number,name,photocount)
            # exit()
            sql = "select id from albumn where institution = '%s' and serial_number = '%s' and girl = '%s'" % (institution,serial_number,girl)
            print(sql)
            # exit()
            mycursor.execute(sql)
            result = mycursor.fetchall()
            # print(result)
            # exit()
            if not result:
                sql = "insert into albumn (institution,name,address,serial_number,girl,date,photocount,keywords,description)\
                      values ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
                        (institution,name,address,serial_number,girl, date,photocount,"","")
                print(sql)
                # exit()
                # print(date)
                mycursor.execute(sql)
                mydb.commit()
                sql = "select id from albumn where institution = '%s' and serial_number = '%s' and girl = '%s'" % (institution,serial_number,girl)
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
                # exit()
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
                if 'mov' in photo.lower() or 'mp4' in photo.lower():
                    continue
                # if photopath[-4:] == '.jpg' or photopath[-4:] == '.png':
                #     print(photopath,'not heic, wait ')
                #     # os.remove(photopath)
                #     continue
                serial_number,imagename = parsephoto(photo,albumn,girl)

                if 'jpg' in photopath:
                    print(os.path.join(albumpath,imagename))
                    print('jpgjpg')
                    # exit()

                    os.rename(photopath,os.path.join(albumpath,imagename))
                    realimagepahth  = os.path.join(albumpath,imagename)
                    return_code = subprocess.run(['heif-enc', realimagepahth])
                    print("return code:", return_code)
                    os.remove(realimagepahth)
                    address = realimagepahth.replace('jpg','heic').lstrip(girl_path)
                # exit()
                else:
                    address = photopath.lstrip(girl_path)


                sql = "select id from image where name = '%s' and serial_number = %s and girl = '%s'" % (name,serial_number, girl)
                print(sql)
                # exit()
                mycursor.execute(sql)
                result = mycursor.fetchall()
                print(result)
                print(address)

                # exit()
                if not result:
                    sql = "insert into image (name,address,albumn_id,serial_number,girl,date,keywords,description)\
                        values ('%s','%s',%s,%s,'%s','%s','%s','%s')" % \
                            (name,address,albumn_id,serial_number,girl, date,"","")
                    print(sql)
                    print(date)
                    mycursor.execute(sql)
                else:
                    print(result)
                    sql = "update image set address = '%s' where name = '%s' and serial_number = %s and girl = '%s' and albumn_id = %s" % (address,name,serial_number, girl,albumn_id)
                    # sql = "update image set albumn_id = %s where address = '%s' "% (albumn_id,address)
                    print(sql)
                    # exit()
                    mycursor.execute(sql)

                    mydb.commit()
        # createthumbnail(girl)
                

if __name__ == "__main__":
    mycursor = mydb.cursor()
    # createalbum("发条少女")
    createalbum('蠢沫沫')

    # createalbum('蠢沫沫', '蠢沫沫 NO.004 艾米利亚 [46P-591MB]')

    # getalbumncover()
    # createthumbnail('日奈娇')

    # createthumbnail('蠢沫沫')

