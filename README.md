# RSA Cryptography: Design, Security, and Vulnerabilities
**CS532 - Cryptography & Data Security**  
**Authors:** Taylor Hunter & Kelly Powell  
**Professor:** Jorge Novillo  
**Fall 2025**

## About This Project
Our final project digs into RSA cryptography - how it works, why it's important, and where things can go seriously wrong. We built some demos that show how weak RSA implementations can be broken in real-time, plus we researched the math behind why these attacks work.

## Project Structure
- `presentation/` - Our presentation slides and notes
  - `RSA_Presentation.md` - Main presentation slides
- `demo/` - Python scripts that actually break weak RSA keys
  - `weak_rsa_demo.py` - Shows factorization attack on small keys
  - `shared_prime_attack.py` - Demonstrates GCD attack on shared primes
  - `rsa_comparison_demo.py` - Compares security across key sizes
  - `DEMO_SCRIPTS.md` - Notes on how to present the demos
  - `MATHEMATICAL_ANALYSIS.md` - Math explanations behind the attacks

## How to Run Our Demos
Make sure you have Python 3.6+ installed, then:

```bash
# Shows how to break RSA keys that are too small
python demo/weak_rsa_demo.py

# Demonstrates the shared prime vulnerability from the 2012 research  
python demo/shared_prime_attack.py

# Compares security levels across different key sizes
python demo/rsa_comparison_demo.py
```

All the demos include step-by-step math so you can see exactly what's happening.

## What We Found Out
- **Key size matters a LOT**: anything under 2048 bits can be broken pretty quickly now
- **Random numbers are critical**: bad randomness means multiple keys might share prime factors
- **Real-world impact**: Heninger et al. found 0.4% of internet RSA keys were instantly breakable in 2012
- **Implementation vs theory**: you can get the math 100% right and still have a completely insecure system
- **Attack methods**: we implemented Pollard's Rho factorization and GCD attacks to show these aren't just theoretical

## Cool Math Stuff We Learned
- How RSA key generation actually works (p, q primes → n = p×q → φ(n) = (p-1)(q-1) → find d)
- Why factorization is hard but GCD is easy (and how that breaks shared prime keys)
- The exponential relationship between key size and security level
- How Shor's algorithm will eventually break all of this with quantum computers

## Sources
We based this on research from Boneh (2007), Heninger et al. (2012), Paar/Pelzl/Güneysu textbook (2024), and current NIST recommendations. Full citations are in our presentation slides.

## Note
This is educational code for a class project. Don't use any of this in production systems (obviously)!