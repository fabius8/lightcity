#!/usr/bin/env python3

import json
from urllib import request, parse

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
    head += "  creator=\"fabius8@163.com\"\n>\n"
    g = Geocoding('f8ca14edcad37856646fadd5d84bf512')  # 这里填写你的高德api的key
    info = json.load(open("city.json"))

    with open('output.gpx', 'w') as the_file:
        the_file.write(head)

    count = 0
    for i in info["city"]:
        count += 1
        result = g.geocode(i)
        with open('output.gpx', 'a') as the_file:
            latlon = '  <wpt '
            latlon += 'lat="' + str(result[1]) + '" '
            latlon += 'lon="' + str(result[0]) + '">\n'
            latlon += '    <name>' + i + '</name>\n'
            latlon += '    <time>' + "2019-01-01T00:" + str(count).zfill(2) + ":00Z</time>\n"
            latlon += '  </wpt>\n'
            latlon += '  <wpt '
            latlon += 'lat="' + str(result[1] + 0.001) + '" '
            latlon += 'lon="' + str(result[0] + 0.001) + '">\n'
            latlon += '    <name>' + i + '</name>\n'
            latlon += '    <time>' + "2019-01-01T00:" + str(count).zfill(2) + ":59Z</time>\n"
            latlon += '  </wpt>\n\n'
            the_file.write(latlon)

