#!/usr/bin/env python

import requests
import re
import urllib.parse as urlparse
from bs4 import BeautifulSoup
import ip_rotate


class Scanner:
    def __init__(self, url):
        self.session = requests.Session()
        self.target_url = url
        self.target_links = []
        self.subdomains_list = []
        self.directories_list = []
        self.output_list = []
        self.proxies = ip_rotate.ScannerProxies()

    def find_subdomains(self):
        with open("dictionary/subdomain_long.txt", "r") as wordlist_file:
            for line in wordlist_file:
                word = line.strip()
                if "http://www." in self.target_url:
                    test_url = "http://" + word + "." + self.target_url.replace("http://www.", "")
                elif "https://www." in self.target_url:
                    test_url = "https://" + word + "." + self.target_url.replace("https://www.", "")
                elif "www." in self.target_url:
                    test_url = word + "." + self.target_url.replace("www.", "")
                else:
                    test_url = word + "." + self.target_url
                response = self.request(test_url)
                if response:
                    print("[+] Subdomain >>> " + test_url + " >>> " + str(response))
                    self.subdomains_list.append(test_url)

    def find_directories(self, input_url=None):
        if input_url is not None:
            self.subdomains_list = input_url
        with open("dictionary/subdomain_long.txt", "r") as wordlist_file:
            for url in self.subdomains_list:
                for line in wordlist_file:
                    word = line.strip()
                    test_url = url + "/" + word
                    response = self.request(test_url)
                    if response:
                        print("[+] Directory >>> " + test_url + " >>> " + str(response))
                        self.directories_list.append(test_url)
            for url in self.subdomains_list:
                for line in wordlist_file:
                    word = line.strip()
                    test_url = url + "/" + word
                    response = self.request(test_url)
                    if response:
                        print("[+] Sub-Directory or file >>> " + test_url + " >>> " + str(response))
                        self.output_list.append(test_url)

    def crawl(self, url=None):
        if url is None:
            url = self.target_url
        href_links = self.extract_links(url)
        for link in href_links:
            link = urlparse.urljoin(url, link)

            if "#" in link:
                link = link.split("#")[0]
            if self.target_url in link and link not in self.target_links:
                self.target_links.append(link)
                print("[+] Link > " + link)
                self.crawl(link)

    def extract_links(self):
        response = requests.get(self.target_url)
        return re.findall('(?:href=")(.*?)"', response.content.decode(errors="ignore"))

    def extract_forms(self, url):
        response = self.session.get(url)
        parsed_html = BeautifulSoup(response.content, features="html.parser")  # "lxml" for execution on linux OS
        return parsed_html.findAll("form")

    def request(self, url):
        try:
            return requests.get(url)
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.MissingSchema:
            pass
        except requests.exceptions.InvalidURL:
            pass
