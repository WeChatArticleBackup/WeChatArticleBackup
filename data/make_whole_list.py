'''
Description: 
Autor: Au3C2
Date: 2020-11-20 19:25:23
LastEditors: Au3C2
LastEditTime: 2021-09-05 16:06:40
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

# for i,jpgpath in enumerate(jpglist):
#     jpgpath_new = jpgpath.replace('\\','/').replace('？','').replace('！','!').replace('，',',').replace('”',"'").replace('“',"'").replace('（',"(").replace('）',")").replace(' ',"_")
#     jpglist[i] = jpgpath_new
#     os.rename(jpgpath, jpgpath_new)

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
        if jpglist:
            with open(filepath,'a+',encoding='utf8') as html:
                jpgname = name[6:].replace('.html','')
                html.seek(0,2) # 文件指针移动到末尾
                html.write('\n')
                html.write(f'<p align="center"><img width: 75%; max-width: 75%; height: auto; src="{jpgname}-评论.JPG" alt="comment"></p>')
            mv(jpglist[0],f'{author}/{year}/{month}/{jpgname}-评论.JPG')
        newpath = f'{author}/{year}/{month}/{name[6:]}'
        mv(filepath,newpath)
        
        
htmllist = glob(f'{rootpath}*/*/*/*.html')
jpglist = glob(f'{rootpath}*/*/*/*.JPG')

# for i,htmlpath in enumerate(htmllist):
#     htmlpath_new = htmlpath.replace('\\','/').replace('？','').replace('！','!').replace('，',',').replace('”',"'").replace('“',"'").replace('（',"(").replace('）',")").replace(' ',"_").replace('：',"_")
#     htmllist[i] = htmlpath_new
#     os.rename(htmlpath, htmlpath_new)

# for i,jpgpath in enumerate(jpglist):
#     jpgpath_new = jpgpath.replace('\\','/').replace('？','').replace('！','!').replace('，',',').replace('”',"'").replace('“',"'").replace('（',"(").replace('）',")").replace(' ',"_").replace('：',"_")
#     jpglist[i] = jpgpath_new
#     os.rename(jpgpath, jpgpath_new)

data = pd.DataFrame(columns=['author','date','title','comment'])
for htmlpath in htmllist:
    htmlpath = htmlpath.replace('\\','/')
    author = htmlpath.split('/')[0]
    year = htmlpath.split('/')[1]
    month = htmlpath.split('/')[2]
    filename = os.path.basename(htmlpath)
    day = filename[:2]
    title = filename[3:].replace('.html','')
    date = ''.join([year,month,day])
    ym = ''.join([year,month])
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
            # 利用正则查找title
            with open(filelist[i],'r',encoding='utf8') as html:
                html.seek(0,0)
                html_data = list()
                title_flag = False
                for line in html:
                    if not title_flag:
                        title = re.findall(r'<title>(.*?)</title>', line,re.I)
                        if title != []:
                            title = title[0]
                            title_flag = True
                            break
                    # if f'{datelist[i]}-' in line:
                    #     line = line.replace(datelist[i],datelist[i][-2:])
                    # html_data.append(line)
            # with open(filelist[i],'w',encoding='utf8') as html:
            #     html.writelines(html_data)
                    
            index_fp.write(f'* [{datelist[i][-2:]}-{title}]({filelist[i]})\n')

        index_fp.write('\n')
    # htmlpath_new = htmlpath.replace('\\','/').replace('？','').replace('！','!').replace('，',',').replace('”',"'").replace('“',"'")
    # os.rename(htmlpath, htmlpath_new)
    # htmlname = os.path.basename(htmlpath).replace('.html','')
index_fp.close()
# comment 
# <p align="center"><img width: 75%; max-width: 75%; height: auto; src="-评论.JPG" alt="comment"></p>
