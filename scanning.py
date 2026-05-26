import requests
from bs4 import BeautifulSoup
import socket
import datetime
import ipapi

def tambah_skema(url):
    if not url.startswith('http'):
        url = 'https://' + url
    return url

def scan_web(url):
    try:
        url = tambah_skema(url)
        # Mengambil informasi URL
        print(f"URL: {url}")
        # Mengambil informasi IP
        domain = url.replace("http://", "").replace("https://", "")
        ip_address = socket.gethostbyname(domain)
        print(f"IP: {ip_address}")
        # Mengambil informasi ISP
        isp_info = ipapi.location(ip_address)
        print(f"ISP: {isp_info['org']}")
        # Mengambil informasi Status Website
        response = requests.get(url, verify=True)
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
            print("Cloudflare: Protected")
        else:
            print("Cloudflare: Unprotected")
        # Mengambil informasi CMS
        cms_list = ['wordpress', 'joomla', 'drupal', 'magento']
        cms_detected = False
        for cms in cms_list:
            if cms in str(response.text).lower():
                print(f"CMS: {cms.capitalize()}")
                cms_detected = True
                break
        if not cms_detected:
            print("CMS: Not detected")
        # Mengambil informasi Server
        server = headers.get('Server')
        print(f"Server: {server if server else 'Not detected'}")
        # Mengambil informasi Header
        print("\nHeader:")
        for key, value in headers.items():
            print(f"{key}: {value}")
        # Mengambil informasi HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        print("\nHTML:")
        print(soup.title.text if soup.title else "No header")
        # Mengambil informasi meta tag
        meta_tags = soup.find_all('meta')
        print("\nMeta Tag:")
        for tag in meta_tags:
            name = tag.get('name')
            content = tag.get('content')
            if name and content:
                print(f"{name}: {content}")
            elif name:
                print(f"{name}: No content")
            elif content:
                print(f"No name: {content}")
    except Exception as e:
        print(f"Error: {e}")

url = input("TARGET URL: ").encode('utf-8').decode('utf-8')
scan_web(url)
