import os


class SaveData:
    def __init__(self):
        self.crawled_dirs_path = ""
        self.links_path = ""
        self.queued_links_path = ""

    def create_dir(self, directory):
        if not os.path.exists(directory):
            print("[+] Creating directory " + directory + " >>\n")
            os.makedirs(directory)

    def create_files(self, project_name, base_url):
        self.crawled_dirs_path = os.path.join(project_name, 'crawled_dirs.txt')
        self.links_path = os.path.join(project_name, "visited_links.txt")
        self.queued_links_path = os.path.join(project_name, "queued_links.txt")
        if not os.path.isfile(self.crawled_dirs_path):
            self.write_file(self.crawled_dirs_path, base_url)
        if not os.path.isfile(self.links_path):
            self.write_file(self.links_path, '')
        if not os.path.isfile(self.queued_links_path):
            self.write_file(self.queued_links_path, '')

    def write_file(self, path, data):
        with open(path, 'w') as f:
            f.write(data + '\n')

    def append_to_file(self, path, data):
        with open(path, 'a') as file:
            file.write(data + '\n')

    def delete_file_contents(self, path):
        open(path, 'w').close()

    # Read a file and convert each line to set items
    def file_to_set(self, file_name):
        results = set()
        with open(file_name, 'rt') as f:
            for line in f:
                results.add(line.replace('\n', ''))
        return results

    def set_to_file(self, links, file_name):
        with open(file_name, "w") as f:
            for link in sorted(links):
                f.write(link + "\n")
