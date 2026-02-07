#!/usr/bin/env python3
"""
Compute the Bateman-Horn correction factor C_Q for Q(n) = n^47 - (n-1)^47

The singular series is:
    C_Q = prod_{p prime} (1 - omega_Q(p)/p) / (1 - 1/p)

where omega_Q(p) is the number of roots of Q(n) = 0 (mod p).

For Q(n) = n^47 - (n-1)^47:
    - omega_Q(p) = 0   if p = 47 (ramified)
    - omega_Q(p) = 0   if p != 1 (mod 47) and p != 47 (inert / shielding)
    - omega_Q(p) = 46  if p = 1 (mod 47) (splitting)

The first splitting prime is p = 283.

Author: Ruqing Chen
Repository: https://github.com/Ruqing1963/Q47-Prime-Constellations
"""

import math


def sieve_primes(n: int) -> list:
    """Sieve of Eratosthenes up to n."""
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(2, n + 1) if is_prime[i]]


def omega_Q(p: int) -> int:
    """
    Compute omega_Q(p): the number of solutions to Q(n) = 0 (mod p).
    
    Theory:
        Q(n) = 0 (mod p)  <=>  n^47 = (n-1)^47 (mod p)
        Let z = n/(n-1). Then z^47 = 1 (mod p).
        
        If p = 47: Q(n) = n - (n-1) = 1 (mod 47), never zero. omega = 0.
        If p = 1 (mod 47): 47 | (p-1), so there are 47 roots of z^47=1.
            z=1 gives n=infinity (projective), so 46 finite solutions. omega = 46.
        Otherwise: gcd(47, p-1) = 1, only z=1 which is projective. omega = 0.
    """
    if p == 47:
        return 0
    elif (p - 1) % 47 == 0:
        return 46
    else:
        return 0


def compute_CQ(p_max: int = 100_000, verbose: bool = True) -> float:
    """
    Compute C_Q by evaluating the truncated Euler product up to p_max.
    
    C_Q = prod_{p <= p_max} (1 - omega_Q(p)/p) / (1 - 1/p)
    """
    primes = sieve_primes(p_max)
    
    C_Q = 1.0
    shielding_product = 1.0  # contribution from omega=0 primes
    n_shielding = 0
    n_splitting = 0
    
    milestones = {283, 1000, 5000, 10000, 50000, p_max}
    
    if verbose:
        print(f"Computing C_Q up to p = {p_max:,}")
        print(f"{'p':>8}  {'omega':>5}  {'local factor':>14}  {'C_Q (running)':>14}  {'type':>10}")
        print("-" * 60)
    
    for p in primes:
        w = omega_Q(p)
        local_factor = (1 - w / p) / (1 - 1 / p)
        C_Q *= local_factor
        
        if w == 0:
            shielding_product *= local_factor
            n_shielding += 1
        else:
            n_splitting += 1
        
        if verbose and (p <= 53 or p in milestones or (p < 300 and (p - 1) % 47 == 0)):
            ptype = "SPLIT" if w == 46 else ("ramified" if p == 47 else "shield")
            print(f"{p:>8}  {w:>5}  {local_factor:>14.6f}  {C_Q:>14.6f}  {ptype:>10}")
    
    if verbose:
        print("-" * 60)
        print()
        print(f"Results (product up to p = {p_max:,}):")
        print(f"  Shielding primes (omega=0):  {n_shielding}")
        print(f"  Splitting primes (omega=46): {n_splitting}")
        print(f"  Shielding product alone:     {shielding_product:.4f}")
        print(f"  Full C_Q:                    {C_Q:.4f}")
        print()
        
        # BH prediction
        N = 2e9
        ln_QN = math.log(47) + 46 * math.log(N)
        predicted = C_Q * N / ln_QN
        print(f"Bateman-Horn prediction at N = 2 x 10^9:")
        print(f"  ln(Q(N))  = {ln_QN:.1f}")
        print(f"  predicted = C_Q * N / ln(Q(N)) = {predicted:,.0f}")
        print(f"  observed  = 17,908,247")
        print(f"  ratio     = {17908247 / predicted:.4f}")
    
    return C_Q


def verify_omega_computationally(p_max: int = 300):
    """
    Brute-force verify omega_Q(p) for small primes by
    counting roots of Q(n) = 0 (mod p) directly.
    """
    primes = sieve_primes(p_max)
    
    print(f"Verifying omega_Q(p) by brute force for p <= {p_max}:")
    print(f"{'p':>6}  {'theory':>7}  {'brute':>6}  {'match':>6}")
    print("-" * 35)
    
    all_match = True
    for p in primes:
        # Brute force: count n in [0, p-1] with Q(n) = 0 (mod p)
        brute = sum(1 for n in range(p) if (pow(n, 47, p) - pow((n - 1) % p, 47, p)) % p == 0)
        theory = omega_Q(p)
        match = "OK" if brute == theory else "FAIL"
        if brute != theory:
            all_match = False
        
        if p <= 53 or (p - 1) % 47 == 0 or brute != theory:
            print(f"{p:>6}  {theory:>7}  {brute:>6}  {match:>6}")
    
    print("-" * 35)
    if all_match:
        print(f"  [PASS] All omega values verified for p <= {p_max}")
    else:
        print(f"  [FAIL] Some omega values mismatch!")
    print()
    return all_match


def main():
    print("=" * 60)
    print("  Bateman-Horn Correction Factor for Q(n) = n^47 - (n-1)^47")
    print("=" * 60)
    print()
    
    # Step 1: Verify omega values
    verify_omega_computationally(300)
    
    # Step 2: Compute full C_Q
    C_Q = compute_CQ(100_000, verbose=True)
    
    print()
    print(f"  >>> C_Q = {C_Q:.2f} <<<")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
