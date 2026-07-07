import requests
import urllib3
import os
import time
from core.colors import Colors

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_directories(url: str) -> dict:
    # URL Standard Normalization
    if not url.startswith("http://") and not url.startswith("https://"):
        if "vulnweb" in url:
            url = "http://" + url
        else:
            url = "https://" + url
            
    print(Colors.info(f"Scanning target application endpoint: {url}"))
    
    wordlist_path = input(f"{Colors.YELLOW}[?] Enter Wordlist Path (or press Enter for Built-in list): ").strip()
    directories = []
    
    if not wordlist_path:
        print(Colors.info("No file provided. Activating PenKit Built-in Web Discovery Wordlist..."))
        # Targeted structured mapping parameters
        directories = [
            "admin", "login", "images", "secure", 
            "includes", "robots.txt", "categories"
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
    print(Colors.info(f"Loaded {len(directories)} components. Starting dynamic session verification...\n"))
    
    # Real Chrome Environment Signature Header Wrapper
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive'
    })
    
    # Target baseline ping before brute force initiation
    try:
        session.get(url, timeout=6, verify=False)
    except Exception as e:
        print(Colors.fail(f"Initial baseline target handshake dropped: {e}"))

    for chunk in directories:
        test_url = url.rstrip("/") + "/" + chunk.lstrip("/")
        try:
            # Dynamic GET processing sequence with clean verification controls
            response = session.get(test_url, timeout=6, verify=False, allow_redirects=True)
            status = response.status_code
            
            # Catch standard validation codes
            if status in [200, 403]: 
                print(f"  {Colors.GREEN}[+] Found: {test_url} (Status: {status})")
                results["Found_Directories"].append({"url": test_url, "status": status})
                
            # WAF prevention delay pattern iteration
            time.sleep(0.2)
                
        except requests.RequestException:
            pass
            
    if not results["Found_Directories"]:
        print(Colors.fail("\nNo common components isolated via dynamic baseline checks."))
    else:
        print(Colors.success(f"\n[+] Brute-force finished. Identified {len(results['Found_Directories'])} targets!"))
        
    return results