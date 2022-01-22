'''
Description: 
Autor: Au3C2
Date: 2020-11-20 19:25:23
LastEditors: Au3C2
LastEditTime: 2021-12-23 00:06:59
'''
import os
import re
from glob import glob

import numpy as np
import pandas as pd

from shutil import move as mv

authors = ['吃瓜群众','宁南山','政事堂']

rootpath = ''

htmllist = glob(f'{rootpath}*/*.html')
jpglist = glob(f'{rootpath}*/*.JPG')

#文件重命名并获取月份信息
for i,htmlpath in enumerate(htmllist):
    htmlpath_new = htmlpath.replace('\\','/').replace('？','').replace('！','!').replace('，',',').replace('”',"'").replace('“',"'").replace('（',"(").replace('）',")").replace(' ',"_").replace('：',"_")
    htmllist[i] = htmlpath_new
    os.rename(htmlpath, htmlpath_new)

index_fp = open('./data/index.md','a+',encoding='utf8')

for author in authors:
    filelist = glob(f'{author}/*.html')
    jpglist = glob(f'{author}/*.JPG')
    for filepath in filelist:
        name = os.path.basename(filepath)
        year, month, day = name[:4], name[4:6], name[6:8]
        if not os.path.exists(f'{author}/{year}'):
            os.mkdir(f'{author}/{year}')
        if not os.path.exists(f'{author}/{year}/{month}'):
            os.mkdir(f'{author}/{year}/{month}')
        title = name[6:].replace('.html','')
        if jpglist:
            with open(filepath,'a+',encoding='utf8') as html:
                html.seek(0,2) # 文件指针移动到末尾
                html.write('\n')
                html.write(f'<p align="center"><img width: 75%; max-width: 75%; height: auto; src="{title}-评论.JPG" alt="comment"></p>')
            mv(jpglist[0],f'{author}/{year}/{month}/{title}-评论.JPG')
        newpath = f'{author}/{year}/{month}/{name[6:]}'
        mv(filepath,newpath)
        index_fp.write(f'* [{title}]({newpath})\n')
index_fp.close()