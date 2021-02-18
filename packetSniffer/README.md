# Packet Sniffer
Following on from MITM read packets received by this machine,
using the scapy module from Python.

# Layer Filtering
Set the filter argument of scapy.sniff function using Berkeley packet filtering
syntax e.g. UDP/port 3/arp/tcp - scapy.sniff filter param does not support http.
Use another scapy function - .hasLayer(http.HTTPRequest) on packet object for this.
https://biot.com/capstats/bpf.html for Berkeley Packet Reference
https://github.com/invernizzi/scapy-http
Set port to 21 for ftp packets
[scapy.PACKET_NAME e.g. raw].field_name e.g.load

# Usage Notes
MITM has a habit of dropping the connection after so many packets so keep an eye on this although
it does work. 
- to set port forwarding: echo 1 > /proc/sys/net/ipv4/ip_forward
- To enable Network Manager use: sudo systemctl start NetworkManager

# Future Development
1. Create input handling to set different layers to sniff
ar maybe to sniff multiple layers.
2. Add logging to .txt

