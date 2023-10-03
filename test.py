
import subprocess
import os 
oripath = r'/home/vajor/t7/girls/蠢沫沫/蠢沫沫 NO.004 艾米利亚 [46P-591MB]'

print(os.listdir(oripath))

newpath = os.listdir(oripath)
for path in newpath:
# for 
    imagepath = os.path.join(oripath, path)
    print(imagepath)
    # exit()
    return_code = subprocess.run(['heif-enc', imagepath])
    print("return code:", return_code)


