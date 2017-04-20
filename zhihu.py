#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import analyzeUser
import loginOperator
import ConfigParser
import io

@click.command()
@click.option("--target", default = "nologin", help = "Please choose login or nologin")
@click.option("--name", default   = "toocooltohavefriends", help = "Please choose a url name in www.zhihu.com")
@click.option("--console",default = "", help = "Login Mode, what To do")
def cmd(target,name,console):
    if target == "nologin":
        nologin = analyzeUser.analyseUser(name)
        nologin.getBasicMsg()
        print("基本信息：")
        print ("关注： " + str(nologin.following) + " 被关注： " + str(nologin.followed))
        print ("话题： " + str(nologin.topic) + " 专栏： " + str(nologin.column))
        print ("问题： " + str(nologin.question) + " 收藏夹： " + str(nologin.collectbox))
        print ("被感谢： " + str(nologin.thanked) + " 被收藏： " + str(nologin.collected))
        print ("编辑： " + str(nologin.edit) + " 被赞同： " + str(nologin.righted))
        print ("回答数据汇总：")
        nologin.getAnswerData()
        nologin.getFollowersData()
        print("关注者数据汇总：")
        print("男性关注者：" + str(nologin.followers['male']) + " 女性关注者：" + str(nologin.followers['female']))
        print("二度关注者：" + str(nologin.followers['follower_count']) + " 二度回答：" + str(nologin.followers['answer_count']))
    elif target  == "login":
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.read("fuck.ini")
        au    = config.get("USER","authorization")
        xu    = config.get("USER","x-udid")
        name  = config.get("USER", "name")
        login = loginOperator.loginOperator(au,xu,name)
        if console == "stopFollowers":
            login.stopFollowers()
        elif console == "stopFollowTopics":
            login.stopFollowTopics()
        elif console == "stopFollowQuestions":
            login.stopFollowQuestions()
        elif console == "deleteActivities":
            login.deleteActivities()
        else:
            print(console + " is a undefined console!")



if __name__ == "__main__":
    cmd()
