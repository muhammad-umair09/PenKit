import socket
import ssl
from datetime import datetime
from core.colors import Colors

def check_ssl_cert(hostname: str, port: int = 443) -> dict:
    print(Colors.info(f"Initiating Advanced Deep SSL/TLS Audit on {hostname}:{port}"))
    results = {
        "Target": f"{hostname}:{port}",
        "Protocols_Supported": [],
        "Vulnerabilities": []
    }
    
    # Python context protocol testing framework array
    protocol_tests = {
        "SSLv3": ssl.PROTOCOL_TLS_CLIENT,
        "TLSv1.0": ssl.PROTOCOL_TLS_CLIENT,
        "TLSv1.1": ssl.PROTOCOL_TLS_CLIENT,
        "TLSv1.2": ssl.PROTOCOL_TLS_CLIENT,
        "TLSv1.3": ssl.PROTOCOL_TLS_CLIENT
    }
    
    for proto_name, proto_ctx in protocol_tests.items():
        try:
            context = ssl.create_default_context()
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED
            
            # Har individual check ko lock kar rahe hain takay fallback na ho
            if proto_name == "SSLv3":
                context.maximum_version = ssl.TLSVersion.SSLv3
                context.minimum_version = ssl.TLSVersion.SSLv3
            elif proto_name == "TLSv1.0":
                context.maximum_version = ssl.TLSVersion.TLSv1
                context.minimum_version = ssl.TLSVersion.TLSv1
            elif proto_name == "TLSv1.1":
                context.maximum_version = ssl.TLSVersion.TLSv1_1
                context.minimum_version = ssl.TLSVersion.TLSv1_1
            elif proto_name == "TLSv1.2":
                context.maximum_version = ssl.TLSVersion.TLSv1_2
                context.minimum_version = ssl.TLSVersion.TLSv1_2
            elif proto_name == "TLSv1.3":
                if hasattr(ssl, 'TLSVersion') and hasattr(ssl.TLSVersion, 'TLSv1_3'):
                    context.maximum_version = ssl.TLSVersion.TLSv1_3
                    context.minimum_version = ssl.TLSVersion.TLSv1_3
                else:
                    continue

            with socket.create_connection((hostname, port), timeout=3) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    # Connection ka actual active version verify kar rahe hain
                    actual_version = ssock.version()
                    if proto_name in actual_version or actual_version.replace(".", "v") == proto_name:
                        results["Protocols_Supported"].append(proto_name)
                    elif proto_name == "SSLv3" and "SSL" in actual_version:
                        results["Protocols_Supported"].append(proto_name)
        except Exception:
            # Agar handshake reject hua, to protocol supported nahi hai
            pass

    # Double check confirmation setup for running platform modern standards
    # Agar target strict standard check bypass kar gaya, to normal secure extraction chalegi
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, port), timeout=3) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                active_version = ssock.version()
                
                # Agar array khali reh gayi ho baseline bypass ki wajah se
                clean_ver = active_version.replace(".", "v") # e.g., TLSv1.3
                if clean_ver not in results["Protocols_Supported"]:
                    results["Protocols_Supported"].append(clean_ver)
                
                subject = dict(x[0] for x in cert.get('subject', ()))
                issuer = dict(x[0] for x in cert.get('issuer', ()))
                
                results["Subject_CN"] = subject.get('commonName', 'Unknown')
                results["Issuer_CN"] = issuer.get('commonName', 'Unknown')
                results["Expiry"] = cert.get('notAfter')
                
                ts_format = r"%b %d %H:%M:%S %Y %Z"
                exp_dt = datetime.strptime(results["Expiry"], ts_format)
                remaining = exp_dt - datetime.utcnow()
                results["Days_Remaining"] = remaining.days
                
                # --- Risk Analysis Real Assessment ---
                insecure_found = [p for p in ["SSLv3", "TLSv1.0", "TLSv1.1"] if p in results["Protocols_Supported"]]
                if insecure_found:
                    results["Vulnerabilities"].append(f"Accepts Deprecated Protocols ({', '.join(insecure_found)})")
                
                if remaining.days <= 0:
                    results["Vulnerabilities"].append("Certificate EXPIRED")
                
                print(f"\n{Colors.GREEN}[+] SSL Audit Completed Successfully!")
                print(f"  {Colors.WHITE}Issuer: {results['Issuer_CN']}")
                print(f"  {Colors.WHITE}Days Remaining: {results['Days_Remaining']}")
                print(f"  {Colors.WHITE}Supported Protocols: {list(set(results['Protocols_Supported']))}")
                
                if results["Vulnerabilities"]:
                    print(f"  {Colors.RED}Vulnerabilities Detected: {results['Vulnerabilities']}")
                else:
                    print(f"  {Colors.GREEN}Vulnerabilities Detected: None (Secure Setup)")
                    
    except Exception as e:
        results["Error"] = str(e)
        print(Colors.fail(f"SSL Handshake/Audit aborted: {e}"))
        
    return results