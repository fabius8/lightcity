#!/usr/bin/env python3
# - *- coding: utf- 8 - *-

import json
import os
from urllib import request, parse
import argparse
import xml.etree.cElementTree as ET
import time
import re
import wda
import sys
import applescript
import socket


def check_running():
    while True:
        try:
            global hyf_suo
            hyf_suo = socket.socket()
            addr = ('', 9999)
            hyf_suo.bind(addr)
            break
        except Exception as err:
            print(time.strftime("%Y-%m-%d %H:%M:%S",
                                time.localtime()), err)
            time.sleep(5)
            continue


check_running()

bundle_id = 'com.autonavi.amap'

parser = argparse.ArgumentParser("lightcity.py city.json")
parser.add_argument("cityjson", help="convert json to gpx.", type=str)
parser.add_argument("--start", default=1, help="City start number", type=int)
parser.add_argument("--auto", default=1, help="auto login", type=int)
parser.add_argument("--freq", default=2, help="cycle how many times", type=int)
parser.add_argument("--keeptime", default=63, help="keep time", type=int)
args = parser.parse_args()
cityjson = args.cityjson
result = re.search('(1.*)_(.*).json', cityjson)
username = result.group(1)
passwd = result.group(2)
citygpx = "city.gpx"
start = args.start
auto = args.auto
freq = args.freq
keeptime = args.keeptime
print("Input:", cityjson, "Output:", citygpx, "Start:", start, "Auto:", auto,
      "Freq:", freq, "Keeptime:", keeptime, "Username:",
      username, "Password:", passwd)


def program_exit(err):
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
          err)
    sys.exit()


def amap_login(c, s):
    s(name=u'我的').tap()
    time.sleep(5)
    s(name=u'登录后开启足迹地图').tap()
    time.sleep(1)
    s(name=u'其他登录方式').tap()
    # time.sleep(1)
    s(name=u'密码登录').tap()
    s(type='TextField').set_text(username+'\n')
    time.sleep(2)
    s(type='SecureTextField').set_text(passwd+'\n')
    # time.sleep(1)
    s(name=u'登录').tap()
    # time.sleep(2)
    s(name=u'返回').tap()
    time.sleep(5)
    login_image = username + "-" + time.strftime("%Y%m%d-%H%M%S") + "-login" + ".png"
    c.screenshot(login_image)
    cmd = "mkdir -p image/" + username + ";"
    cmd += "mv " + login_image + " image/" + username
    os.system(cmd)
    # time.sleep(2)
    s(name=u'首页').tap()
    # time.sleep(1)
    s(name=u'我的位置').tap()


def amap_loginout(c, s, end):
    s(name=u'我的').tap()
    time.sleep(3)
    if end == 1:
        logout_image = username + "-" + time.strftime("%Y%m%d-%H%M%S") + "-logout" + ".png"
        c.screenshot(logout_image)
        cmd = "mkdir -p image/" + username + ";"
        cmd += "mv " + logout_image + " image/" + username
        os.system(cmd)
    s(name=u'设置').tap()
    time.sleep(1)
    if s(name=u'退出登录').exists:
        s(name=u'退出登录').tap()
        # time.sleep(1)
        s(name=u'退出').tap()
        time.sleep(1)
        s.close()
        time.sleep(1)
    else:
        s.close()
        time.sleep(1)


class Geocoding:
    def __init__(self, api_key):
        self.api_key = api_key

    def geocode(self, address):
        """
        """
        geocoding = {'s': 'rsv3',
                     'key': self.api_key,
                     'city': '全国',
                     'address': address}
        geocoding = parse.urlencode(geocoding)
        req = request.Request("%s?%s" % ("http://restapi.amap.com/v3/geocode/geo", geocoding))
        ret = request.urlopen(req)

        if ret.getcode() == 200:
            res = ret.read()
            json_obj = json.loads(res)
            if json_obj['status'] == '1' and int(json_obj['count']) >= 1:
                geocodes = json_obj['geocodes'][0]
                lon = float(geocodes.get('location').split(',')[0])
                lat = float(geocodes.get('location').split(',')[1])
                return [lon, lat]
            else:
                return None
        else:
            return None


def location():
    cmdfile = "./click.scpt"
    r = applescript.run(cmdfile)
    if r.out == 'false':
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
              "xcode location failed")
        return False
    else:
        return True


if __name__ == '__main__':
    g = Geocoding('f8ca14edcad37856646fadd5d84bf512')  # 这里填写你的高德api的key
    info = json.load(open(cityjson))
    total_city = len(info["city"])

    times = 0
    count = 0

    if auto == 1:
        # Enable debug will see http Request and Response
        # wda.DEBUG = True
        # get env from $DEVICE_URL if no arguments pass to wda.Client
        # http://localhost:8100 is the default value if $DEVICE_URL is empty
        try:
            c = wda.Client('http://localhost:8100')
            s = c.session(bundle_id)
            os.system("say check login out!")
            amap_loginout(c, s, 0)
        except Exception as err:
            print(err)
            program_exit(err)

    while True:
        times += 1
        if times > freq:
            break
        for i in info["city"]:
            count += 1
            if count < start and times == 1:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                      count, "/", total_city, "skip")
                continue

            while True:
                try:
                    result = g.geocode(i)
                except Exception as err:
                    cmd = "say" + " update city fail"
                    os.system(cmd)
                    print(err)
                    continue
                if result is not None:
                    break
                # time.sleep(1)
                cmd = "say" + " update city fail"
                os.system(cmd)
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                      "Oh! Get Noting, Try again...")
            gpx = ET.Element("gpx", version="1.1", creator="Xcode")
            wpt = ET.SubElement(gpx, "wpt",
                                lat=str(result[1]), lon=str(result[0]))
            ET.SubElement(wpt, "name").text = i
            ET.ElementTree(gpx).write(citygpx, encoding='utf-8')
            if location() is False:
                program_exit(username + " " + i + " location failed")
            else:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                      count, "/", total_city,
                      "Updated", times, "times! ", i, result)
            time.sleep(3)
            if auto == 1 and times == 1 and count == start:
                errnum = 0
                while True:
                    try:
                        s = c.session(bundle_id)
                        os.system("say login")
                        amap_login(c, s)
                        print(time.strftime("%Y-%m-%d %H:%M:%S",
                                            time.localtime()),
                              username, "login success.")
                        break
                    except Exception as err:
                        errnum += 1
                        if errnum < 3:
                            print(time.strftime("%Y-%m-%d %H:%M:%S",
                                                time.localtime()),
                                  username, "login fail ", errnum, "times!")
                            continue
                        else:
                            program_exit(username + " login fail! " +
                                         errnum + " times!" + err)
            time.sleep(keeptime)
        os.system("say turn around")
        count = 0

    if auto == 1:
        try:
            os.system("say login out")
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                  username, "login out.")
            amap_loginout(c, s, 1)
            s.close()
        except Exception as err:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                  username, "login out failed!", err)


