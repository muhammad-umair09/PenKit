import requests
import urllib3
import os
from core.colors import Colors

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_directories(url: str) -> dict:
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
        
    print(Colors.info(f"Scanning target application endpoint: {url}"))
    
    wordlist_path = input(f"{Colors.YELLOW}[?] Enter Wordlist Path (or press Enter for Built-in list): ").strip()
    directories = []
    
    if not wordlist_path:
        print(Colors.info("No file provided. Activating PenKit Built-in Web Discovery Wordlist..."))
        directories = [
            "admin", "login", "images", "uploads", "robots.txt", 
            "assets", "css", "js", "api", "test", "dev", "backup", 
            "config", "secure", "db", "status"
        ]
    else:
        if not os.path.exists(wordlist_path):
            print(Colors.fail(f"Error: Wordlist file not found at '{wordlist_path}'"))
            return {"Found_Directories": []}
        try:
            with open(wordlist_path, "r") as f:
                directories = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        except Exception as e:
            print(Colors.fail(f"Failed to read file: {e}"))
            return {"Found_Directories": []}

    results = {"Found_Directories": []}
    print(Colors.info(f"Loaded {len(directories)} components. Starting smart scanning...\n"))
    
    # Custom User-Agent taaki server request block na kare
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) PenKit/2.0'}
    
    for chunk in directories:
        test_url = url.rstrip("/") + "/" + chunk.lstrip("/")
        try:
            # Step 1: Pehle HEAD check try karo fast speed ke liye
            response = requests.head(test_url, timeout=4, headers=headers, verify=False, allow_redirects=False)
            status = response.status_code
            
            # Step 2: UPGRADE - Agar server HEAD ko support nahi karta (405/500/400), to GET chalao
            if status in [405, 500, 400, 404] and status != 404:
                response = requests.get(test_url, timeout=4, headers=headers, verify=False, allow_redirects=False)
                status = response.status_code
            
            # Agar valid directory mili
            if status in [200, 301, 302, 403]: 
                print(f"  {Colors.GREEN}[+] Found: {test_url} (Status: {status})")
                results["Found_Directories"].append({"url": test_url, "status": status})
                
        except requests.RequestException:
            pass
            
    if not results["Found_Directories"]:
        print(Colors.fail("\nNo common components isolated via smart checks."))
    else:
        print(Colors.success(f"\n[+] Brute-force finished. Identified {len(results['Found_Directories'])} targets!"))
        
    return results