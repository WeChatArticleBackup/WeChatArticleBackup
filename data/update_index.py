'''
Description: 
Autor: Au3C2
Date: 2020-11-20 19:25:23
LastEditors: Au3C2
LastEditTime: 2022-03-12 10:35:01
'''
import os
import re
from glob import glob

import numpy as np
import pandas as pd

from shutil import move as mv

authors = ['吃瓜群众','宁南山','政事堂']

index_fp = open('./data/index.md','a+',encoding='utf8')

for author in authors:
    filelist = glob(f'{author}/*.html')
    imglist = glob(f'{author}/*.JPG') + glob(f'{author}*/*.PNG') + \
        glob(f'{author}*/*.JPEG') + glob(f'{author}*/*.jpg') + \
        glob(f'{author}*/*.jpeg') + glob(f'{author}*/*.png')
    for filepath in filelist:
        name = os.path.basename(filepath)
        year, month, day = name[:4], name[4:6], name[6:8]
        if not os.path.exists(f'{author}/{year}'):
            os.mkdir(f'{author}/{year}')
        if not os.path.exists(f'{author}/{year}/{month}'):
            os.mkdir(f'{author}/{year}/{month}')
        title = name[6:].replace('.html','')
        if imglist:
            img_format = imglist[0].split('.')[-1]
            with open(filepath,'a+',encoding='utf8') as html:
                html.seek(0,2) # 文件指针移动到末尾
                html.write('\n')
                html.write(f'<p align="center"><img width: 75%; max-width: 75%; height: auto; src="{title}-评论.{img_format} alt="comment"></p>')
            mv(imglist[0],f'{author}/{year}/{month}/{title}-评论.{img_format}')
        newpath = f'{author}/{year}/{month}/{name[6:]}'
        mv(filepath,newpath)
        index_fp.write(f'* [{title}]({newpath})\n')
index_fp.close()