import requests
import urllib3
from core.colors import Colors

# SSL/TLS warnings ko disabled rakhne ke liye
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
        
        # Yahan hum actual cookies ka data nikal rahe hain
        cookies_dict = response.cookies.get_dict()
        if cookies_dict:
            # Agar cookies hain, to unhe string format mein save kar rahe hain
            results["Cookies-Found"] = ", ".join([f"{k}={v[:15]}..." for k, v in cookies_dict.items()])
        else:
            results["Cookies-Found"] = "None"
        
        # Terminal par clean formatting ke sath print karne ke liye
        for k, v in results.items():
            print(f"  {Colors.WHITE}{k}: {v}")
            
    except Exception as e:
        results["Error"] = str(e)
        print(Colors.fail(f"Server response extraction disrupted: {e}"))
    return results