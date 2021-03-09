#!/usr/bin/env python

import requests
import re
import os
import urllib.parse as urlparse
from bs4 import BeautifulSoup


class Scanner:
    def __init__(self, url, scan_name, thread_name):
        self.session = requests.Session()
        self.target_url = url
        self.target_links = []
        self.subdomains_list = []
        self.directories_list = []
        self.subdirectory_list = []
        self.target_name = scan_name
        self.init_logs()
        self.create_data_files()
        self.crawl_single_url(thread_name)

    def init_logs(self):
        make_dir = self.target_name
        make_files = (self.target_name, self.target_url)
        if not os.path.exists(make_dir):
            print("\n[+] Creating directory >> " + make_dir + "\n")
            os.makedirs(make_dir)

    def create_data_files(self):
        subdomains = os.path.join(self.target_name, "subdomains.txt")
        directories = os.path.join(self.target_name, "directories.txt")
        subdirectories = os.path.join(self.target_name, "subdirectories.txt")
        links = os.path.join(self.target_name, "links.txt")
        if not os.path.isfile(subdomains):
            self.write_file(subdomains, "")
        if not os.path.isfile(directories):
            self.write_file(directories, "")
        if not os.path.isfile(subdirectories):
            self.write_file(subdirectories, "")
        if not os.path.isfile(links):
            self.write_file(links, "")

    def write_file(self, path, data):
        with open(path, 'w') as f:
            f.write(data)

    def append_to_file(self, path, data):
        with open(path, 'a') as file:
            file.write(data + '\n')

    def find_subdomains(self, thread_names, proxy=None):
        print("\n[+] Scanning for subdomains >> ")
        print("\n[+] " + thread_names + " Scanning for subdomains >>\n")
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
                    print("[+] Subdomain > " + test_url + " >> " + str(response))
                    self.subdomains_list.append(test_url)
        wordlist_file.close()
        for subdomain in self.subdomains_list:
            self.append_to_file(os.path.join(self.target_name, "subdomains.txt"), subdomain)
        print("\n[+] Subdomain scan complete >> \n")

    def find_directories(self, input_url=None, proxy=None):
        print("[+] Scanning for directories >> \n")
        if input_url is not None:
            self.subdomains_list.append(input_url)
        else:
            self.subdomains_list.append(self.target_url)
        with open("dictionary/common.txt", "r") as wordlist_file:
            for url in self.subdomains_list:
                for line in wordlist_file:
                    print(line)
                    word = line.strip()
                    test_url = url + "/" + word
                    if proxy is None:
                        response = self.request(test_url)
                    else:
                        response = self.request(test_url, proxy)
                    if response:
                        print("[+] Directory > " + test_url + " >> " + str(response))
                        self.directories_list.append(test_url)
        wordlist_file.close()
        for directory in self.directories_list:
            self.append_to_file(os.path.join(self.target_name, "directories.txt"), directory)
        print("\n[+] Scanning for subdirectories >> \n")
        with open("dictionary/common.txt", "r") as wordlist_file:
            for url in self.directories_list:
                for line in wordlist_file:
                    word = line.strip()
                    test_url = url + "/" + word
                    response = self.request(test_url)
                    if response:
                        print("[+] Sub-Directory or file > " + test_url + " >> " + str(response))
                        self.subdirectory_list.append(test_url)
        wordlist_file.close()
        for subdirectory in self.subdirectory_list:
            self.append_to_file(os.path.join(self.target_name, "subdirectories.txt"), subdirectory)
        print("\n[+] Directories scan complete >> \n")

    def crawl_single_url(self, thread_name, url=None):
        if url is None:
            url = self.target_url
        print("[+] Crawling " + url + " for links >> \n")
        href_links = self.extract_links(url)
        for link in href_links:
            link = urlparse.urljoin(url, link)
            if "#" in link:
                link = link.split("#")[0]
            if url in link and link not in self.target_links:
                self.target_links.append(link)
                print("[+] Link > " + link + " found by " + thread_name)
                self.crawl_single_url(link)
        for links in self.target_links:
            self.append_to_file(os.path.join(self.target_name, "links.txt"), links)
        # print("\n[+] Crawling complete >>\n")

    def extract_links(self, proxy=None, url=None):
        if url is None and proxy is None:
            response = requests.get(self.target_url)
        elif url is None and proxy:
            response = requests.get(self.target_url, proxies={"http": proxy, "https": proxy})
        elif url and proxy is None:
            response = requests.get(url)
        elif url and proxy:
            response = requests.get(url, proxies={"http": proxy, "https": proxy})
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
