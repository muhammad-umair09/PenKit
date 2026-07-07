import hashlib
import os
from core.colors import Colors

def identify_hash(hash_str: str) -> str:
    """Hash ki length ke mutabiq algorithm identify karne ke liye"""
    length = len(hash_str)
    if length == 32:
        return "MD5"
    elif length == 40:
        return "SHA-1"
    elif length == 64:
        return "SHA-256"
    elif length == 128:
        return "SHA-512"
    else:
        return "Unknown"

def crack_hash(target_hash: str, hash_type: str, wordlist_path: str) -> bool:
    """Wordlist ka use karke hash crack karne ke liye"""
    if not os.path.exists(wordlist_path):
        print(Colors.fail(f"Error: Wordlist file not found at '{wordlist_path}'"))
        return False
        
    print(Colors.info(f"Initiating Brute-Force/Dictionary attack against {hash_type}..."))
    
    try:
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                word = line.strip()
                if not word:
                    continue
                    
                # On-the-fly execution based on type
                if hash_type == "MD5":
                    guess = hashlib.md5(word.encode()).hexdigest()
                elif hash_type == "SHA-1":
                    guess = hashlib.sha1(word.encode()).hexdigest()
                elif hash_type == "SHA-256":
                    guess = hashlib.sha256(word.encode()).hexdigest()
                elif hash_type == "SHA-512":
                    guess = hashlib.sha512(word.encode()).hexdigest()
                else:
                    return False
                    
                # Check match
                if guess == target_hash:
                    print(f"\n{Colors.GREEN}[=== CRACKED SUCCESS ===]")
                    print(f"  [+] Target Hash: {target_hash}")
                    print(f"  [+] Plaintext  : {word}\n")
                    return True
                    
        print(Colors.fail("\n[-] Password hash exhaustion: String not found in wordlist."))
        return False
        
    except Exception as e:
        print(Colors.fail(f"Cracker interface anomaly: {e}"))
        return False

def generate_hashes(text: str) -> dict:
    """Main function covering Generator, Identifier, and Cracker sub-modes"""
    print(f"\n{Colors.YELLOW}[1] Generate Hashes from Text")
    print(f"[2] Identify & Crack an existing Hash")
    sub_choice = input(f"{Colors.YELLOW}[?] Select Sub-Mode: ").strip()
    
    # === SUB-MODE 1: GENERATOR ===
    if sub_choice == "1":
        if not text:
            text = input("Enter payload data string to convert: ").strip()
            if not text:
                print(Colors.fail("Error: No data string provided."))
                return {}
                
        print(Colors.info("Computing cryptographic digests across multi-algorithm arrays..."))
        results = {
            "MD5": hashlib.md5(text.encode()).hexdigest(),
            "SHA-1": hashlib.sha1(text.encode()).hexdigest(),
            "SHA-256": hashlib.sha256(text.encode()).hexdigest(),
            "SHA-512": hashlib.sha512(text.encode()).hexdigest()
        }
        
        print(f"\n{Colors.GREEN}[+] Cryptographic Generation Matrix Finished:")
        for alg, val in results.items():
            print(f"  [-] {alg.ljust(7)}: {val}")
        return results

    # === SUB-MODE 2: IDENTIFIER & CRACKER ===
    elif sub_choice == "2":
        target_hash = input("[?] Enter the target hash to analyze: ").strip().lower()
        if not target_hash:
            print(Colors.fail("Error: Hash string input empty."))
            return {}
            
        hash_type = identify_hash(target_hash)
        print(Colors.info(f"Analyzing structure... Signature Match Found: {Colors.GREEN}{hash_type}"))
        
        if hash_type == "Unknown":
            print(Colors.fail("Unsupported or invalid hash format length."))
            return {}
            
        crack_choice = input(f"{Colors.YELLOW}[?] Do you want to attempt cracking via wordlist? (y/n): ").strip().lower()
        if crack_choice == 'y':
            wordlist_path = input("[?] Enter Wordlist Path: ").strip()
            # Dynamic dictionary attack run
            crack_hash(target_hash, hash_type, wordlist_path)
            
        return {"Target_Hash": target_hash, "Type": hash_type}
        
    else:
        print(Colors.fail("Invalid selection inside pipeline execution wrapper."))
        return {}