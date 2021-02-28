#! usr/bin python
# ARP Address Resolution Protocol

import scapy.all as scapy
import argparse


def capture_arguments():
    # create an instance of option parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="IP to scan or range of IP addresses e.g. 192.168.0.1/24")
    # options = variables, arguments = --i or --m
    args = parser.parse_args()
    if not args.target:
        parser.error("[-] Please specify an IP address or range of IP addresses, use --help for info")
    return args


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast_mac = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast_mac/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    client_list = []
    for element in answered_list:
        client_dict = {"IP": element[1].psrc, "MAC": element[1].hwsrc}
        client_list.append(client_dict)
    return client_list


def print_result(results_list):
    print("IP\t\t\tMAC Address\n--------------------------------------------")
    for client in results_list:
        print(client["IP"] + "\t\t" + client["MAC"])


options = capture_arguments()
scan_result = scan(str(options.target))
print_result(scan_result)
