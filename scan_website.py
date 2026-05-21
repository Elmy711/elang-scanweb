import requests
from bs4 import BeautifulSoup
import re
import sys
import socket

def scan_site(target_url):
    # Validasi: Pastikan input adalah string
    if not isinstance(target_url, str):
        print(f"Error: Input tidak valid. Diterima: {type(target_url)}, Diperlukan: str")
        return

    # Bersihkan input dari karakter aneh jika ada
    target_url = target_url.strip()

    # Menambahkan protokol jika tidak ada
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url

    # Ekstrak domain untuk resolusi IP
    domain = target_url.replace('http://', '').replace('https://', '').split('/')
    
    detected_cms = []
    is_cloudflare = False
    
    try:
        # 1. Resolusi IP
        ip_address = socket.gethostbyname(domain)
        
        # 2. Request HTTP
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(target_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # --- Deteksi Cloudflare ---
        server_header = response.headers.get('Server', '').lower()
        cf_ray = response.headers.get('CF-RAY')
        cf_cookie = response.cookies.get('cf_clearance')
        
        if 'cloudflare' in server_header or cf_ray or cf_cookie:
            is_cloudflare = True
        # --- Akhir Deteksi Cloudflare ---

        # Pola deteksi CMS
        cms_patterns = {
            'WordPress': [r'wp-content', r'wp-includes', r'wordpress', r'wp-json'],
            'Joomla': [r'joomla', r'com_content', r'joomla-session'],
            'Drupal': [r'drupal', r'Drupal\.settings', r'drupal-settings'],
            'Shopify': [r'shopify', r'cdn\.shopify\.com'],
            'Wix': [r'wix\.com', r'wix\.studio'],
            'Magento': [r'magento', r'magento2']
        }

        # Cek di Header, Body, dan Cookie
        html_content = str(soup) + str(response.headers) + str(response.cookies)
        
        for cms, patterns in cms_patterns.items():
            for pattern in patterns:
                if re.search(pattern, html_content, re.IGNORECASE):
                    if cms not in detected_cms:
                        detected_cms.append(cms)
                    break

        print(f"--- Hasil Scan: {target_url} ---")
        print(f"Status Code: {response.status_code}")
        
        print("\n[Informasi Jaringan]")
        print(f"Domain: {domain}")
        print(f"IP Address: {ip_address}")

        print("\n[Keamanan & CDN]")
        if is_cloudflare:
            print("• Cloudflare: Terdeteksi (Aktif)")
            if cf_ray:
                print(f"  - Ray ID: {cf_ray}")
        else:
            print("• Cloudflare: Tidak terdeteksi")

        print("\n[Web Server]")
        print(f"Server: {response.headers.get('Server', 'Tidak terdeteksi')}")
        print(f"X-Powered-By: {response.headers.get('X-Powered-By', 'Tidak terdeteksi')}")

        print("\n[Deteksi CMS]")
        if detected_cms:
            for cms in detected_cms:
                print(f"• {cms}")
        else:
            print("• Tidak ada CMS umum yang terdeteksi.")
            
        print("\n[Judul Halaman]")
        title = soup.title.string if soup.title else "Tidak ada judul"
        print(f"• {title}")

    except socket.gaierror:
        print(f"Error: Domain '{domain}' tidak dapat ditemukan.")
    except requests.exceptions.RequestException as e:
        print(f"Error koneksi: {e}")
    except Exception as e:
        print(f"Terjadi kesalahan tak terduga: {e}")

if __name__ == "__main__":
    # Cek jumlah argumen
    if len(sys.argv) < 2:
        print("Penggunaan: python3 scan_website.py <alamat_website>")
        print("Contoh: python3 scan_website.py lemaanyilmedo.org")
        sys.exit(1)
    
    # Ambil argumen pertama (index 1) dan pastikan itu string
    # sys.argv adalah list, jadi kita ambil elemen ke-1
    raw_target = sys.argv
    
    # Jika user tidak sengaja memasukkan list (misal lewat IDE lain), kita ambil elemen pertama jika perlu
    if isinstance(raw_target, list):
        raw_target = raw_target
    
    scan_site(raw_target)
