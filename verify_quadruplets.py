#!/usr/bin/env python3
"""
Verification Scripts for Q(n) = n^47 - (n-1)^47 Prime Constellations

Author: Ruqing Chen
Repository: https://github.com/Ruqing1963/Q47-Prime-Constellations
"""

import random
from typing import List, Tuple

def Q(n: int) -> int:
    """Compute Q(n) = n^47 - (n-1)^47"""
    return n**47 - (n-1)**47

def is_prime_miller_rabin(n: int, k: int = 25) -> bool:
    """Miller-Rabin primality test with k rounds"""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Test with k witnesses
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def verify_exclusion_theorem(max_n: int = 1_000_000) -> bool:
    """
    Verify the Structural Exclusion Theorem:
    Q(n) = 1 (mod 3) for all n >= 2
    
    This implies Q(n) + 2 = 0 (mod 3), so (Q(n), Q(n)+2) can never both be prime.
    """
    print(f"Verifying Exclusion Theorem for n in [2, {max_n:,}]...")
    
    for n in range(2, max_n + 1):
        q = Q(n)
        if q % 3 != 1:
            print(f"FAILED at n = {n}: Q({n}) = {q % 3} (mod 3)")
            return False
        
        if n % 100_000 == 0:
            print(f"  Verified up to n = {n:,}")
    
    print(f"  [PASS] Exclusion Theorem verified for all n in [2, {max_n:,}]")
    return True

def verify_quadruplet(n: int) -> Tuple[bool, List[int]]:
    """
    Verify that Q(n), Q(n+1), Q(n+2), Q(n+3) are all prime
    Returns (is_valid, [digits for each])
    """
    results = []
    for i in range(4):
        q = Q(n + i)
        digits = len(str(q))
        is_prime = is_prime_miller_rabin(q)
        results.append((is_prime, digits))
    
    all_prime = all(r[0] for r in results)
    digit_counts = [r[1] for r in results]
    
    return all_prime, digit_counts

def verify_all_quadruplets():
    """Verify all 14 Prime Quadruplets"""
    quadruplets = [
        117309848, 136584738, 218787064, 411784485, 423600750,
        523331634, 640399031, 987980498, 1163461515, 1370439187,
        1643105964, 1691581855, 1975860550, 1996430175
    ]
    
    print("Verifying the 14 Prime Quadruplets...")
    print("-" * 60)
    
    all_valid = True
    for i, n in enumerate(quadruplets, 1):
        is_valid, digits = verify_quadruplet(n)
        status = "PASS" if is_valid else "FAIL"
        print(f"  #{i:2}: n = {n:>13,} | Digits: {digits[0]} | [{status}]")
        
        if not is_valid:
            all_valid = False
    
    print("-" * 60)
    if all_valid:
        print("  [PASS] All 14 quadruplets verified!")
    else:
        print("  [FAIL] Some quadruplets failed verification")
    
    return all_valid

def main():
    print("=" * 60)
    print("  Q(n) = n^47 - (n-1)^47 Verification Suite")
    print("=" * 60)
    print()
    
    # 1. Verify Exclusion Theorem
    verify_exclusion_theorem(100_000)
    print()
    
    # 2. Verify Quadruplets (note: this is slow for large n)
    verify_all_quadruplets()
    print()
    
    print("=" * 60)
    print("  Verification Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()
