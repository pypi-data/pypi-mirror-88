# __author:iseuwei
# data:2020/12/3

import shutil
import os
import pandas as pd
import requests
import yaml
import time
import shutil

from cnsenti import Sentiment

senti = Sentiment(pos='正面词汇.txt',  #正面词典txt文件相对路径
                  neg='负面词汇.txt',  #负面词典txt文件相对路径
                  merge=False,             #融合cnsenti自带词典和用户导入的自定义词典
                  encoding='utf-8')      #两txt均为utf-8编码

dirpath=r'E:\Iseuwei\WorkSpace\PyCharm\WeiboWap\WeiboWap\2018'
filepath='E:\Iseuwei\WorkSpace\PyCharm\WeiboDownload\微博topic2\广州方圆小学哮喘女孩遭体罚致吐血事件.xlsx'

filepath1='EE:\Iseuwei\WorkSpace\PyCharm\WeiboDownload\微博topic2\image\新文件夹/'
filepath2='E:\Iseuwei\WorkSpace\PyCharm\WeiboDownload\微博topic2\image\广州方圆小学哮喘女孩遭体罚致吐血事件'

rootPath='E:\Iseuwei\WorkSpace\PyCharm\WeiboDownload\微博topic2/'

# excel汇总去重
def huizong(dirpath):
    df_out=None
    print('Waiting...')
    for parent, dirnames, filenames in os.walk(dirpath):
        for file in filenames:
            imgName = os.path.splitext(file)[0]
            imgExt = os.path.splitext(file)[1]
            imgPath = os.path.join(parent, file).replace('\\', '/')
            print(imgPath)
            # df_in = pd.read_csv(imgPath)
            df_in = pd.read_excel(imgPath)
            print(df_in)
            if df_out is None:
                df_out=df_in
            else:
                df_out=pd.concat([df_out, df_in], axis=0, ignore_index=True)
    print('去重')
    df_out.drop_duplicates(subset=['id'], keep ='first', inplace = True)
    df_out.to_excel('search_汇总.xlsx', engine='xlsxwriter')


# 重命名
def mrename(filepath2):
    dirList=[]
    for parent, dirnames, filenames in os.walk(filepath2):
        dirList.append(parent)
    dirList=list(set(dirList))

    for dirPath in dirList:
        dirName=dirPath.split('/')[-1]
        index=0
        for parent, dirnames, filenames in os.walk(dirPath):
            for file in filenames:
                index+=1
                imgPath = os.path.join(parent, file).replace('\\', '/')
                newPath=dirName+'/'+parent.split('\\')[-1]+str(index)+'.jpg'
                # print(imgPath)
                # print(newPath)
                os.rename(imgPath, newPath)


# 创建指定目录
def mkDir(dir):
    if os.path.exists(dir):
        return
        shutil.rmtree(dir)
    os.mkdir(dir)


def request_download(IMAGE_URL):

    r = requests.get(IMAGE_URL)
    with open('./image/img2.jpg', 'wb') as f:
        f.write(r.content)

# 微博关键词下载
def ImgDownload(filepath):
    print('Waiting...')
    df_in=pd.read_excel(filepath)
    for index, row in df_in.iterrows():
        print(index)
        if index < 1:
            continue
        mid=str(row['mid'])
        img_list=None
        try:
            img_list = row['img_urls']
            if type(img_list) != str:
                continue
            img_list=yaml.safe_load(img_list)
        except Exception as e:
            print(e)
            continue

        print(img_list)
        # continue
        try:
            for img_url in img_list:
                save_path=rootPath + '广州方圆小学哮喘女孩遭体罚致吐血事件/' + mid
                img_path=save_path + '/' + img_url.split('/')[-1]
                print(save_path, img_path)
                mkDir(save_path)
                r = requests.get(img_url)
                time.sleep(2)
                with open(save_path+'/'+img_url.split('/')[-1], 'wb') as f:
                    f.write(r.content)
        except Exception as e:
            print(e)
        # if not isinstance (img_list,list):
        #     continue


def wordList():
    posstr='''进步、优点、吸引力、有利、获益、信心、鼓舞、辉煌、繁荣、促进、提高、突破、慈善、称赞、赞美、建设性、创造性、创造力、革新、有效、提高效率、增强、卓越、优秀、涨幅、荣誉、荣耀、表彰、机会、机遇、超越、正面、积极、声望、威信、赢得、显著、影响深远、意义重大、历史性、红利、入选、利好、
盈利、收入增长、资金充裕、稳健、成本下降、佳绩、
领先、龙头、热销、好评、品牌、口碑、消费者依赖、位居前茅、重大突破、自主创新、开拓者、
涨停、逆势上涨、增持、
模范、楷模、影响力、洞察力、领导力、独立、
胜诉、获得赔偿
'''
    negstr='''冲突、混乱、失败、不合理、异议、严峻、阻碍、失效、问题、严重、不健全、加剧、过度、
亏损、损失、亏空、破产、财务困难、危机、赤字、困境、巨额债务、不佳、下滑、资金链紧张、资金链断裂、资金断裂、造假、粉饰报表、伪造、欺诈、虚构、虚增、虚报、操纵、违规、违法、虚假、高估、不实、丑闻、舞弊、业绩变脸、推迟披露、
风险、短板、管理不善、被曝、有失公允、负担、损害、喊停、萎缩、滑铁卢、安全隐患、事故、劣势、召回、不利、缺陷、惨淡、闲置、积压、滞销、减产、停产、冻结、
警告、退市、摘牌、崩盘、停牌、套现、跌停、超跌、大盘、减持、抛售、风险警示、
内幕交易、国有资产流失、挪用、偷税、漏税、涉嫌、串通、骗局、失职、腐败、
诉讼、起诉、纠纷、指控、涉案、处罚、证监会、非法、谴责、败诉
'''
    posList=[x.strip() for x in posstr.split('、')]
    negList=[x.strip() for x in negstr.split('、')]
    for word in negList:
        print(word)

def test():
    df_out = pd.DataFrame(
        columns=['mid', 'user_id', 'user_name', 'idendity', 'member', 'weibo_stamp', 'weibo_date', 'weibo_time',
                 'source', 'original', 'content', 'retweet_count', 'comment_count', 'like_count', 'topics', 'at_users',
                 'retweet', 'pos_word', 'neg_word', 'pos', 'neg'])
    df_in=pd.read_excel('E:\Iseuwei\WorkSpace\PyCharm\WeiboDownload/证券时报2018词频.xlsx')
    print(df_in)
    for index, row in df_in.iterrows():
        # row['pos_word'] = None
        # row['neg_word'] = None
        # row['pos'] = None
        # row['neg'] = None
        try:
            content = row['content']
            print(index, content)
            if '万科' in content:
                df_out.loc[len(df_out)] = row
            # # result1 = senti.sentiment_count(content)
            # result2 = senti.sentiment_count(content)
            # print(result2)
            # row['pos_word']=result2['pos']
            # row['neg_word'] = result2['neg']
            # if result2['pos']>result2['neg']:
            #     row['pos']=1
            #     row['neg'] = -1
            # elif result2['pos']<result2['neg']:
            #     row['pos']=-1
            #     row['neg'] = 1
            # else:
            #     row['pos']=0
            #     row['neg'] = 0

        except:
            pass
        # df_out.loc[len(df_out)] = row

    df_out.to_excel('df_out.xlsx')

def test2():
    df_out = pd.DataFrame(
        columns=['mid', 'user_id', 'user_name', 'idendity', 'member', 'weibo_stamp', 'weibo_date', 'weibo_time',
                 'source', 'original', 'content', 'retweet_count', 'comment_count', 'like_count', 'topics', 'at_users',
                 'retweet', 'pos_word', 'neg_word', 'pos', 'neg'])
    df_in=pd.read_excel('E:\Iseuwei\WorkSpace\PyCharm\WeiboDownload/证券时报2018词频.xlsx')
    print(df_in)
    for index, row in df_in.iterrows():
        # row['pos_word'] = None
        # row['neg_word'] = None
        # row['pos'] = None
        # row['neg'] = None
        try:
            content = row['content']
            print(index, content)
            if '万科' in content:
                df_out.loc[len(df_out)] = row
            # # result1 = senti.sentiment_count(content)
            # result2 = senti.sentiment_count(content)
            # print(result2)
            # row['pos_word']=result2['pos']
            # row['neg_word'] = result2['neg']
            # if result2['pos']>result2['neg']:
            #     row['pos']=1
            #     row['neg'] = -1
            # elif result2['pos']<result2['neg']:
            #     row['pos']=-1
            #     row['neg'] = 1
            # else:
            #     row['pos']=0
            #     row['neg'] = 0

        except:
            pass
        # df_out.loc[len(df_out)] = row

    df_out.to_excel('df_out.xlsx')



if __name__ == '__main__':
    # ImgDownload(filepath)

    huizong(dirpath)

    # mrename(filepath2)

    # request_download('https://ww2.sinaimg.cn/orj360/006bRCrmly1gg7szgmzshj30o00ja43m.jpg')
    #
    # wordList()