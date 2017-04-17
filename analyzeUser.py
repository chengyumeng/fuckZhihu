#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from pprint import pprint
import re
import json

class analyseUser(object):
    headers = {
            'Referer':'https://www.zhihu.com',
            'Host':'www.zhihu.com',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
            'Accept':'application/json,text/plain,*/*',
            "Accept-Encoding":"gzip, deflate, sdch, br",
            "authorization":"oauth c3cef7c66a1843f8b3a9e6a1e3160e20",
            "x-udid":"AJDA0p9FzQqPTg5Gz85xEdkfmXRfr7Q9rd0=",
            "Cookie":"aliyungf_tc=AQAAAJg0LG1yGQEAeV70bo5FFtg3XU/B; q_c1=7fbc36ab1b7c4374baa0948fa159bc87|1492443356000|1492443356000"
            }
    numbers = r"\d+"
    following  = 0   # 关注人数
    followed   = 0   # 被关注人数
    topic      = 0   # 关注话题数量
    column     = 0   # 关注专栏数量
    question   = 0   # 关注问题数量
    collectbox = 0   # 关注收藏夹数量
    thanked    = 0   # 被感谢数量
    collected  = 0   # 被收藏数量
    edit       = 0   # 编辑网站频数
    righted    = 0   # 被赞同数量

    def __init__(self,name):
        self.name    = name
        self.session = requests.session()

    def getBasicMsg(self):
        url   = "https://www.zhihu.com/people/" + self.name + "/activities"
        page  = BeautifulSoup(self.session.get(url,headers = self.headers).content,"lxml")
        tag0 = page.find('div',{'class':'Profile-sideColumnItemValue'}).text
        tag1 = page.find('a',{'class':'Profile-sideColumnItemLink'}).text 
        tag2 = page.find('div',{'class':'IconGraf'}).text
        number    = page.find_all('div',{'class':'NumberBoard-value'})
        self.following = number[0].text
        self.followed  = number[1].text
        data     = page.find_all('span',{'class':'Profile-lightItemValue'})
        self.topic       = data[0].text
        self.column      = data[1].text
        self.question    = data[2].text
        self.collectbox  = data[3].text
        patten = re.compile(self.numbers)
        data0 = patten.findall(tag0)
        data1 = patten.findall(tag1)
        data2 = patten.findall(tag2)
        self.thanked   = data0[0]
        self.collected = data0[1]
        self.edit      = data1[0]
        self.righted   = data2[0]

    def getAnswerData(self):
        url = "https://www.zhihu.com/api/v4/members/" + self.name + "/answers?include=data[*].is_normal,suggest_edit,comment_count,can_comment,content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,relationship.is_authorized,voting,is_author,is_thanked,is_nothelp,upvoted_followees;data[*].author.badge[?(type=best_answerer)].topics&offset=0&limit=15&sort_by=created"
        page = self.session.get(url,headers = self.headers).content
        target = json.loads(page)
        data = target['data']
        for v in data:
            print(v['question']['title'])
            print(str(v['voteup_count']))
            print(str(v['updated_time']))
            self.getVoterData(v['id'])

    def getVoterData(self,answer_id):
        offset  = 0
        step    = 20
        is_over = False
        answer_count   = []
        articles_count = []
        follower_count = []
        while (is_over == False):
            url = "https://www.zhihu.com/api/v4/answers/" + str(answer_id) + "/voters?include=\
                   data[*].answer_count,articles_count,follower_count,gender,is_followed,is_following,\
                   badge[?(type=best_answerer)].topics&offset=" + str(offset) +  "&limit=" + str(step)
            page = self.session.get(url,headers = self.headers).content
            target = json.loads(page)
            data = target['data']
            for v in data:
                answer_count.append(v['answer_count'])
                articles_count.append(v['articles_count'])
                follower_count.append(v['follower_count'])
            if(target['paging']['is_end'] == True):
                is_over = True
            offset = offset + step    
        return {'answer_count':answer_count,'articles_count':articles_count,'follower_count':follower_count}

    def getFollowersData(self):
        start   = 20
        step    = 20
        is_over = False
        rt = {'male':0,'female':0,'follower':0,'answer':0}
        while (is_over == False):
            url = "https://www.zhihu.com/api/v4/members/" + self.name + "/followers?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,\
                   badge[?(type=best_answerer)].topics&offset=" + str(start) + "&limit=" + str(step)
            page = self.session.get(url,headers = self.headers).content
            target = json.loads(page)
            if(target['paging']['is_end'] == True):
                is_over = True
            start = start + step
            data = target['data']
            for v in data:
                if (v['gender'] == -1):
                    rt['female'] = rt['female'] + 1
                elif (v['gender'] == 1):
                    rt['male'] = rt['male'] + 1
                rt['follower'] = rt['follower'] + v['follower_count']
                rt['answer']   = rt['answer'] + v['answer_count']
        pprint(rt)
        return rt



a = analyseUser("toocooltohavefriends")
#a.getBasicMsg()
#a.getAnswerData()
a.getFollowersData()
