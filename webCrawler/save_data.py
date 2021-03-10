import os


class SaveData:
    crawled_dirs_path = ""
    links_path = ""
    queued_links_path = ""

    @staticmethod
    def create_dir(directory):
        if not os.path.exists(directory):
            print("[+] Creating directory " + directory + " >>\n")
            os.makedirs(directory)

    @staticmethod
    def create_files(project_name, base_url):
        SaveData.crawled_dirs_path = os.path.join(project_name, 'results/crawled_dirs.txt')
        SaveData.links_path = os.path.join(project_name, "results/visited_links.txt")
        SaveData.queued_links_path = os.path.join(project_name, "results/queued_links.txt")
        if not os.path.isfile(SaveData.crawled_dirs_path):
            SaveData.write_file(SaveData.crawled_dirs_path, "")
        if not os.path.isfile(SaveData.links_path):
            SaveData.write_file(SaveData.links_path, "")
        if not os.path.isfile(SaveData.queued_links_path):
            SaveData.write_file(SaveData.queued_links_path, "")

    @staticmethod
    def write_file(path, data):
        with open(path, 'w') as f:
            f.write(data + '\n')

    @staticmethod
    def append_to_file(path, data):
        with open(path, 'a') as file:
            file.write(data + '\n')

    @staticmethod
    def delete_file_contents(path):
        open(path, 'w').close()

    @staticmethod
    def file_to_set(file_name):
        results = set()
        with open(file_name, 'r') as f:
            for line in f:
                results.add(line.replace('\n', ''))
        return results

    @staticmethod
    def set_to_file(links, file_name):
        with open(file_name, "w") as f:
            for link in sorted(links):
                f.write(link + "\n")