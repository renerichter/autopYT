import os


def get_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip() and not line.strip().startswith('#')]

def parse_urls_argument(urls):
    if len(urls) == 1 and os.path.isfile(urls[0]):
        return get_urls_from_file(urls[0])
    return urls