#!/usr/bin/env python3

import json
import os
from urllib import request, parse
import argparse
import xml.etree.cElementTree as ET
import time
import datetime


class Getcity:
    def __init__(self, api_key):
        self.api_key = api_key

    def geocode(self, address):
        """
        """
        geocoding = {'s': 'rsv3',
                     'key': self.api_key,
                     'keywords': address,
                     'subdistrict': 2}
        geocoding = parse.urlencode(geocoding)
        req = request.Request("%s?%s" % ("http://restapi.amap.com/v3/config/district", geocoding))
        ret = request.urlopen(req)

        if ret.getcode() == 200:
            res = ret.read()
            json_obj = json.loads(res)
            if json_obj['status'] == '1' and int(json_obj['count']) >= 1:
                geocodes = json_obj["districts"][0]["districts"]
                return geocodes
            else:
                return None
        else:
            return None


if __name__ == '__main__':
    g = Getcity('f8ca14edcad37856646fadd5d84bf512')  # 这里填写你的高德api的key
    count = 0
    cities = []
    for i in g.geocode("中国"):
        if i["name"].find("北京") != -1 or i["name"].find("重庆") != -1 or \
           i["name"].find("香港") != -1 or i["name"].find("澳门") != -1 or \
           i["name"].find("天津") != -1 or i["name"].find("台湾") != -1 or \
           i["name"].find("上海") != -1:
            count += 1
            cities.append(i["name"])
            #print(i["name"])
            continue
        for j in i["districts"]:
            count += 1
            cities.append(j["name"])
            #print(j["name"])
    cityjson = input("Please input city file name: ")
    if cityjson == "":
        cityjson = "allcity_unname.json"
    with open(cityjson, "w", encoding='utf-8') as f:
        json.dump({'date': str(datetime.datetime.now()),
                   'city': cities},
                  f, indent=4, ensure_ascii=False)
    print("city number:", count)
