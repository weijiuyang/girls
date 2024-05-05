import os
from config import *

print(os.listdir(previewpath))


for one in os.listdir(previewpath):
    os.rename(os.path.join(previewpath, one), os.path.join(previewpath, one).replace('jpg','webp'))