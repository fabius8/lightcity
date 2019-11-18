#!/usr/bin/env python3

import json
import os
from urllib import request, parse
import argparse
import xml.etree.cElementTree as ET
import time

parser = argparse.ArgumentParser("createcity.py city.json")
parser.add_argument("cityjson", help="output city to json.", type=str)
args = parser.parse_args()
cityjson = args.cityjson


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
        if i["name"].find("新疆") != -1 or i["name"].find("西藏") != -1 or \
           i["name"].find("海南") != -1 or i["name"].find("云南") != -1 or \
           i["name"].find("山东") != -1 or i["name"].find("浙江") != -1 or \
           i["name"].find("江苏") != -1 or i["name"].find("广州") != -1 or \
           i["name"].find("广西") != -1 or i["name"].find("湖北") != -1 or \
           i["name"].find("河南") != -1 or i["name"].find("河北") != -1 or \
           i["name"].find("江西") != -1 or i["name"].find("四川") != -1 or \
           i["name"].find("贵州") != -1 or i["name"].find("陕西") != -1 or \
           i["name"].find("福建") != -1 or i["name"].find("安徽") != -1:
            for j in i["districts"]:
                count += 1
                cities.append(j["name"])
                print(j["name"])
    with open(cityjson, "w", encoding='utf-8') as f:
        json.dump({'city': cities}, f, indent=4, ensure_ascii=False)
    print("city number:", count)
