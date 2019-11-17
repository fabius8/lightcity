#!/usr/bin/python3

import json
import re

input_text = "temp.txt"
output_json = "temp.json"


def process_text_to_json(input_text):
    city_data = []
    with open(input_text, "r", encoding='utf-8') as f:
        for line in f:
            line = re.split(',|\s+|;|\n', line)
            line.remove('')
            if line is None:
                continue
            for i in line:
                if i != "":
                    city_data.append(i)
    return city_data


if __name__ == '__main__':
    cities = process_text_to_json(input_text)
    with open(output_json, "w", encoding='utf-8') as f:
        json.dump({'city': cities}, f, indent=4, ensure_ascii=False)

