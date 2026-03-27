import math
import time
import argparse

def pi_gauss_legendre(iterations=5):
    a = 1.0
    b = 1.0 / math.sqrt(2.0)
    t = 0.25
    p = 1.0
    for _ in range(iterations):
        an = (a + b) / 2.0
        b = math.sqrt(a * b)
        t -= p * (a - an)**2
        a = an
        p *= 2.0
    return (a + b)**2 / (4.0 * t)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", "-i", type=int, default=5)
    args = parser.parse_args()

    start = time.perf_counter()
    pi = pi_gauss_legendre(args.iterations)
    end = time.perf_counter()

    elapsed = end - start
    ms = elapsed * 1000.0

    print(f"{pi:.15f}")
    print(f"Elapsed: {elapsed:.6f} s ({ms:.3f} ms)")
