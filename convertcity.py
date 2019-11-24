#!/usr/bin/env python3

import json
import re
from urllib import request, parse


input_text = "temp.txt"
output_json = "temp.json"


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
            line = re.split('\.|，|,|\s+|;|\n|、|。', line)
            line.remove('')
            if line is None:
                continue
            for i in line:
                if i != "":
                    print(i)
                    count +=1
                    city_data.append(i)

        print("city number:", count)
        print(city_data)
        city_data_v2 = sorted(set(city_data), key=city_data.index)
        city_data = city_data_v2
        print(city_data)
        print("city number:", (len(city_data)), "after remove same city")
    return city_data


if __name__ == '__main__':
    g = Geocoding('f8ca14edcad37856646fadd5d84bf512')
    print("process start...")
    cities = process_text_to_json(input_text)
    check_cities = cities
    for i in cities:
        if test_city(g, i) is None:
            print("x", i)
            check_cities.remove(i)
    cities = check_cities
    print("End city number:", len(cities))
    with open(output_json, "w", encoding='utf-8') as f:
        json.dump({'city': cities}, f, indent=4, ensure_ascii=False)
    print("process end!")


