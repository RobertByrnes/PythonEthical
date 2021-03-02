#!/usr/bin/env python

from lxml.html import fromstring
import requests


class ScannerProxies:
    def __init__(self):
        self.proxies = []
        self.proxy_source = "https://free-proxy-list.net/"

    def get_proxies(self):
        response = requests.get(self.proxy_source)
        parser = fromstring(response.text)
        for i in parser.xpath('//tbody/tr'):  # [:10] from before colon - sets number of proxies returned
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                self.proxies.append(proxy)
        return self.proxies

    def print_proxies(self):
        if self.proxies:
            proxy_count = len(self.proxies)
            print("\n[+] " + str(proxy_count) + " possible proxies discovered >> Testing ...\n")
        else:
            print("\n[-] Proxies empty. Using your local IP instead.\n")

    def test_proxies_dropping_errors(self):
        url = 'https://httpbin.org/ip'
        for proxy in self.proxies:
            try:
                response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=3)
                print("[+] Request >> " + str(proxy) + " / Response >> " + str(response.json()))
            except requests.exceptions.ConnectTimeout:
                print("[-] Request >> " + str(proxy) + " / Server took too long to respond.")
                self.proxies.remove(proxy)
            except requests.exceptions.SSLError:
                print("[-] Request >> " + str(proxy) + " / SSL certificate error.")
                self.proxies.remove(proxy)
            except requests.exceptions.ProxyError:
                print("[-] Request >> " + str(proxy) + " / Connection error.")
                self.proxies.remove(proxy)
        proxy_count = len(self.proxies)
        print("\n[+] Test complete >> " + str(proxy_count) + " working proxies in list.\n")
        for proxy in self.proxies:
            print("[+] Working proxy >> " + str(proxy))


proxy_servers = ScannerProxies()
proxy_servers.get_proxies()
proxy_servers.print_proxies()
proxy_servers.test_proxies_dropping_errors()

# add max time for testing
# add verbose to constructor for printing the proxies or not
