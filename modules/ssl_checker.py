import socket
import ssl
from datetime import datetime
from core.colors import Colors

def check_ssl_cert(hostname: str, port: int = 443) -> dict:
    print(Colors.info(f"Initiating Advanced Deep SSL/TLS Audit on {hostname}:{port}"))
    results = {
        "Target": f"{hostname}:{port}",
        "Protocols_Supported": [],
        "Protocols_Rejected": [],
        "Vulnerabilities": []
    }
    
    # --- UPGRADE 1: SSL/TLS Protocol Version Audit ---
    # Hum alag-alag versions se handshake try karenge dekhne ke liye ki kaun sa allowed hai
    protocol_tests = {
        "SSLv3": ssl.PROTOCOL_TLS, # Deprecated & Insecure
        "TLSv1.0": ssl.PROTOCOL_TLS,
        "TLSv1.1": ssl.PROTOCOL_TLS,
        "TLSv1.2": ssl.PROTOCOL_TLS,
        "TLSv1.3": ssl.PROTOCOL_TLS if hasattr(ssl, 'HAS_TLSv1_3') else None
    }
    
    for proto_name, proto_ctx in protocol_tests.items():
        if proto_ctx is None:
            continue
        try:
            context = ssl.create_default_context()
            # Puraane protocols ko force karne ke liye context settings adjust kar rahe hain
            if proto_name == "TLSv1.0":
                context.minimum_version = ssl.TLSVersion.TLSv1
                context.maximum_version = ssl.TLSVersion.TLSv1
            elif proto_name == "TLSv1.1":
                context.minimum_version = ssl.TLSVersion.TLSv1_1
                context.maximum_version = ssl.TLSVersion.TLSv1_1
            elif proto_name == "TLSv1.2":
                context.minimum_version = ssl.TLSVersion.TLSv1_2
                context.maximum_version = ssl.TLSVersion.TLSv1_2
            elif proto_name == "TLSv1.3":
                context.minimum_version = ssl.TLSVersion.TLSv1_3
                context.maximum_version = ssl.TLSVersion.TLSv1_3
                
            with socket.create_connection((hostname, port), timeout=3) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    results["Protocols_Supported"].append(proto_name)
        except Exception:
            results["Protocols_Rejected"].append(proto_name)

    # --- UPGRADE 2: Basic Certificate Data Extraction ---
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, port), timeout=3) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                subject = dict(x[0] for x in cert.get('subject', ()))
                issuer = dict(x[0] for x in cert.get('issuer', ()))
                
                results["Subject_CN"] = subject.get('commonName', 'Unknown')
                results["Issuer_CN"] = issuer.get('commonName', 'Unknown')
                results["Expiry"] = cert.get('notAfter')
                
                # Expiry Calculation
                ts_format = r"%b %d %H:%M:%S %Y %Z"
                exp_dt = datetime.strptime(results["Expiry"], ts_format)
                remaining = exp_dt - datetime.utcnow()
                results["Days_Remaining"] = remaining.days
                
                # --- UPGRADE 3: Security & Misconfiguration Analysis ---
                # Check 1: Insecure Protocols allowed?
                insecure_found = [p for p in ["SSLv3", "TLSv1.0", "TLSv1.1"] if p in results["Protocols_Supported"]]
                if insecure_found:
                    results["Vulnerabilities"].append(f"Accepts Deprecated Protocols ({', '.join(insecure_found)})")
                    print(Colors.fail(f"Risk Found: Server accepts weak protocols: {insecure_found}"))
                
                # Check 2: Certificate Expired or close to expiry?
                if remaining.days <= 0:
                    results["Vulnerabilities"].append("Certificate EXPIRED")
                    print(Colors.fail("Risk Found: Certificate has expired!"))
                elif remaining.days < 15:
                    results["Vulnerabilities"].append("Certificate expiring soon (less than 15 days)")
                    print(Colors.warn("Warning: Certificate is close to expiration."))
                
                # Final Output Presentation
                print(f"\n{Colors.GREEN}[+] SSL Audit Completed Successfully!")
                print(f"  {Colors.WHITE}Issuer: {results['Issuer_CN']}")
                print(f"  {Colors.WHITE}Days Remaining: {results['Days_Remaining']}")
                print(f"  {Colors.WHITE}Supported Protocols: {results['Protocols_Supported']}")
                if results["Vulnerabilities"]:
                    print(f"  {Colors.RED}Vulnerabilities Detected: {results['Vulnerabilities']}")
                else:
                    print(f"  {Colors.GREEN}Vulnerabilities Detected: None (Secure Setup)")
                    
    except Exception as e:
        results["Error"] = str(e)
        print(Colors.fail(f"SSL Handshake/Audit aborted: {e}"))
        
    return results