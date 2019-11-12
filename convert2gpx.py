#!/usr/bin/env python3

import json
import time
from datetime import datetime
from urllib import request, parse
import argparse

parser = argparse.ArgumentParser("convert2gpx.py city.json")
parser.add_argument("cityjson", help="convert json to gpx.", type=str)
args = parser.parse_args()
cityjson = args.cityjson
citygpx = cityjson.replace(".json", ".gpx")
print("input:", cityjson, "output:", citygpx)


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


if __name__ == '__main__':
    head = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n"
    head += "<gpx\n  xmlns=\"http://www.topografix.com/GPX/1/1\"\n"
    head += "  xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n"
    head += "  xsi:schemaLocation=\"http://www.topografix.com/GPX/1/1\n"
    head += "  http://www.topografix.com/GPX/1/1/gpx.xsd\"\n"
    head += "  version=\"1.1\"\n"
    head += "  creator=\"fabius8@163.com\"\n>"
    g = Geocoding('f8ca14edcad37856646fadd5d84bf512')  # 这里填写你的高德api的key
    info = json.load(open(cityjson))

    with open(citygpx, 'w') as the_file:
        the_file.write(head)

    ts = 1573401600
    count = 0
    for i in info["city"]:
        count += 1
        result = g.geocode(i)
        print(i, result)
        with open(citygpx, 'a') as the_file:
            latlon = '\n  <wpt '
            latlon += 'lat="' + str(result[1]) + '" '
            latlon += 'lon="' + str(result[0]) + '">\n'
            latlon += '    <name>' + i + '</name>\n'
            ts += 1
            strts = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%SZ')
            latlon += '    <time>' + strts + '</time>\n'
            latlon += '  </wpt>\n'
            latlon += '  <wpt '
            latlon += 'lat="' + str(result[1] + 0.005) + '" '
            latlon += 'lon="' + str(result[0] + 0.005) + '">\n'
            latlon += '    <name>' + i + '</name>\n'
            ts += 2
            strts = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%SZ')
            latlon += '    <time>' + strts + '</time>\n'
            latlon += '  </wpt>\n'
            the_file.write(latlon)

    print("city:", count)
    with open(citygpx, 'a') as the_file:
        the_file.write('</gpx>')

