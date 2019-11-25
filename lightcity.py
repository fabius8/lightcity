#!/usr/bin/env python3

import json
import os
from urllib import request, parse
import argparse
import xml.etree.cElementTree as ET
import time

parser = argparse.ArgumentParser("convert2gpx.py city.json")
parser.add_argument("cityjson", help="convert json to gpx.", type=str)
parser.add_argument("--start", default=0, help="City start number", type=int)
args = parser.parse_args()
cityjson = args.cityjson
citygpx = "city.gpx"
start = args.start
print("Input:", cityjson, "Output:", citygpx, "Start:", start)
print("")

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


ecmd = "osascript ./click.scpt 1>/dev/null"


if __name__ == '__main__':
    g = Geocoding('f8ca14edcad37856646fadd5d84bf512')  # 这里填写你的高德api的key
    info = json.load(open(cityjson))
    total_city = len(info["city"])

    times = 0
    count = 0
    keeptime = 30
    while True:
        times += 1
        for i in info["city"]:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            count += 1
            if count < start:
                print(count, "/", total_city, "skip")
                continue
            else:
                start = 0
            while True:
                try:
                    result = g.geocode(i)
                except Exception as result:
                    cmd = "say" + " update city fail"
                    os.system(cmd)
                    print(result)
                    continue
                if result is not None:
                    break
                time.sleep(3)
                cmd = "say" + " update city fail"
                os.system(cmd)
                print("Oh! Get Noting, Try again...")
            print(count, "/", total_city,
                  "Updated", times, "times! ", i, result)
            gpx = ET.Element("gpx", version="1.1", creator="Xcode")
            wpt = ET.SubElement(gpx, "wpt",
                                lat=str(result[1]), lon=str(result[0]))
            ET.SubElement(wpt, "name").text = i
            ET.ElementTree(gpx).write(citygpx, encoding='utf-8')
            os.system(ecmd)
            time.sleep(63)
        os.system("say turn around")
        count = 0

