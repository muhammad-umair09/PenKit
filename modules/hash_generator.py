import hashlib
from core.colors import Colors

def generate_hashes(text: str) -> dict:
    # Agar user ne input khali choda ho
    if not text:
        text = input("Enter payload data string to convert: ").strip()
        if not text:
            print(Colors.fail("Error: No data string provided for processing."))
            return {}

    print(Colors.info("Computing cryptographic digests across multi-algorithm arrays..."))
    
    results = {}
    try:
        # Standard cryptographic algorithms computation
        results["MD5"] = hashlib.md5(text.encode()).hexdigest()
        results["SHA-1"] = hashlib.sha1(text.encode()).hexdigest()
        results["SHA-256"] = hashlib.sha256(text.encode()).hexdigest()
        results["SHA-512"] = hashlib.sha512(text.encode()).hexdigest()
        
        # Output printing loop - 'Colors.white' ki jagah standard interpolation use ki hai
        print(f"\n{Colors.GREEN}[+] Cryptographic Generation Matrix Finished:")
        print(f"  [-] MD5    : {results['MD5']}")
        print(f"  [-] SHA-1  : {results['SHA-1']}")
        print(f"  [-] SHA-256: {results['SHA-256']}")
        print(f"  [-] SHA-512: {results['SHA-512']}\n")
        
    except Exception as e:
        print(Colors.fail(f"Execution handling failure: {e}"))
        
    return results