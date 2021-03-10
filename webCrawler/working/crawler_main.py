#!/usr/bin/env python

import threading
from working import crawler
from save_data import SaveData

target_url = "www.skatewarehouse.co.uk"
project_name = "skatewarehouse"
workers = 8
queued_words = []
queued_words2 = []
queued_directories = []
save = SaveData()


def on_boot(name, url):
    save.create_dir(name)
    save.create_files(name, url)


def producer():
    with open("../dictionaries/common.txt", "r+") as wordlist:
        for line in wordlist:
            line = line.strip()
            queued_words.append(line)
            queued_words2.append(line)
    wordlist.close()
    print("[+] Wordlist transferred to queues by " + threading.current_thread().name + " >>\n")


def get_dirs(url):
    if not len(queued_words) == 0:
        word = queued_words.pop(0)
        directory = crawler.Crawler().find_directories(word, url)
        if directory:
            print("[+] Dir >> " + directory[0] + " >> by " + threading.current_thread().name)
            queued_directories.append(directory[0])
            save.append_to_file(save.crawled_dirs_path, directory[0])
    if not len(queued_words) == 0:
        get_dirs(target_url)
    else:
        print("[+] Dir scan completed by " + threading.current_thread().name + ", moving on.")
        get_subs()


def get_subs():
    if not len(queued_directories) == 0 or not len(queued_words2) == 0:
        url = queued_directories.pop(0)
        word = queued_words2.pop(0)
        directory = crawler.Crawler().find_directories(word, url)
        if directory:
            print("[+] SubDir >> " + directory[0] + " >> by " + threading.current_thread().name)
            save.append_to_file(save.crawled_dirs_path, directory[0])
    if not len(queued_directories) == 0 or not len(queued_words2) == 0:
        get_subs()
    else:
        print("\n[+] SubDir scan completed by " + threading.current_thread().name)


def main():
    on_boot(project_name, target_url)
    producer()
    print("[+] Creating workforce of " + str(workers) + " threads >>\n")
    for _ in range(workers):
        t = threading.Thread(target=get_dirs, args=[target_url],)
        t.start()


if __name__ == "__main__":
    main()
