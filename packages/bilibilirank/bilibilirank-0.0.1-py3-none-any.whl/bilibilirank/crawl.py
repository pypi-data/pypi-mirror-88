# -*- coding:utf-8 -*-

# __author:ly_peppa
# date:2020/12/10

# 导入必要的几个包
import requests
from bs4 import BeautifulSoup
import pandas as pd



# 定义映射表
key_map=dict(zip(['全站','番剧','国产动画','国创相关','纪录片','动画','音乐','舞蹈','游戏','知识','数码','生活','美食','鬼畜','时尚','娱乐','影视','电影','电视剧','原创','新人'],
                 ['all','bangumi','guochan','guochuang','documentary','douga','music','dance','game','technology','digital','life','food','kichiku','fashion','ent','cinephile','movie','tv','origin','rookie']))

def PopularRank(keyword='全站'):
    '''
    下载bilibili排行榜数据，
    :return:
    返回pandas格式的数据
    '''
    df_rank = pd.DataFrame(columns=['排名', '标题', '网址', '播放量', '弹幕量', 'UP主/收藏量', '综合得分'])     # 指定列名构造pandas表格
    response=requests.get('https://www.bilibili.com/v/popular/rank/{:s}'.format(key_map[keyword]))        # requests向url网址发送get请求获返回网页数据
    response.encoding='utf-8'                                       # 设置字符集
    soup = BeautifulSoup(response.text, "html.parser")              # 使用BeautifulSoup解析web网页
    rank_list = soup.find('ul', attrs={'class': 'rank-list'}).find_all('li', attrs={'class': 'rank-item'})  # find()找到指定的节点
    for item in rank_list:                      # 遍历该节点，解析每一行数据
        num=item.div.text.strip()               # 解析出排名
        info=item.find('div', class_='info')
        title=info.a.text.strip()               # 解析出标题
        link='https:'+info.a['href']            # 解析出链接
        detail=item.find('div', class_='detail').find_all('span')
        play = detail[0].text.strip()           # 解析出播放量
        view = detail[1].text.strip()           # 解析出弹幕量
        name = detail[2].text.strip()           # 解析出UP主名字
        pts=item.find('div', class_='pts')
        score=pts.div.text.strip()              # 解析出综合得分

        row = [num, title, link, play, view, name, score]
        # print(row)
        df_rank.loc[len(df_rank)]=row           # 解析出来的数据按行追加到DataFrame表中
    df_rank.set_index('排名',drop=True,append=False,inplace=True,verify_integrity=False)  # 设置索引
    return df_rank

def PopularHot(pn=None):
    '''
    下载bilibili综合热门数据，
    :return:
    返回pandas格式的数据
    '''
    hot_list = None
    pn_count=0
    while True if pn is None else (pn_count<pn):
        pn_count+=1
        response=requests.get('https://api.bilibili.com/x/web-interface/popular?ps=50&pn={:d}'.format(pn_count))        # requests向url网址发送get请求获返回网页数据
        response.encoding='utf-8'                                       # 设置字符集
        data_json=response.json()['data']
        if data_json['no_more']:
            break
        if hot_list is None:
            hot_list=data_json['list']
        else:
            hot_list.extend(data_json['list'])
    df=pd.DataFrame(data=hot_list)
    df.set_index('aid',drop=True,append=False,inplace=True,verify_integrity=False)  # 设置索引
    return df

def PopularHistory():
    '''
    下载bilibili入站必刷数据，
    :return:
    返回pandas格式的数据
    '''
    response = requests.get('https://api.bilibili.com/x/web-interface/popular/precious?page_size=100&page=1')  # requests向url网址发送get请求获返回网页数据
    response.encoding = 'utf-8'  # 设置字符集
    hot_list = response.json()['data']['list']
    df=pd.DataFrame(data=hot_list)
    df.set_index('aid',drop=True,append=False,inplace=True,verify_integrity=False)  # 设置索引
    return df


def PopularWeekly(number=1):
    '''
    下载bilibili每周必看数据，
    :return:
    返回pandas格式的数据
    '''
    response = requests.get('https://api.bilibili.com/x/web-interface/popular/series/one?number={:d}'.format(number))  # requests向url网址发送get请求获返回网页数据
    response.encoding = 'utf-8'  # 设置字符集
    hot_list = response.json()['data']['list']
    df=pd.DataFrame(data=hot_list)
    df.set_index('aid',drop=True,append=False,inplace=True,verify_integrity=False)  # 设置索引
    return df


if __name__ == '__main__':

    df_rank=PopularRank('全站')
    print(df_rank)
    df_rank.to_csv('bilibilirank.csv',encoding="utf-8-sig")         # pandas直接保存到csv

    df = PopularHot()
    print(df)
    df.to_excel('bilibili_hot.xlsx')

    df = PopularHistory()
    print(df)
    df.to_excel('bilibili_history.xlsx')

    df = PopularWeekly()
    print(df)
    df.to_excel('bilibili_weekly.xlsx')