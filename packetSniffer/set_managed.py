#! usr/bin/env python

import os
os.system('systemctl start NetworkManager')
os.system('ip link set wlan0mon down')
os.system('iwconfig wlan0mon mode managed channel auto')
os.system('ip link set wlan0mon up')
os.system('iw dev')
