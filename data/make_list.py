'''
Description: 
Autor: Au3C2
Date: 2020-11-20 19:25:23
LastEditors: Au3C2
LastEditTime: 2021-01-11 23:47:23
'''
import os
import re
from glob import glob

import numpy as np
import pandas as pd

# authors = ['吃瓜群众专栏pro','宁南山','政事堂2019']

rootpath = ''

htmllist = glob(f'{rootpath}*/*.html')
jpglist = glob(f'{rootpath}*/*.JPG')
filelist = htmllist + jpglist

#文件重命名并获取月份信息
for filepath in filelist:
    filepath_new = filepath.replace('\\','/').replace('？','').replace('！','!').replace('，',',').replace('”',"'").replace('“',"'").replace('（',"(").replace('）',")").replace(' ',"_")
    os.rename(filepath, filepath_new)

htmllist = glob(f'{rootpath}*/*.html')
data = pd.DataFrame(columns=['author','date','title','comment'])
for htmlpath in htmllist:
    htmlpath = htmlpath.replace('\\','/')
    author = htmlpath.split('/')[-2]
    filename = os.path.basename(htmlpath)
    title = filename.replace('.html','')
    date = title[:8]
    ym = title[:6]
    commentpath = htmlpath.replace('.html','-评论.JPG')
    if os.path.exists(commentpath):
        comment = True
    else:
        comment = False
    data = data.append({'author':author,'ym':ym,'date':date,'title':title,'file':htmlpath,'comment':comment},ignore_index=True)

# data['date'] = pd.to_datetime(data['date'],format='%Y%m%d')
data[['author','ym','date','title']] = data[['author','ym','date','title']].astype(str)
data['comment'] = data['comment'].astype(bool)
data.to_excel('./data/list.xlsx')
# data = data.groupby(['date','author'])
ymlist = np.sort(np.unique(data['ym'].values))[::-1]
authors =np.sort(np.unique(data['author'].values))

# data.set_index('author',inplace=True)

index_fp = open('./data/index.md','w',encoding='utf8')
for ym in ymlist:
    index_fp.write(f'# {ym[:4]}年\n\n## {ym[4:]}月\n\n')
    data_ym = data[data['ym']==ym]
    data_ym.reset_index(inplace=True, drop=True)
    for author in authors:
        index_fp.write(f'### {author}\n\n')
        articles = data[data['ym']==ym]
        articles = articles[articles['author']==author].sort_values(['date'],ascending=False)
        filelist = articles['file'].values
        datelist = articles['date'].values
        # articles.reset_index()
        # titles = np.sort(aticles['title'].values)
        for i in range(len(articles)):
            with open(filelist[i],'r',encoding='utf8') as html:
                for line in html:
                    title = re.findall(r'<title>(.*?)</title>', line,re.I)
                    if title != []:
                        title = title[0]
                        break
            index_fp.write(f'* [{datelist[i]}-{title}]({filelist[i]})\n')
            pass
        index_fp.write('\n')
    # htmlpath_new = htmlpath.replace('\\','/').replace('？','').replace('！','!').replace('，',',').replace('”',"'").replace('“',"'")
    # os.rename(htmlpath, htmlpath_new)
    # htmlname = os.path.basename(htmlpath).replace('.html','')
index_fp.close()
# comment 
# <p align="center"><img width: 75%; max-width: 75%; height: auto; src="-评论.JPG" alt="comment"></p>
