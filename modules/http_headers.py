import requests
import urllib3
from core.colors import Colors

# SSL/TLS warnings ko screen se gayab karne ke liye
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def analyze_http_headers(url: str) -> dict:
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
        
    print(Colors.info(f"Connecting to live API/Web server engine asset: {url}"))
    results = {}
    try:
        response = requests.get(url, timeout=5, verify=False)
        hdrs = response.headers
        results["Server"] = hdrs.get("Server", "Not Disclosed")
        results["Powered-By"] = hdrs.get("X-Powered-By", "Not Disclosed")
        results["Content-Type"] = hdrs.get("Content-Type", "Not Disclosed")
        results["Cache-Control"] = hdrs.get("Cache-Control", "Not Configured")
        results["Set-Cookie"] = "Present" if "Set-Cookie" in hdrs else "Absent"
        
        # Yahan fix kiya gaya hai: Colors.WHITE ko sahi tareeqe se format kiya hai
        for k, v in results.items():
            print(f"  {Colors.WHITE}{k}: {v}")
            
    except Exception as e:
        results["Error"] = str(e)
        print(Colors.fail(f"Server response extraction disrupted: {e}"))
    return results