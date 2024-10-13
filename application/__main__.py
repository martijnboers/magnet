import os

import libtorrent as lt
import time
import socket
import requests
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed


def fetch_magnet_links(url):
    """Fetch magnet links from the given URL by reading and splitting based on newlines."""
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return []

    # Simply split the plain text response content by newline
    magnet_links = response.text.splitlines()
    return [link for link in magnet_links if link.startswith('magnet:')]


def get_seeders_ips(magnet_link, timeout=60):
    """Get seeders' IPs from the magnet link using libtorrent with a timeout."""

    # Create a temporary directory to store the torrent files
    with tempfile.TemporaryDirectory() as tempdir:
        ses = lt.session()
        ses.listen_on(6881, 6891)
        params = {
            'save_path': tempdir,  # Use temporary directory as save_path
            'storage_mode': lt.storage_mode_t(2),
        }

        handle = lt.add_magnet_uri(ses, magnet_link, params)
        ses.start_dht()

        start_time = time.time()
        while not handle.has_metadata():
            # Check if the timeout is exceeded
            if time.time() - start_time > timeout:
                return magnet_link, []  # Return an empty list of seeders if metadata could not be retrieved
            time.sleep(1)

        seeders_ips = []
        while not handle.is_seed():
            status = handle.status()
            peers = status.handle.get_peer_info()
            for peer in peers:
                ip = peer.ip[0]
                if ip not in seeders_ips:
                    seeders_ips.append(ip)
            time.sleep(1)
        return magnet_link, seeders_ips


def reverse_dns_lookup(ip):
    """Perform reverse DNS lookup on an IP address."""
    try:
        domain = socket.gethostbyaddr(ip)
        return domain[0]
    except socket.herror:
        return None


def process_magnet_link(magnet_link):
    """Process a single magnet link: Get seeders and perform reverse DNS lookup."""
    seeders_ips = get_seeders_ips(magnet_link, timeout=60)
    magnet_link, ips = seeders_ips

    if not ips:
        print(f"No seeders found or failed to get metadata for {magnet_link}")
        return magnet_link, []

    domain_results = []
    for ip in ips:
        domain = reverse_dns_lookup(ip)
        domain_results.append((ip, domain))

    return magnet_link, domain_results


def main():
    """Main function to be called when running the script."""
    url = os.getenv("URL")
    all_domain_results = []

    # Step 1: Fetch magnet links
    magnet_links = fetch_magnet_links(url)
    if not magnet_links:
        print("No magnet links found.")
        return

    # Step 2: Process each magnet link concurrently using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_magnet = {executor.submit(process_magnet_link, magnet): magnet for magnet in magnet_links}

        # As each future completes, print the results
        for future in as_completed(future_to_magnet):
            magnet_link, domain_results = future.result()
            if domain_results:
                print(f"Results for {magnet_link}:")
                for ip, domain in domain_results:
                    if domain:
                        print(f"{ip} -> {domain}")
                        all_domain_results.append(domain_results)
                    else:
                        print(f"{ip} -> No domain found")

    print("<---------- all results ------------->")
    for domain in domain_results:
        print(f"{ip} -> {domain}")


if __name__ == "__main__":
    main()
