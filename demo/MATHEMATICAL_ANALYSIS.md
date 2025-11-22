# RSA Math Notes and Attack Details
**By:** Taylor Hunter & Kelly Powell  
**Class:** CS532 - Cryptography & Data Security  
**Notes:** Math behind our RSA demos - formulas and why the attacks work

---

## How RSA Actually Works (The Math Part)

### **Setting up RSA Keys**
This is the process we follow in our code (same as the textbook):

1. **Pick Two Primes:**
   ```
   Get two different prime numbers p and q
   They need to be random and big (ours are tiny for the demo)
   ```

2. **Make the Modulus:**
   ```
   n = p × q
   The security comes from: easy to multiply, hard to factor back
   ```

3. **Totient Function:**
   ```
   φ(n) = (p-1)(q-1)
   Counts integers ≤ n that are coprime to n
   ```

4. **Public Exponent Selection:**
   ```
   Choose e such that gcd(e, φ(n)) = 1
   Common choice: e = 65537 = 2¹⁶ + 1 (Fermat prime F₄)
   ```

5. **Private Exponent Computation:**
   ```
   d ≡ e⁻¹ (mod φ(n))
   Ensures: ed ≡ 1 (mod φ(n))
   ```

### **RSA Encryption/Decryption Mathematics**

**Encryption:**
```
c ≡ mᵉ (mod n)
where: m = plaintext, c = ciphertext, (e,n) = public key
```

**Decryption:**
```
m ≡ cᵈ (mod n)
where: d = private exponent, (d,n) = private key
```

**Mathematical Correctness Proof:**
```
m ≡ cᵈ ≡ (mᵉ)ᵈ ≡ mᵉᵈ ≡ m¹ ≡ m (mod n)
Since ed ≡ 1 (mod φ(n)) by Euler's theorem
```

---

## Attack Mathematics

### **1. Factorization Attack (Demo 1)**

**Vulnerability:** Small modulus n enables efficient factorization

**Pollard's Rho Algorithm:**
```
Goal: Find non-trivial factor of n
Method: Detect cycle in sequence xᵢ₊₁ = (xᵢ² + c) mod n
Complexity: O(√p) where p is smallest prime factor
For small n: Nearly instant factorization
```

**Attack Steps:**
1. **Factor n:** Use Pollard's Rho to find p, q where n = p × q
2. **Compute φ(n):** φ(n) = (p-1)(q-1)  
3. **Recover d:** d ≡ e⁻¹ (mod φ(n))
4. **Decrypt:** m ≡ cᵈ (mod n)

**Time Complexity:**
- 512-bit RSA: ~2⁶⁰ operations (months with distributed computing)
- 32-bit RSA (demo): ~2¹⁶ operations (milliseconds)

### **2. Shared Prime Attack (Demo 2)**

**Vulnerability:** Poor randomness causes prime reuse across keys

**Mathematical Principle:**
```
If n₁ = p × q₁ and n₂ = p × q₂ (shared prime p)
Then gcd(n₁, n₂) = p
```

**Euclidean GCD Algorithm:**
```
gcd(a,b): 
  while b ≠ 0:
    a, b = b, a mod b
  return a
Complexity: O(log min(a,b))
```

**Attack Steps:**
1. **Collect moduli:** Gather public keys (n₁, e₁), (n₂, e₂), ...
2. **Compute GCDs:** For all pairs (nᵢ, nⱼ), compute gcd(nᵢ, nⱼ)
3. **Find shared primes:** If gcd(nᵢ, nⱼ) > 1, then gcd = shared prime p
4. **Factor both keys:** 
   - q₁ = n₁/p, q₂ = n₂/p
   - φ(n₁) = (p-1)(q₁-1), φ(n₂) = (p-1)(q₂-1)
   - d₁ ≡ e₁⁻¹ (mod φ(n₁)), d₂ ≡ e₂⁻¹ (mod φ(n₂))

**Efficiency:**
- GCD computation: Extremely fast O(log n)
- Scales to internet-wide key analysis
- Can check millions of key pairs quickly

### **3. Security Level Analysis**

**Key Size vs Security:**
```
Bit Length | Security Level | Attack Complexity
-----------+----------------+------------------
512        | Broken (2009)  | ~2⁶⁰ operations
768        | Broken (2019)  | ~2⁸⁰ operations  
1024       | Deprecated     | ~2⁸⁶ operations
2048       | Current min    | ~2¹¹² operations
3072       | Recommended    | ~2¹²⁸ operations
4096       | High security  | ~2¹⁵⁰ operations
```

**Exponential Security Growth:**
- Each bit doubles difficulty approximately
- 2048-bit keys are ~2⁵² times harder than 512-bit
- Quantum computers reduce all to polynomial time (Shor's algorithm)

---

## Real-World Vulnerability Mathematics

### **Heninger et al. (2012) Study Results:**

**Data Set:**
- 6.2 million RSA public keys analyzed
- Keys collected from internet-facing devices
- Routers, firewalls, embedded systems

**Mathematical Findings:**
```
Vulnerable keys: 64,081 (0.4% of total)
Attack method: GCD computation between all pairs
Shared factors found: Due to insufficient entropy
Time to break: Seconds (once shared prime identified)
```

**Statistical Analysis:**
```
P(two keys share factor) ≈ 2/√πN for N-bit primes
With poor randomness: P increases dramatically
Result: Measurable fraction of real keys vulnerable
```

### **Implementation Vulnerability Patterns:**

**Insufficient Entropy:**
```
Entropy requirement: ≥128 bits for cryptographic security
Poor sources: System clock, process IDs, predictable seeds
Result: Repeated or similar prime generation
```

**Identical Firmware:**
```
Problem: Same random seed across device deployments  
Mathematical impact: Identical (p,q) pairs generated
Attack result: All affected devices share same private key
```

**Predictable Random Number Generators:**
```
Linear Congruential Generators: xₙ₊₁ = (axₙ + c) mod m
Problem: Predictable sequence if parameters/seed known
Impact: Attacker can predict generated primes
```

---

## Mathematical Validation of Demonstrations

### **Demo 1 Validation:**
Our weak RSA demonstration generates keys with:
- 16-bit primes (vs. required 1024+ bits)
- 32-bit modulus (vs. required 2048+ bits)
- Factorization time: <1 second (vs. required centuries)

This mathematically proves the exponential security relationship.

### **Demo 2 Validation:**  
Our shared prime attack recreates:
- GCD-based attack methodology from Heninger et al.
- Multiple device compromise scenario
- Statistical vulnerability patterns found in real deployments

This validates the mathematical principles behind the published research.

### **Academic Research Connection:**
Both demonstrations implement the exact mathematical techniques described in:
- Boneh (2007): RSA attack overview and complexity analysis
- Heninger et al. (2012): Shared prime vulnerability discovery  
- Paar, Pelzl, Güneysu (2024): RSA mathematical foundations

---

## Cryptographic Implications

### **One-Way Function Property:**
```
Forward direction (key generation): Fast
  p, q → n = p×q (polynomial time)

Reverse direction (factorization): Hard  
  n → p, q (sub-exponential time for proper key sizes)
```

**RSA Security Assumption:**
> The difficulty of factoring large composite integers is computationally infeasible

**Implementation Reality:**
> Security assumption only holds with proper implementation:
> - Sufficient key sizes (≥2048 bits)
> - Cryptographically secure randomness  
> - Proper parameter validation
> - Secure padding schemes

### **Mathematical vs. Implementation Security:**

**Mathematical Correctness ≠ Cryptographic Security**

A mathematically valid RSA implementation can be:
- ✓ Mathematically correct (ed ≡ 1 (mod φ(n)))
- ✗ Cryptographically broken (factorizable modulus)

Our demonstrations prove this critical distinction through practical attacks on mathematically valid but improperly implemented RSA systems.

---

## Conclusion

The mathematical analysis demonstrates that RSA's security depends entirely on proper implementation of the underlying number-theoretic principles. While the algorithm's mathematical foundation is elegant and theoretically sound, real-world security requires careful attention to:

1. **Sufficient key sizes** to ensure factorization remains computationally infeasible
2. **Quality randomness** to prevent shared prime vulnerabilities  
3. **Proper parameter validation** throughout the key generation process
4. **Implementation best practices** that translate mathematical theory into practical security

Our demonstrations provide concrete mathematical evidence supporting the academic research findings and validate the critical importance of implementation quality in cryptographic systems.