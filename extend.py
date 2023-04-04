from setting import *
import re
import os 
import cv2
from PIL import Image

def getgirls():
    girls_name = os.listdir(girl_path)
    girls = []
    for girl in girls_name:
        onegirl = []
        onegirl.append(girl)
        girlpath = os.path.join(girl_path,girl)
        mainimgpath = os.path.join(girlpath,".mainimg")
        mainimgs = os.listdir(mainimgpath)
        for onemainimg in  mainimgs:
            onemainimgpathold = os.path.join(mainimgpath,onemainimg)
            # print(onemainimgpath)
            onemainimgpathnew = onemainimgpathold.replace(' ','_')
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
            
            mainpath = "../static/images/girls/" + onemainimgpathnew.lstrip(girl_path)
        # print(onegirl)
        girls.append([onegirl,mainpath])
    print(girls)
    # girls = ""
    return girls

def parsealbumn(albumn,girl):

    print(albumn)
    # exit()
    institution,date,number,name,photocount = None,"1000-01-01",None,None,None
    try:
        institution,date,number,name,photocount = albumn.split()
        print('ssss')
        if date[0] == 'N':
            name = number + name
            number = date
            date = "1000-01-01"
            print( institution,date,number,name,photocount) 
    except Exception as e:
        print(e)
        temp = albumn.split('[')[0]
        temp = temp.split('【')[0]
        templist = temp.split()
        institution = templist[0]
        number = templist[1]
        name = ' '.join(templist[2:])

    albumpath = os.path.join(girl_path,girl,albumn)
    photocount = len(os.listdir(albumpath))
    print(photocount)
    institution =  institutionrename(institution)
    number = numberrename(number)
    # if albumn == '桜桃喵 NO.040 小小少女 少女私房 [50P-442MB]':
    #     print('uuu')
    #     print(institution)
    #     exit()

    if not date == None:
        date = timerename(date)

    return institution,date,number,name,photocount

def institutionrename(institution):
    if "XIUREN".lower() in institution.lower():
        return "秀人网"

    if "FEILIN".lower() in institution.lower():
        return "嗲囡囡"
    
    if "MyGirl".lower() in institution.lower():
        return "美媛馆"  
    if institution  == '桜井宁宁':
        return '桜井宁宁'
    if institution  == '桜桃喵':
        return '桜桃喵'
    if institution  == '日奈娇':
        return '日奈娇'
    if '过期米线' in institution:
        return '过期米线'



def parsephoto(photo,albumn,girl):
    print(photo,albumn,girl)
    if "cover" in photo:
        return 0,albumn +' cover.jpg'
    for suffix in [".jpg",".png",".jpeg"]:
        photo = photo.rstrip(suffix)
    print(photo)

    for delimiter in "_- ":
        if delimiter in photo:
            photo = photo.split(delimiter)[-1]
            print(photo)
    # exit()
    pattern = r'\d+'
    match = re.search(pattern,photo)
    serialnumber = int(match.group())
    print(serialnumber,str(serialnumber),albumn +' ' + str(serialnumber) + '.jpg')
    # exit()
    return serialnumber,albumn +' ' + str(serialnumber) + '.jpg'
    
def numberrename(number):
    pattern = r'\d+'
    match = re.search(pattern,number)
    return match.group()

def timerename(time):
    return time.replace(".","-")


# def keywordsdrop(string):
#     """" 处理不需要关键字 """
#     if string in keyworddrop :
#         return False, ""
    
#     """" 移除日语  """
#     if not removejap(string):
#         return False, ""
    
#     """ 替换"""
#     if string in keywordreplace:
#         string = keywordreplace[string]

#     return True, string

# """" 读取文件，分割成各个部分 """
# def divide(essaypath):
#     with open(essaypath, "r") as f :
#         temp = f.readlines()
#     index = 0
#     while temp[index] == "\n":
#         index += 1
#     title = temp[index].strip()
#     index += 1
#     while temp[index] == "\n":
#         index += 1
#     writeragin = temp[index].strip()
#     index += 1
#     while temp[index] == "\n":
#         index += 1
#     website = temp[index].strip()
#     index += 1
#     while temp[index] == "\n":
#         index += 1
#     description = ""    
#     while temp[index][0] != "#":
#         description += temp[index]
#     # print(description.strip(),index) 
#         index += 1
#     description = description.strip()

#     keywords = set()

    # while temp[index] == "\n":
    #     index += 1
    # print(index)
    while temp[index][0] == "#":

        """
            用下面的方法，太慢了
        """
        # str = temp[index][1:].strip()

        # jap = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\uAC00-\uD7A3]')  # \uAC00-\uD7A3为匹配韩文的，其余为日文
        # if jap.search(str):
        #     print('Yes')
        keyword = temp[index][1:].strip()
        keyword_list = re.split("[/ ,]", keyword)
        # keyword_list = keyword.split("",",s")
        for keyword in keyword_list:
            isdrop, waitkeywords = keywordsdrop(keyword)
        if isdrop :
            keywords.add(waitkeywords)
        index += 1
    # print(keywords)                                                   
    while temp[index] == "\n":
        index += 1
    content = "".join(temp[index:])  
    # print(content)
    return title, website, description, keywords, content 


def easydivide(essaypath):
    with open(essaypath, "r") as f :
        temp = f.readlines()
    index = 0
    if temp[index][0] == "第" or  "(":
        index += 1                                                 
    while temp[index] == "\n":
        index += 1
    title = temp[index].strip()
    index += 1
    content = "".join(temp[index:])  
    return title, content 

def linkaudio(path):
    # allpath = os.path.join(publication_path,path) 
    title, content = easydivide(path)
    # audio = re.compile(r'“([^”]*)”')  
    audio = re.compile("\\“(?:(?!\\”).)*(\\,|\\~|\\。|\\！|\\？|(\\……))”");
    audiolist = []
    for match in audio.finditer(content): # content为需要查找的内容
        currentaudio = match.group()[1:-1]
        if len(currentaudio) > 4:
            # audiopathabsolute = "/home/vajor/books/static/audio/" + currentaudio + ".mp3"
            audiopath = "../static/audio/" + path[:-4] + '/' + currentaudio[:80] + ".mp3"
            print(audiopath)
            audiolist.append((audiopath, currentaudio))
    content = re.sub(audio, audiore,content)
    return title,content,audiolist

def audiore(match):
    audio = match.group()
    return '<a onclick="playAudio(\'%s\')">'%audio[1:-1] + audio + "</a>"
