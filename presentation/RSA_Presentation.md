# RSA Cryptography: Design, Security Foundations, and Weak-Key Vulnerabilities

**Authors:** Taylor Hunter & Kelly Powell  
**Institution:** SUNY Polytechnic Institute  
**Course:** CS532 - Cryptography & Data Security  
**Professor:** Jorge Novillo  
**Date:** December 1st, 2025

---

## What We'll Cover Today
1. **What is RSA and why it matters**
2. **How it changed cryptography**
3. **The math behind RSA**
4. **Problems we found in RSA**
5. **Real vulnerabilities in the wild**
6. **Our coding demos**
7. **What this means going forward**
8. **Sources we used**

---

## 1. Introduction to RSA

### What is RSA?
- Public-key crypto system from 1978
- Made by Rivest, Shamir, and Adleman (hence "RSA")  
- Big deal: you can encrypt stuff without sharing a secret key first

### Why This Was Huge
- Before RSA: everyone had to use the same secret key
- Problem: how do you share that key safely? Meet in person? Mail it?
- RSA fixed this: one key for encryption (public), different key for decryption (private)

### The Math Idea
- Easy direction: multiply two big prime numbers together
- Hard direction: factor that big number back into the original primes
- This asymmetry is what makes RSA secure (when done right)

---

## 2. Connection to Cryptography Field

### Fixing the Key Problem
- Old crypto: if you have 100 people, you need like 5000 different key exchanges 
- Gets crazy fast - scales quadratically which is bad
- RSA: just publish your public key, keep private key secret

### Where We Use RSA Today
- HTTPS websites (like when you see the lock icon)
- Code signing - so your computer knows software is legit
- Email encryption (PGP and S/MIME)
- Digital certificates - the whole PKI infrastructure
- IoT devices (though this is where problems happen...)

### Why We're Studying This
- Good example of math theory actually working in practice
- Shows concepts like modular arithmetic, prime numbers, computational complexity
- But also shows how theory vs implementation can go wrong

---

## 3. How RSA Works

### Setting Up Keys (the tricky part)
1. Pick two big random prime numbers: p and q
2. Multiply them: n = p × q  
3. Calculate φ(n) = (p-1)(q-1) - this is Euler's totient function
4. Pick e (usually 65537 because it works well and is fast)
   - Just needs gcd(e, φ(n)) = 1
5. Find d where d ≡ e⁻¹ (mod φ(n)) - this is the hard math part

### Actually Using RSA
- Encrypt: c = m^e mod n
- Decrypt: m = c^d mod n  
- Why this works: because of how we set up d and e, the math cancels out

### What You Share vs Keep Secret
- Public key: (e, n) - anyone can have this
- Private key: (d, n) - only you know this
- Security depends on: can't figure out d without knowing p and q

---

## 4. Main Issues and Problems

### 4.1 Keys Too Small
- Old 512-bit keys can be broken now (was done in 2009)
- Need at least 2048 bits today, 3072+ is better
- With cloud computing and GPUs, small keys don't stand a chance

### 4.2 Bad Random Numbers (This is a Big One!)
- 2012 study found 0.4% of internet RSA keys could be broken instantly
- Problem: devices using crappy random number generators
- If two different keys accidentally use the same prime - both keys are toast

### 4.3 Implementation Mistakes  
- Using e=3 without proper padding = bad idea
- PKCS #1 padding done wrong leads to attacks
- Lots of ways to mess up the implementation even if math is right

### 4.4 Speed Issues
- RSA is really slow compared to AES and other symmetric crypto
- Usually only used to encrypt small things like session keys
- Not practical for encrypting large files directly

### 4.5 Quantum Computers (Future Problem)
- Shor's algorithm would break ALL RSA keys if we had big quantum computers
- Not a problem today but we need to plan for it

---

## 5. Weak Implementation Vulnerabilities

### Real-World Consequences
- **Complete security failure:** Loss of confidentiality, authentication, integrity
- **IoT vulnerabilities:** Identical firmware with same private keys
- **Pattern detection:** Attackers can exploit insufficient entropy

### Common Implementation Errors
1. **Identical random seeds** across devices
2. **Insufficient entropy** during key generation
3. **Poorly chosen primes** with detectable patterns
4. **Incorrect padding** implementations

### Case Studies
- **Heninger et al. (2012):** Millions of weak keys in network devices
- **IoT security failures:** Mass deployment of identical keys
- **Academic demonstrations:** Concurrent factorization attacks

---

## 6. Hands-On Demonstration

### Live Code Demo: Breaking Weak RSA
**File:** `demo/weak_rsa_demo.py`

### Demonstration Setup
```python
# Generate intentionally weak RSA keys
p = generate_small_prime(16)  # 16-bit prime (~5 digits)
q = generate_small_prime(16)  # 16-bit prime (~5 digits)
n = p * q                     # 32-bit modulus (DANGEROUSLY SMALL)
```

### Attack Simulation
1. **Key Generation:** Create RSA keypair with 16-bit primes
2. **Encryption:** Encrypt secret message with public key
3. **Attack Phase:** Factorize n using Pollard's Rho algorithm
4. **Key Recovery:** Recompute private exponent d from factors
5. **Message Recovery:** Decrypt ciphertext with recovered key

### Expected Demo Output
```
[+] WEAK RSA PARAMETERS
p = 54321 (16-bit prime)
q = 65123 (16-bit prime)  
n = 3538847283 (32-bit modulus)
[!] WARNING: This key size is DANGEROUSLY SMALL!

[+] ATTACK PHASE
[*] Factorization SUCCESSFUL in 0.0023 seconds!
[!] ATTACK SUCCESSFUL - secret message recovered!
```

### Key Demonstration Points
- **Instant factorization:** Sub-second attack on weak keys
- **Complete compromise:** Private key fully recovered
- **Educational impact:** Shows vulnerability consequences
- **Real-world relevance:** Mirrors actual IoT device vulnerabilities

### Technical Implementation
- **Pollard's Rho Algorithm:** Efficient factorization for demonstration
- **Modular arithmetic:** Shows RSA mathematical operations
- **Attack timeline:** Demonstrates speed of compromise
- **Vulnerability analysis:** Connects to academic research findings

---

## 7. What We Learned

### RSA Is Still Important
- Still used everywhere even though it's from 1978
- Good for learning how crypto theory actually works in practice  
- Tons of systems still depend on it working right

### What Makes RSA Actually Secure
- Key size matters: use 2048+ bits, not the tiny ones we demo'd
- Random numbers need to be really random (not predictable)
- Implementation details matter - lots of ways to mess up
- Keep up with security recommendations as they change

### Looking Forward
- Quantum computers will eventually break all RSA (Shor's algorithm)
- We'll need post-quantum crypto, but that's still being figured out
- For now, RSA works if you do it right
- Worth understanding since it's not going away soon

### Main Point
**The math can be perfect but if you implement it wrong, you're toast. RSA shows how theory and practice both matter in crypto.**

---

## References

1. Almazari, Mahmoud M., et al. "RSA Private Keys and the Presence of Weak Keys: An Evaluation." *Journal of Discrete Mathematical Sciences and Cryptography*, July 2022.

2. Boneh, Dan. "Twenty Years of Attacks on the RSA Cryptosystem." *Notices of the AMS*, 2007.

3. Gerjuoy, Edward. "Shor's Factoring Algorithm and Modern Cryptography." *American Journal of Physics*, vol. 72, no. 5, 2004.

4. Heninger, Nadia, et al. "Detection of Widespread Weak Keys in Network Devices." *USENIX Security Symposium*, 2012.

5. Just, Jiri, and John Coffey. "An Assessment of Attacks Strategies on the RSA Public-Key Cryptosystem." *International Institute of Informatics and Systemics*, 2009.

6. Kilgallin, Jonathan, and Ross Vasko. "Factoring RSA Keys in the IoT Era." *IEEE/Keyfactor*, 2019.

7. Maitra, Subhamoy, and S. Sarkar. "Revisiting Wiener's Attack: New Weak Keys in RSA." *Lecture Notes in Computer Science*, vol. 5222, Springer, 2008.

8. Paar, Christof, Jan Pelzl, and Tim Güneysu. *Understanding Cryptography: From Established Symmetric and Public-Key Primitives to Advanced Protocols*. 2nd ed., Springer Spektrum, 2024.

9. Rivest, Ronald L., Adi Shamir, and Leonard Adleman. "A Method for Obtaining Digital Signatures and Public-Key Cryptosystems." *Communications of the ACM*, vol. 21, no. 2, 1978.

10. Ruzai, W. N. A., et al. "Concurrent Factorization of RSA Moduli via Weak Key Conditions." *AIMS Mathematics*, vol. 9, no. 5, 2024.

---

## Running the Live Demonstrations

### Three Demo Options for Maximum Impact

#### **Demo 1: Weak Key Factorization** *(Primary - Must Run)*
```cmd
python demo/weak_rsa_demo.py
```
- **Duration:** ~30 seconds
- **Shows:** Instant factorization of weak RSA keys
- **Impact:** Dramatic demonstration of vulnerability

#### **Demo 2: Shared Prime Attack** *(Secondary - High Impact)*
```cmd
python demo/shared_prime_attack.py  
```
- **Duration:** ~45 seconds
- **Shows:** How identical primes compromise multiple keys instantly
- **Impact:** Demonstrates Heninger et al. research findings

#### **Demo 3: Security Comparison** *(Optional - Educational)*
```cmd
python demo/rsa_comparison_demo.py
```
- **Duration:** ~20 seconds
- **Shows:** Key size security levels and best practices
- **Impact:** Educational summary of implementation guidelines

