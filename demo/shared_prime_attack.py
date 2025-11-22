# shared_prime_attack.py
# Demonstration of RSA vulnerability when keys share common prime factors
# Based on Heninger et al. (2012) research findings

import random
from math import gcd

def modinv(a, m):
    """Modular inverse via Extended Euclidean Algorithm."""
    r0, r1 = a, m
    s0, s1 = 1, 0
    t0, t1 = 0, 1
    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
        t0, t1 = t1, t0 - q * t1
    if r0 != 1:
        raise ValueError("No modular inverse")
    return s0 % m

def is_probable_prime(n, k=8):
    """Miller-Rabin primality test."""
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19]:
        if n == p:
            return True
        if n % p == 0:
            return False
    
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    for _ in range(k):
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits=20):
    """Generate a prime of specified bit length."""
    while True:
        candidate = random.getrandbits(bits)
        candidate |= 1  # make odd
        if is_probable_prime(candidate):
            return candidate

def generate_rsa_keypair(p, q):
    """Generate RSA keypair from given primes."""
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Use e = 65537 if possible, otherwise find suitable e
    e = 65537
    if gcd(e, phi) != 1:
        for candidate in range(3, 1000, 2):
            if gcd(candidate, phi) == 1:
                e = candidate
                break
    
    d = modinv(e, phi)
    return (e, n), (d, n)

def simulate_weak_random_generation():
    """Simulate poor random number generation that produces shared primes."""
    print("="*60)
    print("SHARED PRIME ATTACK DEMO")
    print("CS532 Project - Taylor Hunter & Kelly Powell")
    print("Recreating the 2012 study that found weak keys on the internet")
    print("="*60)
    
    # Simulate a scenario where devices use insufficient entropy
    print("\n[+] SCENARIO: Devices with crappy random number generators")
    print("    (Like IoT devices that all use the same firmware)")
    
    # Generate a small pool of "weak" primes that might be reused
    print("\n[*] Making a small pool of primes (pretending we have bad entropy)...")
    weak_prime_pool = []
    for i in range(5):
        p = generate_prime(20)  # 20-bit primes for demo
        weak_prime_pool.append(p)
        print(f"    Prime {i+1}: {p}")
    
    # Simulate multiple "devices" generating RSA keys
    devices = []
    print(f"\n[*] Simulating 8 devices generating RSA keys...")
    print(f"[!] Some devices will accidentally reuse primes due to weak randomness")
    
    for device_id in range(8):
        # Simulate poor randomness - sometimes reuse primes
        if random.random() < 0.3:  # 30% chance of reusing a prime
            p = random.choice(weak_prime_pool)
            print(f"    Device {device_id+1}: REUSING prime {p}")
        else:
            p = random.choice(weak_prime_pool)
        
        q = random.choice(weak_prime_pool)
        while q == p:
            q = random.choice(weak_prime_pool)
        
        pub_key, priv_key = generate_rsa_keypair(p, q)
        devices.append({
            'id': device_id + 1,
            'p': p,
            'q': q, 
            'n': pub_key[1],
            'public_key': pub_key,
            'private_key': priv_key
        })
        print(f"    Device {device_id+1}: n = {pub_key[1]} (p={p}, q={q})")
    
    return devices

def attack_shared_primes(devices):
    """Demonstrate attack when RSA keys share prime factors."""
    print("\n[+] SHARED PRIME ATTACK MATHEMATICS")
    print("="*60)
    print("Attack Principle: If gcd(n₁, n₂) > 1, then n₁ and n₂ share a prime factor")
    print("\nMathematical basis:")
    print("   If n₁ = p × q₁ and n₂ = p × q₂ (shared prime p)")
    print("   Then gcd(n₁, n₂) = gcd(p×q₁, p×q₂) = p")
    print("   Once p is found: q₁ = n₁/p and q₂ = n₂/p")
    print("   Both RSA keys are immediately broken!")
    
    print("\n[*] Collecting public moduli from all devices...")
    
    # Extract all moduli (public information)
    moduli = [(device['id'], device['n']) for device in devices]
    
    print(f"\n[*] Computing GCD between all pairs of moduli...")
    vulnerabilities_found = []
    
    for i in range(len(moduli)):
        for j in range(i + 1, len(moduli)):
            device1_id, n1 = moduli[i]
            device2_id, n2 = moduli[j]
            
            shared_factor = gcd(n1, n2)
            
            if shared_factor > 1 and shared_factor != n1 and shared_factor != n2:
                print(f"\n[!] VULNERABILITY FOUND!")
                print(f"    Devices {device1_id} and {device2_id} share prime factor: {shared_factor}")
                
                # Extract both primes for both devices
                other_factor1 = n1 // shared_factor
                other_factor2 = n2 // shared_factor
                
                vulnerabilities_found.append({
                    'device1': device1_id,
                    'device2': device2_id,
                    'shared_prime': shared_factor,
                    'n1': n1,
                    'n2': n2,
                    'p1': shared_factor,
                    'q1': other_factor1,
                    'p2': shared_factor,
                    'q2': other_factor2
                })
                
                print(f"    Device {device1_id}: p={shared_factor}, q={other_factor1}")
                print(f"    Device {device2_id}: p={shared_factor}, q={other_factor2}")
    
    return vulnerabilities_found

def demonstrate_key_recovery(devices, vulnerabilities):
    """Show how shared primes lead to complete key compromise."""
    if not vulnerabilities:
        print("\n[*] No shared primes found in this simulation.")
        return
    
    print(f"\n[+] PRIVATE KEY RECOVERY")
    print(f"[*] Demonstrating complete compromise of affected devices...")
    
    for vuln in vulnerabilities:
        device1_id = vuln['device1']
        device2_id = vuln['device2']
        
        # Find the actual device objects
        device1 = next(d for d in devices if d['id'] == device1_id)
        device2 = next(d for d in devices if d['id'] == device2_id)
        
        print(f"\n[*] Recovering private keys for devices {device1_id} and {device2_id}:")
        
        # Recover device 1 private key
        p1, q1 = vuln['p1'], vuln['q1']
        phi1 = (p1 - 1) * (q1 - 1)
        e1 = device1['public_key'][0]
        d1_recovered = modinv(e1, phi1)
        
        # Recover device 2 private key  
        p2, q2 = vuln['p2'], vuln['q2']
        phi2 = (p2 - 1) * (q2 - 1)
        e2 = device2['public_key'][0]
        d2_recovered = modinv(e2, phi2)
        
        print(f"    Device {device1_id} private key recovered: d = {d1_recovered}")
        print(f"    Device {device2_id} private key recovered: d = {d2_recovered}")
        
        # Verify recovery was successful
        original_d1 = device1['private_key'][0]
        original_d2 = device2['private_key'][0]
        
        if d1_recovered == original_d1 and d2_recovered == original_d2:
            print(f"    ✓ BOTH PRIVATE KEYS SUCCESSFULLY RECOVERED!")
        else:
            print(f"    ✗ Key recovery failed")

def show_real_world_impact():
    """Display information about real-world implications."""
    print(f"\n" + "="*70)
    print("REAL-WORLD IMPACT & RESEARCH FINDINGS")
    print("="*70)
    
    print("\n[+] Heninger et al. (2012) Study Results:")
    print("    • Analyzed 6.2 million RSA public keys from the internet")
    print("    • Found 0.4% shared prime factors due to weak randomness")
    print("    • 64,081 keys were immediately compromised")
    print("    • Affected routers, firewalls, and embedded devices")
    
    print("\n[+] Common Causes of Shared Primes:")
    print("    • Insufficient entropy during key generation")
    print("    • Identical random number generator seeds")
    print("    • Poor quality random number generators")  
    print("    • Mass deployment of identical firmware")
    print("    • Virtual machines with predictable states")
    
    print("\n[+] Attack Efficiency:")
    print("    • GCD computation is extremely fast O(log n)")
    print("    • Can check millions of key pairs quickly")
    print("    • No advanced mathematical techniques required")
    print("    • Attack scales to internet-wide key scanning")
    
    print("\n[+] Mitigation Strategies:")
    print("    • Use cryptographically secure random number generators")
    print("    • Ensure sufficient entropy before key generation")
    print("    • Generate unique keys per device")
    print("    • Regular key rotation and monitoring")
    print("    • Hardware security modules (HSMs) for key generation")

if __name__ == "__main__":
    # Run the complete demonstration
    devices = simulate_weak_random_generation()
    vulnerabilities = attack_shared_primes(devices)
    demonstrate_key_recovery(devices, vulnerabilities)
    show_real_world_impact()
    
    print(f"\n" + "="*70)
    print("DEMONSTRATION COMPLETE")
    print("This attack requires only PUBLIC KEYS - no advanced cryptanalysis needed!")
    print("="*70)