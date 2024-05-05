import pymysql
# 创建连接
mydb = pymysql.connect(
    host="127.0.0.1",
    port=3306, 
    user='root', 
    passwd='vajors123',
    db='girls')
# 创建游标(查询数据返回为元组格式)
#mydb = conn.cursor()


path = r"/home/vajor/t7/albumn"
previewpath = r"/home/vajor/t7/preview"

girl_path = '/home/vajor/t7/girls'
girl_origin_path = '/home/vajor/t7/girls_origin'
girl_thumbnail_path = '/home/vajor/t7/girls_thumbnail'

headers = { "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "Referer":'https://www.text-to-speech.cn/?user_id=de7a64bb5f5611bb',
            "Host": "www.text-to-speech.cn",
            "Origin": "https://www.text-to-speech.cn",
            "cookie": "X_CACHE_KEY=1a2935c904b302fa2af05abc66956db9; kbitrate=audio-16khz-32kbitrate-mono-mp3; language=; pitch=-11; role=0; speed=-2; style=0; voice=zh-CN-YunfengNeural; Hm_lpvt_5a701c66b9f669402a583d455eb47da5=1676553802; Hm_lvt_5a701c66b9f669402a583d455eb47da5=1676545517"  
            } 


