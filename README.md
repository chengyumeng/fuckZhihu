#  fuckZhihu 批量进行知乎操作的利器
![fuckZHihu](https://github.com/Chengyumeng/fuckZhihu/blob/master/logo.jpeg)

## 执行未登录操作
```console
$ python zhihu.py --target=nologin --name=toocooltohavefriends
$ # 对应用户：https://www.zhihu.com/people/toocooltohavefriends
$ # 您可以对zhihu.py做逻辑上修改适应自定义应用场景
```

## 执行登录操作
- 配置文件 fuck.ini 相关配置令牌可以在Chrome登录用户状态下从请求header中获取
- 操作介绍

```console
$ python zhihu.py --target=login --console=stopFollowers
$ # 取关所有已关注者
```

```console
$ python zhihu.py --target=login --console=stopFollowTopics
$ # 取关所有已关注话题
```

```console
$ python zhihu.py --target=login --console=stopFollowQuestions
$ # 取关所有已关注问题
```

```console
$ python zhihu.py --target=login --console=deleteActivities
$ # 删除所有时间线记录
```

## TODO
- 增加流程，可单独删掉全部回答
- 清空时间线的时候可以备份
- 根据时间做处理

## BUG
- 网络存在问题下抛出异常
- ...

## 欢迎关注微信公众账号：程天写代码
![guojingcoooool](https://github.com/Chengyumeng/spider163/blob/master/wechat.jpeg)



