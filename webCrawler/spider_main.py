#!/usr/bin/env python

import threading
from spider import Spider
from savedata import SaveData
from queue import Queue


class SpiderMain:
    def __init__(self):
        self.TARGET_URL = "https://www.skatewarehouse.co.uk"
        self.PROJECT_NAME = "skatewarehouse"
        self.WORKERS = 4
        self.Spider = Spider(self.TARGET_URL, self.PROJECT_NAME)  # crawling object
        self.Saver = SaveData()  # saving object
        self.QUEUE = Queue()  # queue object

    def init_files(self, name, url):  # using saver object to create dir and files
        self.Saver.create_dir(name)
        self.Saver.create_files(name, url)

    def spawn_spiders(self):  # creates workers using threading lib
        print("[+] Creating workforce of " + str(self.WORKERS) + " spiders >>")
        for _ in range(self.WORKERS):
            thread = threading.Thread(target=self.accept_job)
            thread.daemon = False
            thread.start()

    def accept_job(self):
        link = self.QUEUE.get()  # take a job from the queue
        self.Spider.search(link)  # crawl this link
        self.QUEUE.task_done()  # indicate job is complete

    def crawl(self):
        links_queue = self.Saver.file_to_set(self.Saver.queued_links_path)
        if len(links_queue) > 0:
            print("[+] " + str(len(links_queue)) + " queued links awaiting spiders >>")
        self.add_job()

    def add_job(self):
        for link in self.Saver.file_to_set(self.Saver.queued_links_path):
            self.QUEUE.put(link)
        self.QUEUE.join()
        self.crawl()

    def main(self):
        self.init_files(self.PROJECT_NAME, self.TARGET_URL)

        self.spawn_spiders()

        self.crawl()


if __name__ == "__main__":
    run = SpiderMain()
    run.main()
