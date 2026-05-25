import requests
from bs4 import BeautifulSoup
import socket
import datetime

def scan_web(url):
    try:
        # Mengambil informasi URL
        print(f"URL: {url}")

        # Mengambil informasi IP
        domain = url.replace("http://", "").replace("https://", "")
        ip_address = socket.gethostbyname(domain)
        print(f"IP: {ip_address}")

        # Mengambil informasi Status Website
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Status: Online ({response.status_code})")
        elif response.status_code == 404:
            print(f"Status: Not Found ({response.status_code})")
        elif response.status_code == 500:
            print(f"Status: Internal Server Error ({response.status_code})")
        else:
            print(f"Status: {response.status_code}")

        # Mengambil informasi DNS
        print(f"DNS: {domain} -> {ip_address}")

        # Mengambil informasi Cloudflare
        headers = response.headers
        if 'cloudflare' in str(headers).lower():
            print("Cloudflare: Terproteksi")
        else:
            print("Cloudflare: Tidak terproteksi")

        # Mengambil informasi CMS
        cms_list = ['wordpress', 'joomla', 'drupal', 'magento']
        cms_detected = False
        for cms in cms_list:
            if cms in str(response.text).lower():
                print(f"CMS: {cms.capitalize()}")
                cms_detected = True
                break
        if not cms_detected:
            print("CMS: Tidak terdeteksi")

        # Mengambil informasi Header
        print("\nHeader:")
        for key, value in headers.items():
            print(f"{key}: {value}")

        # Mengambil informasi HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        print("\nHTML:")
        print(soup.title.text if soup.title else "Tidak ada judul")

        # Mengambil informasi meta tag
        meta_tags = soup.find_all('meta')
        print("\nMeta Tag:")
        for tag in meta_tags:
            name = tag.get('name')
            content = tag.get('content')
            if name and content:
                print(f"{name}: {content}")
            elif name:
                print(f"{name}: Tidak ada konten")
            elif content:
                print(f"Tidak ada nama: {content}")
    except Exception as e:
        print(f"Error: {e}")

url = input("TARGET URL: ")
scan_web(url)
