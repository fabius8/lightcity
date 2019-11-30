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

bundle_id = 'com.autonavi.amap'

parser = argparse.ArgumentParser("lightcity.py city.json")
parser.add_argument("cityjson", help="convert json to gpx.", type=str)
parser.add_argument("--start", default=0, help="City start number", type=int)
parser.add_argument("--auto", default=1, help="auto login", type=int)
args = parser.parse_args()
cityjson = args.cityjson
result = re.search('^(.*)_(.*).json', cityjson)
username = result.group(1)
passwd = result.group(2)
citygpx = "city.gpx"
start = args.start
auto = args.auto
print("Input:", cityjson, "Output:", citygpx, "Start:", start, "Auto:", auto)


def program_exit(err):
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
          err)
    sys.exit()


def amap_login(s):
    s(name=u'我的').tap()
    time.sleep(5)
    s(name=u'登录后开启足迹地图').tap()
    time.sleep(1)
    s(name=u'其他登录方式').tap()
    # time.sleep(1)
    s(name=u'密码登录').tap()
    # time.sleep(1)
    s(type='TextField').set_text(username+'\n')
    time.sleep(2)
    s(type='SecureTextField').set_text(passwd+'\n')
    # time.sleep(1)
    s(name=u'登录').tap()
    # time.sleep(2)
    s(name=u'返回').tap()
    # time.sleep(2)
    s(name=u'首页').tap()
    # time.sleep(1)
    s(name=u'我的位置').tap()


def amap_loginout(s):
    s(name=u'我的').tap()
    time.sleep(1)
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
    keeptime = 30

    if auto == 1:
        # Enable debug will see http Request and Response
        # wda.DEBUG = True
        c = wda.Client('http://localhost:8100')
        # get env from $DEVICE_URL if no arguments pass to wda.Client
        # http://localhost:8100 is the default value if $DEVICE_URL is empty
        s = c.session(bundle_id)
        try:
            os.system("say check login out!")
            amap_loginout(s)
        except Exception as err:
            print(err)

    while True:
        times += 1
        if times == 3:
            break
        for i in info["city"]:
            count += 1
            if count < start:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                      count, "/", total_city, "skip")
                continue
            else:
                start = 0
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
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                  count, "/", total_city,
                  "Updated", times, "times! ", i, result)
            gpx = ET.Element("gpx", version="1.1", creator="Xcode")
            wpt = ET.SubElement(gpx, "wpt",
                                lat=str(result[1]), lon=str(result[0]))
            ET.SubElement(wpt, "name").text = i
            ET.ElementTree(gpx).write(citygpx, encoding='utf-8')
            while True:
                if location() is False:
                    program_exit(username + " " + i + " location failed")
                else:
                    break
            time.sleep(3)
            if auto == 1 and times == 1 and count == 1:
                try:
                    s = c.session(bundle_id)
                    os.system("say login")
                    amap_login(s)
                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                          username, "login success.")
                except Exception as err:
                    program_exit(username + " login fail! " + err)
            time.sleep(63)
        os.system("say turn around")
        count = 0

    if auto == 1:
        try:
            os.system("say login out")
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                  username, "login out.")
            amap_loginout(s)
            s.close()
        except Exception as err:
            print(err)

