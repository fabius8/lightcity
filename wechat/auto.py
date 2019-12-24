#!/usr/bin/env python3
# - *- coding: utf- 8 - *-
import requests
import time
import sys

userlist = []
new_useridlist = []

welcome = "Hi，亲，请问是需要高德点亮城市吗? 可以帮您免费点亮1个城市哦~"
howmuch = "Hi，请问是需要高德点亮城市吗? 点亮1座城市收费1元，现在可以免费领取1个任意城市点亮喔~\n另外打包价20元30个。30元50个。40元70个。50元90个。60元110个。70元130个。80元150个。90元170个。100元190个。110元210个。120元230个。130元250个。140元270个。150元290个。160元310个。170元330个。180元350个。190元370个(全亮)\n请提供您的高德登录信息（在账户与安全里设置密码），谢谢~~"


class sendMsg:
    def __init__(self):
        pass

    def sendmsg(self, userId, content):
        """
        """
        data = {'userId': userId,
                'content': content}
        URL = 'http://localhost:52700/wechat-plugin/send-message'
        r = requests.post(url=URL, data=data)
        if r.ok:
            return True
        else:
            return False


class User:
    def __init__(self):
        pass

    def user(self):
        """
        """
        URL = 'http://localhost:52700/wechat-plugin/user'
        r = requests.get(url=URL)
        if r.ok:
            return r.json()
        else:
            None


def init_userlist():
    info = User()
    info = info.user()
    if info is None:
        return
    for i in info:
        if i['userId'] not in userlist:
            userlist.append(i['userId'])


if __name__ == '__main__':
    print("running...")
    init_userlist()
    user = User()
    sendMsg = sendMsg()
    tmpmsg = ""
    while True:
        time.sleep(10)
        try:
            info = user.user()
            if info is None:
                continue
            for i in info:
                if i['userId'] not in userlist:
                    print(i['userId'], i['title'], "is a new user",)
                    userlist.append(i['userId'])
                    new_useridlist.append(i['userId'])
                    tmpmsg = i['subTitle']
            if len(new_useridlist) == 0:
                continue
            for userid in new_useridlist:
                print("send msg")
                sendMsg.sendmsg("wxid_mvl7o57opos421", userid+": "+tmpmsg)
                time.sleep(5)
                sendMsg.sendmsg(userid, welcome)
            new_useridlist = []

        except Exception as err:
            new_useridlist = []
            print(err)
