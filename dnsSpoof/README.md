# Setup / Close
create an accessible que usinf iptables:
iptables -I FORWARD -j NFQUEUE --queue-num 0
restore iptables after use:
iptables --Flush

# DNS
service apache2 start - to start apache in kali
Domain Name Server - browser sends request to dns server to resolve
domain names into ip addresses, e.g. A record. DNS server sends 
response with ip to user computer so user computer may access the ip address.

# DNS Spoof
This is achieved by sending on request from the target to dns server awaiting
the response and then modifying the packet response to change the ip address
to one of choice made by the hacker machine.

# Check
DNSQR - dns question record - qname contains domain name
DNSRR - dns resource record - A record - rdata field - contains IP

