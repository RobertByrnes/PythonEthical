#!/usr/bin/env python

import threading
from spider import Spider
from savedata import SaveData
import time
target_url = "https://www.skatewarehouse.co.uk"
project_name = "skatewarehouse"
workers = 1
save = SaveData()
spider = Spider(target_url)
visited = []
queued = []


new_links = []


def on_boot(name, url):
    save.create_dir(name)
    save.create_files(name, url)


def producer():
    page_links = spider.search()
    for link in page_links:
        save.append_to_file(save.queued_links_path, link)
        save.append_to_file(save.links_path, link)
    print("[+] links transferred to queue by " + threading.current_thread().name + " >>\n")
    return True


def make_queues():
    with open(save.queued_links_path, "r") as links:
        for link in links:
            queued.append(link)
    links.close()
    print("[+] Queue length >> " + str(len(queued)))
    time.sleep(.5)
    save.delete_file_contents(save.queued_links_path)
    with open(save.links_path, "r") as test_links:
        for test_link in test_links:
            visited.append(test_link)
    test_links.close()
    print("[+] Visited links count >> " + str(len(visited)))
    time.sleep(.5)
    save.delete_file_contents(save.queued_links_path)
    return True


def spiders():
    try:
        page_links = spider.search(queued.pop())  # remove and use search link from the end of the queue
        for link in page_links:
            if visited.count(link) == 0:  # check if any new link already in links.txt
                print(link + " found by " + threading.current_thread().name)
                save.append_to_file(save.links_path, link)  # if it is not already in links.txt put it there
        if make_queues():
            spiders()
    except:
        pass



def main():
    on_boot(project_name, target_url)
    if producer():
        if make_queues():
            print("[+] Creating workforce of " + str(workers) + " threads >>\n")
            for _ in range(workers):
                t = threading.Thread(target=spiders)
                t.start()


if __name__ == "__main__":
    main()
