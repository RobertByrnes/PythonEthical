# Getting Past HTTPS
# HTTP
Sent as plain text therefore very easy to manipulate.

# HTTPS
Encrypted using TLS(Transport Layer Security) or SSL(Secure Sockets Layer)
Initial request usual sent over HTTP - server responds with 'lets use HTTPS'

# Moxie
This guy came up with a way to downgrade HTTPS to HTTP - exploiting
users not typing 'https' at the beginning of their requests.
This is done in Python using SSLstrip lib.  Works on port 10000
For a MITM attack with this, hacker machine will fool victim machine
into using HTTP and forward/collect requests/responses to website/server in
HTTPS.  We can read the responses   from the web server because the HTTPS request
are initiated by the hacker machine.

# Beware HSTS
Hard coded list of websites a browser will only in HTTPS! THere was a loophole
that got fixed.

# Beware will appear in targets browser as not secure

# Beware will not work with netfilter FORWARD chain
use "iptables -I OUTPUT -j NFQUEUE --queue-num 0"
and "iptables -I INPUT -j NFQUEUE --queue-num 0"
This is because all packets will be redirected to sslstrip and therefore
FORWARD chain will be empty.

Also, dport/sport in file_interceptor.py will need to because of rule created in
"iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000" in
strip_ssl.py

# sslstrip args
sslstrip 0.9 by Moxie Marlinspike                                               
Usage: sslstrip <options>                                                       
                                                                                
Options:                                                                        
-w <filename>, --write=<filename> Specify file to log to (optional).            
-p , --post                       Log only SSL POSTs. (default)                 
-s , --ssl                        Log all SSL traffic to and from server.       
-a , --all                        Log all SSL and HTTP traffic to and from server.
-l <port>, --listen=<port>        Port to listen on (default 10000).            
-f , --favicon                    Substitute a lock favicon on secure requests. 
-k , --killsessions               Kill sessions in progress.                                                                                                          
-h                                Print this help message.

