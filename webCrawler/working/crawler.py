#! usr/bin/env python
import requests


class Crawler:
    def __init__(self):
        self.subdomains_list = []
        self.output_list = []

    def request(self, url):
        try:
            return requests.get("http://" + url)
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.MissingSchema:
            pass
        except requests.exceptions.InvalidURL:
            pass

    def find_subdomains(self, url, subdomains):
        with open("dictionary/subdomain_long.txt", "r") as wordlist_file:
            for line in wordlist_file:
                word = line.strip()
                test_url = word + "." + url
                response = self.request(test_url)
                if response:
                    print("[+] Subdomain >>> " + test_url + " >>> " + str(response))
                    subdomains.append(test_url)
        return subdomains

    def find_directories(self, word, url):
        word = str(word).strip()
        test_url = url + "/" + word
        response = self.request(test_url)
        if response:
            directory = [test_url, response]
            return directory
