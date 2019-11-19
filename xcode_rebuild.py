#!/usr/bin/env python3
import os
import time

ecmd = "osascript ./xcode_rebuild.scpt 1>/dev/null"

time.sleep(1)
os.system(ecmd)
