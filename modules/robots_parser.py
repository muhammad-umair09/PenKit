import requests
import urllib3
from core.colors import Colors

# SSL warnings ko disable rakhne ke liye
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def parse_robots_txt(url: str) -> dict:
    # URL formatting check
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    
    # Root domain par robots.txt ka path set karna
    if not url.endswith("/robots.txt"):
        url = url.rstrip("/") + "/robots.txt"
        
    print(Colors.info(f"Targeting infrastructure discovery component: {url}"))
    results = {
        "Disallowed_Paths": [],
        "Sitemaps": []
    }
    
    try:
        response = requests.get(url, timeout=5, verify=False)
        
        if response.status_code == 200:
            lines = response.text.split("\n")
            
            # Line by line parse karna
            for line in lines:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                
                # Disallow paths nikalna
                if line.lower().startswith("disallow:"):
                    path = line.split(":", 1)[1].strip()
                    if path:
                        results["Disallowed_Paths"].append(path)
                
                # Sitemap links nikalna
                elif line.lower().startswith("sitemap:"):
                    sitemap = line.split(":", 1)[1].strip()
                    if sitemap:
                        results["Sitemaps"].append(sitemap)
            
            print(Colors.success(f"robots.txt found. Isolated paths identified: {len(results['Disallowed_Paths'])}"))
            
            # --- UPGRADE: Live Paths Printing on Screen ---
            if results["Disallowed_Paths"]:
                print(f"\n{Colors.YELLOW}[*] Listing All Disallowed Paths Live on Screen:")
                for path in results["Disallowed_Paths"]:
                    print(f"  {Colors.WHITE}[-] Disallowed: {path}")
            
            if results["Sitemaps"]:
                print(f"\n{Colors.GREEN}[+] Sitemap Links Identified:")
                for sitemap in results["Sitemaps"]:
                    print(f"  {Colors.WHITE}[=>] Sitemap: {sitemap}")
                    
        else:
            print(Colors.fail(f"robots.txt not found on this server (Status Code: {response.status_code})"))
            
    except Exception as e:
        results["Error"] = str(e)
        print(Colors.fail(f"Robots.txt parsing aborted: {e}"))
        
    return results