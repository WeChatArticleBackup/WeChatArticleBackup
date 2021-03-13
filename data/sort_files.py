'''
Description: 
Autor: Au3C2
Date: 2021-03-13 10:10:59
LastEditors: Au3C2
LastEditTime: 2021-03-13 10:31:37
'''
from glob import glob
import os
from shutil import move as mv

authors = ['吃瓜群众','宁南山','政事堂']
rootpath = ''

for author in authors:
    filelist = glob(f'{author}/*.*')
    for filepath in filelist:
        name = os.path.basename(filepath)
        year, month, day = name[:4], name[4:6], name[6:8]
        if not os.path.exists(f'{author}/{year}'):
            os.mkdir(f'{author}/{year}')
        if not os.path.exists(f'{author}/{year}/{month}'):
            os.mkdir(f'{author}/{year}/{month}')
        newpath = f'{author}/{year}/{month}/{name[6:]}'
        mv(filepath,newpath)