#!/usr/bin/env python3

import json
import re
from collections import Counter
from urllib import request, parse
import datetime


input_text = "temp.txt"
output_json = "temp.json"


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


def test_city(g, city):
    try:
        result = g.geocode(city)
    except Exception as result:
        print(result)
        return None
    return result


def process_text_to_json(input_text):
    city_data = []
    count = 0
    with open(input_text, "r", encoding='utf-8') as f:
        for line in f:
            line = re.split('\"|\.|，|,|\s+|;|\n|、|。', line)
            try:
                line.remove('')
            except Exception as err:
                print(err)
            if line is None:
                continue
            for i in line:
                if i != "":
                    count += 1
                    city_data.append(i)

        print("city number:", count)

        print(city_data, len(city_data))
        print("\n>>>same>>>")
        b = dict(Counter(city_data))
        for k, v in b.items():
            if v > 1:
                print("!", k)
        print("<<<same<<<\n")
        city_data_v2 = sorted(set(city_data), key=city_data.index)
        city_data = city_data_v2
        print("city number:", (len(city_data)), "after remove same city")
        print(city_data, len(city_data))
    return city_data


if __name__ == '__main__':
    g = Geocoding('f8ca14edcad37856646fadd5d84bf512')
    gc = Getcity('f8ca14edcad37856646fadd5d84bf512')
    print("process start...")

    count = 0
    all_cities = []
    for i in gc.geocode("中国"):
        if i["name"].find("北京") != -1 or i["name"].find("重庆") != -1 or \
           i["name"].find("香港") != -1 or i["name"].find("澳门") != -1 or \
           i["name"].find("天津") != -1 or i["name"].find("台湾") != -1 or \
           i["name"].find("上海") != -1:
            count += 1
            all_cities.append(i["name"])
            continue
        for j in i["districts"]:
            count += 1
            all_cities.append(j["name"])

    if len(all_cities) != 370:
        print("get all city failed!")

    cities = process_text_to_json(input_text)
    check_cities = []
    unfind_cities = []
    find = 0
    for i in cities:
        find = 0
        for j in all_cities:
            if j.find(i) != -1:
                check_cities.append(j)
                find = 1
                #print(i, j)
                break
        if find == 0:
            unfind_cities.append(i)

    print("\n>>>unfind>>>")
    for i in unfind_cities:
        print("X", i)
    print("<<<unfind<<<\n")

    cities = check_cities
    for i in cities:
        if test_city(g, i) is None:
            print("X", i)
            check_cities.remove(i)
    cities = check_cities

    print(cities, len(cities))
    print("\n>>>same>>>")
    b = dict(Counter(cities))
    for k, v in b.items():
        if v > 1:
            print("!", k)
    print("<<<same<<<\n")
    cities = sorted(set(cities), key=cities.index)

    print("End city number:", len(cities))
    print(cities, len(cities))
    with open(output_json, "w", encoding='utf-8') as f:
        json.dump({'date': str(datetime.datetime.now()),
                   'city': cities},
                  f, indent=4, ensure_ascii=False)
    print("process end!")

