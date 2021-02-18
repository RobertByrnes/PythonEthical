# ARP SPOOFER
# Spoof the Router
Send ARP response to router that Hacker Machine (HM) is the Victims Machine (VM)
The router updates ARP table associating Victim IP with HM MAC address.

# Spoof the Target
Send ARP response to 'VM' that 'HM' is the router. VM will update ARP table
associating HM MAC address as router MAC address.

# Result
Therefore, all traffic (requests and responses) flow through the 'HM'. See Requirements,
port forwarding must be enabled on HM to allow traffic through.  If not, VM will be blocked
from the router.

# Why?
ARP is exploited this way because all clients accept responses even where
no request has been sent.  Clients accept response without verification.

# Requirements
echo 1 > /proc/sys/net//ipv4/ip_forward : enable port forwarding - this must be
enabled for victim internet access to flow through HM.

# Keystrokes
CTRL + C to end while-loop and quit.

# Notes
dst = destination ip
hwdst = destination MAC
pscr = router - for ARP table of target machine
Add the following code lines to arp_spoof/restore functions to view packet data:
    print(packet.show())
    print(packet.summary())