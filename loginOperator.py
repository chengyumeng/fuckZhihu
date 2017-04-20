#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests
from pprint import pprint
import cookielib
import time
import os.path
import json

class loginOperator(object):

    headers = {
            'Referer':'https://www.zhihu.com',
            'Host':'www.zhihu.com',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.3',
            'Accept':'application/json,text/plain,*/*',
            "Accept-Encoding":"gzip, deflate, sdch, br",
            "authorization":"oauth c3cef7c66a1843f8b3a9e6a1e3160e20",
            "x-udid":"AJDA0p9FzQqPTg5Gz85xEdkfmXRfr7Q9rd0=",
            "Cookie":"aliyungf_tc=AQAAAJg0LG1yGQEAeV70bo5FFtg3XU/B; q_c1=7fbc36ab1b7c4374baa0948fa159bc87|1492443356000|1492443356000"
            }

    def __init__(self,authorization,x_uuid,name):
        self.headers['authorization'] = authorization
        self.headers['x-uuid']        = x_uuid
        self.name    = name
        self.session = requests.session()

    def get_xsrf(self):
        index_url = "https://www.zhihu.com"
        page      = self.session.get(index_url,headers = self.headers).text
        _xsrf     = re.findall(r'name="_xsrf" value="(.*?)"',page)
        return _xsrf[0]

    def stopFollowers(self):
        offset = 0 
        step  = 20
        is_over = False
        while(is_over == False):
            url    = "https://www.zhihu.com/api/v4/members/" + self.name + "/followees?include=data[*].gender,badge[?(type=best_answerer)].topics&offset=" + str(offset) + "&limit=" + str(step)
            page   = self.session.get(url,headers = self.headers).content
            target = json.loads(page)
            if (target['paging']['is_end'] == True):
                is_over = True
            for v in target['data']:
                self.stopFollow(v['url_token'])        

    def stopFollow(self,name):
        url  = "https://www.zhihu.com/api/v4/members/" + str(name) + "/followers"
        page = self.session.delete(url,headers = self.headers).content

    def stopFollowTopics(self):
        is_over = False
        while(is_over == False):
            url = "https://www.zhihu.com/api/v4/members/" + self.name + "/following-topic-contributions?include=data[*].topic.introduction&offset=0&limit=20"
            page   = self.session.get(url,headers = self.headers).content
            target = json.loads(page)
            if (target['paging']['is_end'] == True):
                is_over = True
            for v in target['data']:
                self.stopFollowTopic(v['topic']['url'])

    def stopFollowTopic(self,url):
        url  = url + "/followers"
        page = self.session.delete(url,headers = self.headers).content

    def stopFollowQuestions(self):
        is_over = False
        while(is_over == False):
            url = "https://www.zhihu.com/api/v4/members/" + self.name + "/following-questions?include=data[*].created,author&offset=0&limit=20"
            page   = self.session.get(url,headers = self.headers).content
            target = json.loads(page)
            if (target['paging']['is_end'] == True):
                is_over = True
            for v in target['data']:
                self.stopFollowQuestion(v['id'])

    def stopFollowQuestion(self,qid):
        url = "https://www.zhihu.com/api/v4/questions/" + str(qid) + "/followers"
        page = self.session.delete(url,headers = self.headers).content

    def deleteActivities(self):
        is_over = False
        while (is_over == False):
            url = "https://www.zhihu.com/api/v4/members/" + self.name + "/activities?limit=20&after_id=1491060699&desktop=True"
            page = self.session.get(url,headers = self.headers).content
            target = json.loads(page)
            if (target['paging']['is_end'] == True):
                is_over = True
            for v in target['data']:
                if v['verb'] == "ANSWER_VOTE_UP":
                    self.doNotAgree(v['target']['id'])
                elif v['verb'] == "MEMBER_VOTEUP_ARTICLE":
                    self.doNotAgreeArticle(v['target']['id'])
                elif v['verb'] == "ANSWER_CREATE":
                    self.deleteAnswer(v['target']['id'],v['target']['question']['id'])
                    

    def doNotAgree(self,answer_id):
        url = "https://www.zhihu.com/api/v4/answers/" + str(answer_id) + "/voters"
        payload = json.dumps({"type":"neutral"})
        page = self.session.post(url,headers = self.headers,data = payload).content
    
    def doNotAgreeArticle(self,article_id):
        url  = "https://www.zhihu.com/api/v4/articles/" + str(article_id) + "/likers"
        page = self.session.delete(url,headers = self.headers).content

    def deleteAnswer(self,answer_id,question_id):
        url  = "https://www.zhihu.com/api/v4/answers/" + str(answer_id)
        page = self.session.delete(url,headers = self.headers).content
        print("删除回答的题目： https://www.zhihu.com/question/" + str(question_id))


if __name__ == '__main__':
    au = "Bearer Mi4wQUFDQWZfVkhBQUFBVU1KWTZEdWZDeVlBQUFCZ0FsVk5vSkVkV1FDVEJhSm1KZkQ0MXZxenZwMENKTGdPX2JleTdB|1492650396|5a673bbe0a2392d344f3820fb078dee2439da317"
    xu = "AEBCLN5MoguPTn6ll5L9zlaAkJL8FelnXfQ="
    a = loginOperator(au,xu,'toocooltohavefriends')
    a.deleteActivities()
