#!/usr/bin/env python
import sys
from lxml.html import fromstring
import requests


class ScannerProxies:
    def __init__(self, depth=0, timeout=3, verbose="off", filename="proxies",
                 proxy_source="https://free-proxy-list.net/"):
        self.proxies = []
        self.proxy_source = proxy_source
        self.depth = depth
        self.timeout = timeout
        self.verbose = verbose
        self.filename = filename
        self.proxy_to_serve = ""
        self.new_proxy_list = []
        self.used_proxy_list = []

    def get_proxies(self):
        response = requests.get(self.proxy_source)
        parser = fromstring(response.text)
        if self.depth == 0:
            for i in parser.xpath('//tbody/tr'):
                if i.xpath('.//td[7][contains(text(),"yes")]'):
                    proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                    self.proxies.append(proxy)
        else:
            try:
                for i in parser.xpath('//tbody/tr')[:self.depth]:
                    if i.xpath('.//td[7][contains(text(),"yes")]'):
                        proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                        self.proxies.append(proxy)
            except TypeError:
                print('\n[-] Depth argument must be an integer greater than 0, or not passed.')
                print("This is the number of tables rows searched for ip addresses at " + str(self.proxy_source) + "\n")
                sys.exit()
        self.print_proxies()

    def print_proxies(self):
        if self.proxies:
            proxy_count = len(self.proxies)
            print("\n[+] " + str(proxy_count) + " possible proxies discovered >> Testing ...\n")
        else:
            print("\n[-] Proxies empty. Using your local IP instead.\n")
        self.test_proxies_dropping_errors()

    def test_proxies_dropping_errors(self):
        max_test_time = self.timeout * len(self.proxies)
        print("[+] Maximum time for testing is >> " + str(max_test_time) + " seconds.\n")
        url = 'https://httpbin.org/ip'
        for proxy in self.proxies:
            try:
                response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=self.timeout)
                if self.verbose == "on":
                    print("[+] Request >> " + str(proxy) + " / Response >> " + str(response.json()))
            except requests.exceptions.ConnectTimeout:
                if self.verbose == "on":
                    print("[-] Request >> " + str(proxy) + " / Server took too long to respond.")
                self.proxies.remove(proxy)
            except requests.exceptions.SSLError:
                if self.verbose == "on":
                    print("[-] Request >> " + str(proxy) + " / SSL certificate error.")
                self.proxies.remove(proxy)
            except requests.exceptions.ProxyError:
                if self.verbose == "on":
                    print("[-] Request >> " + str(proxy) + " / Connection error.")
                self.proxies.remove(proxy)
        proxy_count = len(self.proxies)
        print("\n[+] Test complete >> " + str(proxy_count) + " working proxies in list.\n")
        for proxy in self.proxies:
            print("[+] Working proxy >> " + str(proxy))
        self.save_to_file()

    def save_to_file(self):
        try:
            file = open("proxies/" + self.filename + ".txt", "x")
        except FileExistsError:
            file = open("proxies/" + self.filename + ".txt", "a")
        for proxy in self.proxies:
            file.write(str(proxy) + "\n")
        file.close()
        print("\n[+] File written in location proxies/" + self.filename + ".txt")

    def serve_proxies(self):
        with open("proxies/proxies.txt", "r+") as proxy_file:
            for proxy in proxy_file.readlines():
                self.new_proxy_list.append(proxy)
        with open("proxies/proxy_bin.txt", "r+") as used_proxies:
            for old_proxy in used_proxies.readlines():
                self.used_proxy_list.append(old_proxy)
        proxy_file.close()
        used_proxies.close()
        self.pull_proxy_from_file()
        return self.proxy_to_serve

    def pull_proxy_from_file(self):
        new_proxy = self.new_proxy_list[1]
        if new_proxy not in self.used_proxy_list:
            self.used_proxy_list.append(new_proxy)
            self.new_proxy_list.remove(new_proxy)
            self.proxy_to_serve = new_proxy

    def rewrite_proxy_files(self):
        with open("proxies/proxies.txt", "w") as proxy_file:
            for proxy in self.new_proxy_list:
                proxy_file.write(str(proxy).strip() + "\n")
            proxy_file.close()
        with open("proxies/proxy_bin.txt", "w") as used_proxies:
            for used_proxy in self.used_proxy_list:
                used_proxies.write(str(used_proxy).strip() + "\n")
            used_proxies.close()


# proxy_servers = ScannerProxies(depth=40, verbose="on")
# proxy_servers.get_proxies()
