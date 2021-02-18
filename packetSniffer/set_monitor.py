#! usr/bin/env python

import os


def kill_network_manager():
    os.system('sudo airmon-ng check')
    os.system('sudo airmon-ng check kill')


def set_monitor_mode():
    os.system('ip link set wlan0 down')
    os.system('iw wlan0 set monitor control')
    os.system('ip link set wlan0 up')
    os.system('iw dev')


kill_network_manager()
set_monitor_mode()
