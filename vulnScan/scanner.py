#!/usr/bin/env python

import requests
import re
import urllib.parse as urlparse
from bs4 import BeautifulSoup


class Scanner:
    def __init__(self, url):
        self.session = requests.Session()
        self.target_url = url
        self.target_links = []
        self.subdomains_list = []
        self.directories_list = []
        self.output_list = []

    def find_subdomains(self, proxy=None):
        print("\n[+] Scanning for subdomains >> \n")
        with open("dictionary/subdomain.txt", "r") as wordlist_file:
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
                if proxy is None:
                    response = self.request(test_url)
                else:
                    response = self.request(test_url, proxy)
                if response:
                    print("[+] Subdomain >> " + test_url + " >> " + str(response))
                    self.subdomains_list.append(test_url)
        wordlist_file.close()
        print("\n[+] Subdomain scan complete. >> \n")

    def find_directories(self, input_url=None, proxy=None):
        print("[+] Scanning for directories >>> \n")
        if input_url is not None:
            self.subdomains_list.append(input_url)
        else:
            self.subdomains_list.append(self.target_url)
        with open("dictionary/5line_testfile.txt", "r") as wordlist_file:
            for url in self.subdomains_list:
                for line in wordlist_file:
                    word = line.strip()
                    test_url = url + "/" + word
                    if proxy is None:
                        response = self.request(test_url)
                    else:
                        response = self.request(test_url, proxy)
                    if response:
                        print("[+] Directory >> " + test_url + " >> " + str(response))
                        self.directories_list.append(test_url)
            wordlist_file.close()
            print("\n[+] Scanning for subdirectories >> \n")
        with open("dictionary/common.txt", "r") as wordlist_file:
            for url in self.directories_list:
                for line in wordlist_file:
                    word = line.strip()
                    test_url = url + "/" + word
                    response = self.request(test_url)
                    if response:
                        print("[+] Sub-Directory or file >> " + test_url + " >> " + str(response))
                        self.output_list.append(test_url)
        wordlist_file.close()
        print("\n[+] Directories scan complete >> \n")

    def crawl(self, url=None, proxy=None):
        if url is None:
            url = self.target_url
        if proxy is None:
            href_links = self.extract_links()
        else:
            href_links = self.extract_links(proxy)
        for link in href_links:
            link = urlparse.urljoin(url, link)

            if "#" in link:
                link = link.split("#")[0]
            if self.target_url in link and link not in self.target_links:
                self.target_links.append(link)
                print("[+] Link >> " + link)
                self.crawl(link)

    def extract_links(self, proxy=None):
        if proxy is None:
            response = requests.get(self.target_url)
        else:
            response = requests.get(self.target_url, proxies={"http": proxy, "https": proxy})
        return re.findall('(?:href=")(.*?)"', response.content.decode(errors="ignore"))

    def extract_forms(self, proxy=None):
        print("[+] Extracting html forms from web pages >> \n")
        if proxy is None:
            response = self.session.get(self.target_url)
        else:
            response = self.session.get(self.target_url, proxies={"http": proxy, "https": proxy})
        parsed_html = BeautifulSoup(response.content, features="html.parser")  # "lxml" for execution on linux OS
        return parsed_html.findAll("form")

    def request(self, url, proxy=None):
        try:
            if proxy is None:
                return requests.get(url)
            else:
                return requests.get(url, proxies={"http": proxy, "https": proxy})
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.MissingSchema:
            pass
        except requests.exceptions.InvalidURL:
            pass
