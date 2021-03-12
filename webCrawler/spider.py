#! usr/bin/env python
import requests
import re
import urllib.parse as urlparse
from save_data import SaveData
import time


class Spider:
    def __init__(self, url, name):
        self.TARGET_URL = url
        self.domain = self.get_domain_name(url)
        self.PROJECT_NAME = name
        self.queued_links_file = "results/" + name + "/queued_links.txt"
        self.links_visited_file = "results/" + name + "/visited_links.txt"
        self.Saver = SaveData()
        self.queue = set()
        self.crawled = set()
        self.setup()
        self.search(spider_name="Charlotte the Spider", url=url)

    def setup(self):
        print("\n[+] Using domain name >> " + self.domain + "\n")
        time.sleep(1)
        self.Saver.create_dir(self.PROJECT_NAME)
        self.Saver.create_files(self.PROJECT_NAME, self.TARGET_URL)
        self.queue = self.Saver.file_to_set(self.queued_links_file)
        self.crawled = self.Saver.file_to_set(self.links_visited_file)

    def search(self, spider_name, url):
        try:
            print(1)
            self.sort_to_queue(Spider.extract_links(url))
            print(2)
            print("[+] now crawling >> " + url + " with " + spider_name)
            print("[+] Queued " + str(len(self.queue)) + " >> Crawled " + str(len(self.crawled)))
            if url in self.queue:
                self.queue.remove(url)
            if url not in self.crawled:
                self.crawled.add(url)
            self.update()
        except Exception as e:
            print("[-] Exception occured in " + url + " >> Exception: " + str(e))
        print(4)
        return True

    @staticmethod
    def extract_links(url):
        try:
            response = requests.get(url)
            return re.findall('(?:href=")(.*?)"', response.content.decode(errors="ignore"))
        except Exception as e:
            print("[-] Exception occured in " + url + " >> Exception: " + str(e))

    def sort_to_queue(self, links):
        for link in links:
            if (link in self.crawled) or (link in self.queue):
                continue
            if self.domain != Spider.get_domain_name(link):
                continue
            link = urlparse.urljoin(self.TARGET_URL, link)
            if link not in self.queue:
                self.queue.add(link)

    def update(self):
        try:
            self.Saver.set_to_file(self.queue, self.queued_links_file)
            self.Saver.set_to_file(self.crawled, self.links_visited_file)
            print(3)
            return True
        except Exception as e:
            print("[-] Exception: Saving >> " + str(e))

    @staticmethod
    def get_domain_name(url):
        try:
            results = str(urlparse.urlparse(url).netloc)
            return results
        except Exception as e:
            return str(e)
