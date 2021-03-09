#! usr/bin/env python
import requests
import re
import urllib.parse as urlparse


class Spider:
    def __init__(self, url):
        self.target_links = []
        self.target_url = url

    def extract_links(self, url):
        try:
            response = requests.get(url)
            return re.findall('(?:href=")(.*?)"', response.content.decode(errors="ignore"))
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.MissingSchema:
            pass

    def search(self, url=None):
        if url is None:
            url = self.target_url
        href_links = self.extract_links(url)
        for link in href_links:
            link = urlparse.urljoin(url, link)
            if "#" in link:
                link = link.split("#")[0]
            if self.target_url in link and link not in self.target_links:
                self.target_links.append(link)
        return self.target_links
