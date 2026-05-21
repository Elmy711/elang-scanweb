import requests
from bs4 import BeautifulSoup
import socket
import datetime

def scan_web(url):
    try:
        # Mengambil informasi IP
        domain = url.replace("http://", "").replace("https://", "")
        ip_address = socket.gethostbyname(domain)
        print(f"Informasi IP: {ip_address}")

        # Mengambil informasi header
        response = requests.get(url)
        headers = response.headers
        print("\nInformasi Header:")
        for key, value in headers.items():
            print(f"{key}: {value}")

        # Mengambil informasi DNS
        print(f"\nInformasi DNS: {domain} -> {ip_address}")

        # Mengambil informasi Cloudflare
        if 'cloudflare' in str(headers).lower():
            print("\nInformasi Cloudflare: Terproteksi")
        else:
            print("\nInformasi Cloudflare: Tidak terproteksi")

        # Mengambil informasi CMS
        cms_list = ['wordpress', 'joomla', 'drupal', 'magento']
        cms_detected = False
        for cms in cms_list:
            if cms in str(response.text).lower():
                print(f"\nInformasi CMS: {cms.capitalize()}")
                cms_detected = True
                break
        if not cms_detected:
            print("\nInformasi CMS: Tidak terdeteksi")

        # Mengambil informasi Status Website
        if response.status_code == 200:
            print(f"\nInformasi Status Website: Online ({response.status_code})")
        elif response.status_code == 404:
            print(f"\nInformasi Status Website: Not Found ({response.status_code})")
        elif response.status_code == 500:
            print(f"\nInformasi Status Website: Internal Server Error ({response.status_code})")
        else:
            print(f"\nInformasi Status Website: {response.status_code}")

        # Mengambil informasi HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        print("\nInformasi HTML:")
        print(soup.title.text)

        # Mengambil informasi meta tag
        meta_tags = soup.find_all('meta')
        print("\nInformasi Meta Tag:")
        for tag in meta_tags:
            print(f"{tag.get('name')}: {tag.get('content')}")

    except Exception as e:
        print(f"Error: {e}")

url = input("Masukkan URL: ")
scan_web(url)
