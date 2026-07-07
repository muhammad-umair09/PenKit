import requests
import urllib3
import os
from core.colors import Colors

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_directories(url: str) -> dict:
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
        
    print(Colors.info(f"Scanning target application endpoint: {url}"))
    
    # User se list poochenge
    wordlist_path = input(f"{Colors.YELLOW}[?] Enter Wordlist Path (or press Enter for Built-in list): ").strip()
    
    directories = []
    
    # UPGRADE: Agar user Enter dabaye, to computer se file dhoondne ke bajaye ye list load hogi
    if not wordlist_path:
        print(Colors.info("No file provided. Activating PenKit Built-in Web Discovery Wordlist..."))
        directories = [
            "admin", "login", "images", "uploads", "robots.txt", 
            "assets", "css", "js", "api", "test", "dev", "backup", 
            "config", "secure", "db", "v1", "v2", "status"
        ]
    else:
        # Agar user ne path diya hai to file read karein
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
    print(Colors.info(f"Loaded {len(directories)} components. Starting rapid head checks...\n"))
    
    # Scan Engine Execution Loop
    for chunk in directories:
        test_url = url.rstrip("/") + "/" + chunk.lstrip("/")
        try:
            response = requests.head(test_url, timeout=3, verify=False)
            
            # Agar folder mila (Status 200, 301, 302, 403 Forbidden)
            if response.status_code in [200, 301, 302, 403]: 
                print(f"  {Colors.GREEN}[+] Found: {test_url} (Status: {response.status_code})")
                results["Found_Directories"].append({"url": test_url, "status": response.status_code})
        except requests.RequestException:
            pass
            
    if not results["Found_Directories"]:
        print(Colors.fail("\nNo common components isolated via rapid head checks."))
    else:
        print(Colors.success(f"\n[+] Brute-force finished. Identified {len(results['Found_Directories'])} targets!"))
        
    return results