#!/usr/bin/env python

import threading
from spider import Spider
from save_data import *
from queue import Queue


class SpiderMain:
    def __init__(self):
        self.TARGET_URL = "https://www.skatewarehouse.co.uk"
        self.PROJECT_NAME = "skatewarehouse"
        self.queue_path = "results/" + self.PROJECT_NAME + "/queued_links.txt"
        self.WORKERS = 4
        self.Spider = Spider(self.TARGET_URL, self.PROJECT_NAME)  # crawling object
        self.QUEUE = Queue()  # queue object

    def spawn_spiders(self):  # creates workers using threading lib
        print("[+] Creating workforce of " + str(self.WORKERS) + " more spiders >>")
        for _ in range(self.WORKERS):
            thread = threading.Thread(target=self.accept_job)
            thread.daemon = True
            thread.start()

    def accept_job(self):
        while True:
            link = self.QUEUE.get()  # take a job from the queue
            self.Spider.search(threading.current_thread().name, link)  # crawl this link
            self.QUEUE.task_done()  # indicate job is complete

    def crawl(self):
        links_queue = SaveData.file_to_set(self.queue_path)
        for link in links_queue:
            if len(links_queue) > 0:
                if str(self.TARGET_URL) in str(link):
                    print("[+] " + str(len(links_queue)) + " queued links awaiting spiders >>")
                    self.add_job()

    def add_job(self):
        for link in SaveData.file_to_set(self.queue_path):
            self.QUEUE.put(link)
        self.QUEUE.join()
        self.crawl()

    def main(self):
        self.spawn_spiders()

        self.crawl()


if __name__ == "__main__":
    run = SpiderMain()
    run.main()
