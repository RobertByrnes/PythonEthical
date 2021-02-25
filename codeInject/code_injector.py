#! usr/bin/env python
import netfilterqueue
import scapy.all as scapy
import os
import re
os.system("iptables -I INPUT -j NFQUEUE --queue-num 0")
os.system("iptables -I OUTPUT -j NFQUEUE --queue-num 0")


def set_load(packet, load):
    packet[scapy.Raw].load = load
    if packet[scapy.IP].len:
        del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    if packet[scapy.IP].len:
        del packet[scapy.TCP].len
    del packet[scapy.TCP].len
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 10000:
            print("[+] Request")
            # modified_load = re.sub("Accept-Encoding:.*?\\r\\n", "", scapy_packet[scapy.Raw].load)
            # new_packet = set_load(scapy_packet, modified_load)
            # packet.set_payload(str(new_packet))
            print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 10000:
            print("[+] Response")
            print(scapy_packet.show())

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
