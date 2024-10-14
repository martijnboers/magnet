import os

import time
import socket
import requests
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
import btdht
import binascii
from time import sleep


def fetch_btih(url):
    """Fetch magnet links from the given URL by reading and splitting based on newlines."""
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return []

    # Simply split the plain text response content by newline
    magnet_links = response.json
    return [link.btih for link in magnet_links]


def get_seeders_ips(magnet_link):
    while True:
        print(dht.get_peers(binascii.a2b_hex(info_hash)))
        sleep(1)


def reverse_dns_lookup(ip):
    """Perform reverse DNS lookup on an IP address."""
    try:
        domain = socket.gethostbyaddr(ip)
        return domain[0]
    except socket.herror:
        return None


def process_magnet_link(magnet_link):
    """Process a single magnet link: Get seeders and perform reverse DNS lookup."""
    seeders_ips = get_seeders_ips(magnet_link)

    if not seeders_ips:
        print(f"No seeders found or failed to get metadata for {magnet_link}")
        return magnet_link, []

    domain_results = []
    for ip in ips:
        domain = reverse_dns_lookup(ip)
        domain_results.append((ip, domain))

    return magnet_link, domain_results

def main():
    dht = btdht.DHT()
    dht.start()
    sleep(15)  # wait for the DHT to build

    while True:
        print(dht.get_peers(binascii.a2b_hex("b08e88e85c571996755365e038b2c1d7f3fe5c24")))
        sleep(1)


# def main():
#     """Main function to be called when running the script."""
#     url = os.getenv("URL")
#     all_domain_results = []
#
#     # Step 1: Fetch magnet links
#     magnet_links = fetch_btih(url)
#     if not magnet_links:
#         print("No magnet links found.")
#         return
#
#     # Step 2: Process each magnet link concurrently using ThreadPoolExecutor
#     with ThreadPoolExecutor(max_workers=3) as executor:
#         future_to_magnet = {executor.submit(process_magnet_link, magnet): magnet for magnet in magnet_links}
#
#         # As each future completes, print the results
#         for future in as_completed(future_to_magnet):
#             magnet_link, domain_results = future.result()
#             if domain_results:
#                 print(f"Results for {magnet_link}:")
#                 for ip, domain in domain_results:
#                     if domain:
#                         print(f"{ip} -> {domain}")
#                         all_domain_results.append(domain_results)
#                     else:
#                         print(f"{ip} -> No domain found")
#
#     print("<---------- all results ------------->")
#     for domain in domain_results:
#         print(f"{ip} -> {domain}")
