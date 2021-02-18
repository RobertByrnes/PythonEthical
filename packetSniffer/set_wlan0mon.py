#! usr/bin/env python

import os

os.system('ifconfig wlan0')
os.system('airmon-ng check kill')
os.system('ifconfig wlan0 up')
os.system('airmon-ng start wlan0')
# os.system('airodump-ng wlan0mon')
os.system('ifconfig wlan0mon')
