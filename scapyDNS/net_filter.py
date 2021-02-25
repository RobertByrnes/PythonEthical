#! usr/bin/env
# Use: iptables -I FORWARD -j NFQUEUE --queue-num 0
import netfilterqueue


def process_packet(packet):
    print(packet)


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
