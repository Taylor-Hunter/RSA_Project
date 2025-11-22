# rsa_comparison_demo.py
# CS532 Project - comparing different RSA key sizes
# Taylor Hunter & Kelly Powell

def demonstrate_key_size_security():
    """Shows why RSA key size matters so much"""
    
    print("="*60)
    print("RSA KEY SIZE COMPARISON")
    print("Why size matters in RSA - CS532 Project")
    print("Taylor Hunter & Kelly Powell")
    print("="*60)
    
    # Example weak vs strong moduli (for demonstration purposes)
    weak_examples = [
        ("8-bit", 143, "11 × 13", "Toy example"),
        ("16-bit", 15161, "119 × 127", "Instantly breakable"),
        ("32-bit", 3538847283, "54321 × 65123", "Seconds to break"),
        ("512-bit", "RSA-512", "Multiple factorizations", "Hours/days (2009)"),
    ]
    
    strong_examples = [
        ("1024-bit", "RSA-1024", "No known factorization", "Deprecated (2010)"),
        ("2048-bit", "RSA-2048", "Current minimum standard", "Secure until ~2030"),
        ("3072-bit", "RSA-3072", "Equivalent to AES-128", "Recommended for new systems"),
        ("4096-bit", "RSA-4096", "High security applications", "Long-term security"),
    ]
    
    print("\n[BAD] Weak key sizes (easy to break):")
    print("-" * 40)
    for size, example, factors, status in weak_examples:
        print(f"{size:>10}: {status}")
        if isinstance(example, int):
            print(f"          Example: n = {example} = {factors}")
        else:
            print(f"          {example} - {factors}")
    
    print("\n[GOOD] Strong key sizes (actually secure):")
    print("-" * 50)
    for size, example, factors, status in strong_examples:
        print(f"{size:>10}: {status}")
        print(f"          {factors}")
    
    print("\nWhat we learned:")
    print("• Each extra bit makes it way harder to crack")
    print("• 512-bit RSA got broken in 2009 (took a while but it happened)")
    print("• 1024-bit is old and not recommended anymore")
    print("• 2048-bit is the minimum now, 3072+ is better")
    print("• Quantum computers will eventually break all of these")

def demonstrate_attack_complexity():
    """Shows how much harder it gets to break bigger keys"""
    
    print("\n" + "="*60)
    print("HOW HARD IS IT TO BREAK RSA?")
    print("="*60)
    
    complexity_data = [
        ("512-bit", "2009", "~2^60 operations", "Months (distributed)"),
        ("768-bit", "2019", "~2^80 operations", "Years (academic)"), 
        ("1024-bit", "Not broken", "~2^86 operations", "Decades (estimated)"),
        ("2048-bit", "Not broken", "~2^112 operations", "Centuries (current tech)"),
    ]
    
    print("\n[+] FACTORIZATION RECORDS:")
    print(f"{'Key Size':<12} {'Status':<12} {'Complexity':<20} {'Time Required'}")
    print("-" * 65)
    
    for key_size, status, complexity, time_req in complexity_data:
        print(f"{key_size:<12} {status:<12} {complexity:<20} {time_req}")
    
    print("\nWhy bigger keys are so much better:")
    print("• Each extra bit roughly doubles how hard it is to crack")
    print("• 2048-bit keys are like 2^52 times harder than 512-bit")
    print("• Attackers use fancy algorithms (GNFS, QS) but still takes forever")
    print("• Quantum computers would make this all moot though")

def show_implementation_best_practices():
    """What you should actually do to make RSA secure"""
    
    print("\n" + "="*60)
    print("HOW TO DO RSA RIGHT")
    print("="*60)
    
    print("\nChecklist for secure RSA:")
    
    practices = [
        ("Key Size", "≥ 2048 bits (3072+ recommended for new systems)"),
        ("Prime Generation", "Cryptographically secure random number generator"),
        ("Prime Testing", "Multiple rounds of Miller-Rabin primality testing"),
        ("Public Exponent", "e = 65537 (F4) for security and efficiency"),
        ("Padding Scheme", "OAEP for encryption, PSS for signatures"),
        ("Key Validation", "Verify p ≠ q, proper size, no weak patterns"),
        ("Entropy Source", "Hardware RNG or well-seeded CSPRNG"),
        ("Key Storage", "Secure key management, consider HSMs"),
        ("Key Rotation", "Regular key updates, especially for long-term use"),
        ("Quantum Readiness", "Plan migration to post-quantum cryptography")
    ]
    
    for category, recommendation in practices:
        print(f"• {category:>15}: {recommendation}")
    
    print("\nCommon ways people mess up RSA:")
    
    vulnerabilities = [
        "Small key sizes (< 2048 bits)",
        "Predictable or poor quality randomness",
        "Shared primes across multiple keys", 
        "Weak padding schemes (e.g., PKCS#1 v1.5 for encryption)",
        "Low public exponents without proper padding",
        "Insufficient prime testing during generation",
        "Identical keys across device deployments",
        "Side-channel vulnerable implementations"
    ]
    
    for i, vuln in enumerate(vulnerabilities, 1):
        print(f"{i:>2}. {vuln}")

if __name__ == "__main__":
    demonstrate_key_size_security()
    demonstrate_attack_complexity()
    show_implementation_best_practices()
    
    print("\n" + "="*60)
    print("BOTTOM LINE: Doing the math right isn't enough!")
    print("You have to implement everything correctly too.")
    print("="*60)