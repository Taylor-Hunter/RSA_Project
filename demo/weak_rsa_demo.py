# weak_rsa_demo.py
# CS532 Project - shows how weak RSA keys can be broken
# Taylor Hunter & Kelly Powell

import random
from math import gcd

# Helper functions we need

def modinv(a, m):
    """Calculate modular inverse using extended euclidean algorithm
    Found this algorithm online and adapted it for our use"""
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
    if n < 2:
        return False
    # small primes
    for p in [2, 3, 5, 7, 11, 13, 17, 19]:
        if n == p:
            return True
        if n % p == 0:
            return False
    # write n-1 = 2^r * d
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

def generate_small_prime(bits=16):
    """Generate a small prime (16 bits by default)."""
    while True:
        candidate = random.getrandbits(bits)
        candidate |= 1  # make odd
        if is_probable_prime(candidate):
            return candidate

def pollards_rho(n):
    """Pollard's Rho factorization algorithm (for DEMO on small n)."""
    if n % 2 == 0:
        return 2
    x = random.randrange(2, n - 1)
    y = x
    c_const = random.randrange(1, n - 1)
    d = 1
    f = lambda v: (pow(v, 2, n) + c_const) % n

    while d == 1:
        x = f(x)
        y = f(f(y))
        d = gcd(abs(x - y), n)
        if d == n:
            # retry with different parameters
            return pollards_rho(n)
    return d

# ---------- Weak RSA Setup ----------

def generate_weak_rsa():
    """Make a weak RSA key with small primes (for demo purposes)"""
    print("[*] Making RSA key with tiny primes (don't try this at home)...")
    p = generate_small_prime(16)  # 16-bit prime
    q = generate_small_prime(16)
    while p == q:  # make sure they're different (learned this the hard way)
        q = generate_small_prime(16)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    if gcd(e, phi) != 1:
        # fall back to a small odd exponent
        for candidate in range(3, 1000, 2):
            if gcd(candidate, phi) == 1:
                e = candidate
                break

    d = modinv(e, phi)
    return (e, n), (d, n), p, q, phi

def encrypt_int(m, public_key):
    e, n = public_key
    return pow(m, e, n)

def decrypt_int(c, private_key):
    d, n = private_key
    return pow(c, d, n)

# ---------- Demo ----------

if __name__ == "__main__":
    print("="*50)
    print("BREAKING WEAK RSA KEYS - CS532 Project Demo")
    print("By: Taylor Hunter & Kelly Powell")  
    print("="*50)
    print("This shows what happens when RSA keys are too small")
    
    # 1) Generate WEAK RSA keys
    pub, priv, p, q, phi = generate_weak_rsa()
    e, n = pub
    d, _ = priv

    print("\n[+] Generating the RSA key (following the textbook steps)")
    print("Step 1: Pick two primes")
    print(f"   p = {p} (small 16-bit prime)")
    print(f"   q = {q} (small 16-bit prime)")
    
    print("\nStep 2: Calculate n = p * q")
    print(f"   n = {p} * {q} = {n}")
    print(f"   This gives us a {n.bit_length()}-bit modulus")
    
    print("\nStep 3: Calculate phi(n) = (p-1)*(q-1)")
    print(f"   phi(n) = ({p}-1) * ({q}-1) = {phi}")
    
    print("\nStep 4: Pick e (we'll use the common choice)")
    print(f"   e = {e}")
    print(f"   Check: gcd({e}, {phi}) = {gcd(e, phi)} ✓")
    
    print("\nStep 5: Find d where e*d ≡ 1 (mod phi(n))")
    print(f"   d = {d}")
    print(f"   Verify: {e}*{d} mod {phi} = {(e*d) % phi} (should be 1)")
    
    print(f"\nGenerated keypair:")
    print(f"   Public:  (e={e}, n={n})")
    print(f"   Private: (d={d}, n={n})")
    
    print(f"\n!! WARNING: {n.bit_length()}-bit key is TINY!")
    print(f"   Real RSA needs 2048+ bits to be secure")
    print(f"   This will break in seconds...")

    # 2) Encrypt a secret message
    msg = 42
    print("\n[+] Now let's encrypt a message")
    print("Using the standard RSA formula: c = m^e mod n")
    print(f"\nMessage to encrypt: {msg}")
    print(f"Using public key: e={e}, n={n}")
    print("\nDoing the math:")
    print(f"   {msg}^{e} mod {n}")
    c = encrypt_int(msg, pub)
    print(f"   = {c}")
    print(f"\nEncrypted message: {c}")
    print("(Note: {msg}^{e} is huge - thousands of digits! - so we use modular arithmetic)")

    # 3) Simulate attacker with only public information
    print("\n[+] Now for the attack!")
    print("[*] Pretend we're a hacker who only knows the public key and ciphertext")
    print("[*] Let's try to factor n using Pollard's Rho...")
    print("    (This should be impossible for real RSA keys)")
    
    import time
    start_time = time.time()
    factor = pollards_rho(n)
    end_time = time.time()
    
    other_factor = n // factor
    if factor > other_factor:
        factor, other_factor = other_factor, factor
    
    print(f"[+] FACTORIZATION SUCCESSFUL in {end_time - start_time:.4f} seconds!")
    print(f"    Recovered factors: p = {factor}, q = {other_factor}")

    # 4) Recompute private key from attacker's perspective
    print("\n[+] MATHEMATICAL KEY RECOVERY")
    print("="*50)
    print("Step 1: Use recovered primes to recompute φ(n)")
    phi_attack = (factor - 1) * (other_factor - 1)
    print(f"   φ(n) = (p-1)(q-1) = ({factor}-1)×({other_factor}-1)")
    print(f"   φ(n) = {factor-1} × {other_factor-1} = {phi_attack}")
    
    print("\nStep 2: Recompute private exponent d")
    print(f"   d ≡ e⁻¹ (mod φ(n))")
    print(f"   d ≡ {e}⁻¹ (mod {phi_attack})")
    d_attack = modinv(e, phi_attack)
    print(f"   d = {d_attack}")
    
    print("\nStep 3: Verify correctness")
    print(f"   Original d = {d}")
    print(f"   Recovered d = {d_attack}")
    print(f"   Match: {d == d_attack} ✓" if d == d_attack else f"   Match: {d == d_attack} ✗")

    # 5) Decrypt with the recovered private key
    print("\n[+] RSA DECRYPTION MATHEMATICS")
    print("="*50)
    print("RSA Decryption Formula: m ≡ cᵈ (mod n)")
    print(f"\nCiphertext: c = {c}")
    print(f"Recovered private key: d = {d_attack}")
    print("\nDecryption calculation:")
    print(f"   m ≡ {c}^{d_attack} (mod {n})")
    m_recovered = pow(c, d_attack, n)
    print(f"   m = {m_recovered}")
    print(f"\nRecovered plaintext: {m_recovered}")
    print(f"Original message:    {msg}")
    print(f"Attack successful:   {m_recovered == msg} ✓" if m_recovered == msg else f"Attack successful: {m_recovered == msg} ✗")

    if m_recovered == msg:
        print(f"\n{'='*60}")
        print("[!] ATTACK SUCCESSFUL!")
        print("[!] Weak RSA completely broken - secret message recovered!")
        print(f"[!] Original message: {msg}")
        print(f"[!] Recovered message: {m_recovered}")
        print("="*60)
    else:
        print("[!] Something went wrong; recovered message does not match.")

    # 6) Educational summary
    print(f"\n[+] VULNERABILITY ANALYSIS")
    print("This demonstrates why proper RSA implementation is critical:")
    print(f"• Small key size ({n.bit_length()} bits) enables instant factorization")
    print("• Modern standards require 2048+ bit keys")
    print("• Weak random number generation creates exploitable patterns")
    print("• Implementation errors can completely compromise RSA security")
    print("\nReal-world impact: Heninger et al. (2012) found 0.4% of internet")
    print("RSA keys shared factors due to similar implementation weaknesses.")