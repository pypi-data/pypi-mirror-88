#!python
import sys
import argparse
import os
from validator_collection import checkers
import multiprocessing as mp
import requests
from tabulate import tabulate
import tldextract

"""
Prints the msr package version
"""
def version():
    import pkg_resources
    version = pkg_resources.get_distribution("msr-by-sooz").version
    print(version)

def is_valid_url(url: str) -> bool:
    return checkers.is_url(url)

"""
Returns the directory to store registered URLs based on XDG convention:
https://wiki.archlinux.org/index.php/XDG_Base_Directory
"""
def get_registry_dir() -> str:
    home_dir = os.path.expanduser("~")
    xdg_data_home = os.environ.get("XDG_DATA_HOME", os.path.join(home_dir, ".local", "share"))
    return os.path.join(xdg_data_home, "msr_data")

def get_url_registry_path() -> str:
    return os.path.join(get_registry_dir(), 'url_registry')

"""
- Validates the given URL
- Persists URL into registry if valid
"""
def register():
    url = args.url

    # Validate url
    if is_valid_url(url) == False:
        print("invalid url -_-")
        sys.exit(1)

    # Get registry dir
    registry_dir = get_registry_dir()
    if not os.path.exists(registry_dir):
        os.makedirs(registry_dir)
    registry = os.path.join(registry_dir, 'url_registry')

    with open(registry, "a+") as file:
        # TODO: handle duplicates
        file.write(url + "\n")


def get_registered_urls() -> [str]:
    registry_path = get_url_registry_path()
    if not os.path.exists(registry_path):
        return []
    with open(registry_path, "r+") as file:
        urls = file.read().splitlines()
    return [url.rstrip() for url in urls]

def get_body_size(url: str) -> int:
    # TODO: error handling
    response = requests.get(url, allow_redirects=True)
    return len(response.content)

def print_pretty(col_headers, col_1_data, col_2_data):
    table = tabulate([list(entry) for entry in zip(col_1_data,
                 col_2_data)], headers=col_headers, tablefmt='orgtbl')
    print(table)

"""
Prints a table mapping registered URLs to size (in bytes)
of the body received by making a GET request to that URL
"""
def measure():
    # TODO: error handling
    urls = get_registered_urls()
    pool = mp.Pool(mp.cpu_count())
    response_sizes = pool.map_async(get_body_size, urls)
    pool.close()
    pool.join()
    print_pretty(["URL", "Response Body Size"], urls, response_sizes.get())

def get_response_time_in_ms(url: str) -> float:
    # TODO: error handling
    r = requests.get(url)
    return r.elapsed.total_seconds() * 1000

"""
Prints a table mapping registered domains to average load time
(in MS) of the registered URLs of each domain
"""
def race():
    # TODO: error handling
    urls = get_registered_urls()
    pool = mp.Pool(mp.cpu_count())
    load_times = pool.map_async(get_response_time_in_ms, urls)
    pool.close()
    pool.join()

    loaded_times = load_times.get()
    domain_map = {}
    for url, time in zip(urls, loaded_times):
        extracted = tldextract.extract(url)
        domain = "{}.{}".format(extracted.domain, extracted.suffix)
        if domain in domain_map:
            domain_entry = domain_map.get(domain)
            num_domains = domain_entry[0] + 1
            new_total_time = domain_entry[1] + time
        else:
            domain_map[domain] = [1, time]
    
    avg_map = {}
    for domain, entry in domain_map.items():
        avg_map[domain] = entry[1] / entry[0]

    print_pretty(['URL', 'Response Time (MS)'], avg_map.keys(),
             avg_map.values())

commands_to_functions_to_args = {
    'version' : [version, []],
    'register' : [register, ['url']],
    'measure' : [measure, []],
    'race' : [race, []]
}

parser = argparse.ArgumentParser(description="party time")
subparsers = parser.add_subparsers(dest='option')
for arg, arg_data in commands_to_functions_to_args.items():
    arg_parser = subparsers.add_parser(arg)
    for arg_arg in arg_data[1]:
        arg_parser.add_argument(arg_arg)
args = parser.parse_args()

if len(sys.argv) <= 1:
    parser.print_help()
    sys.exit(1)

commands_to_functions_to_args[args.option][0]()
