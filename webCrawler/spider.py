#! usr/bin/env python
import requests
import re
import urllib.parse as urlparse
from savedata import SaveData


class Spider:
    def __init__(self, url, name):
        self.TARGET_URL = url
        self.PROJECT_NAME = name
        self.queued_links_file = self.PROJECT_NAME + "/queued_links.txt"
        self.links_visited_file = self.PROJECT_NAME + "/visited_links.txt"
        self.queue = set()
        self.crawled = set()
        self.search()
        self.Saver = SaveData()

    def search(self, url=None):
        if url is None:
            url = self.TARGET_URL
        href_links = self.extract_links(url)
        for link in href_links:
            link = urlparse.urljoin(url, link)
            if "#" in link:
                link = link.split("#")[0]
            self.sort_to_queue(link)
            self.add_to_crawled_set(link)

    def extract_links(self, url):
        try:
            response = requests.get(url)
            return re.findall('(?:href=")(.*?)"', response.content.decode(errors="ignore"))
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.MissingSchema:
            pass

    def sort_to_queue(self, link):
        if (link not in self.crawled) or (link not in self.queue):
            self.queue.add(link)

    def add_to_crawled_set(self, link):
        if link not in self.crawled:
            self.crawled.add(link)

    def update(self):
        self.Saver.set_to_file(self.queue, self.queued_links_file)
        self.Saver.set_to_file(self.crawled, self.links_visited_file)




