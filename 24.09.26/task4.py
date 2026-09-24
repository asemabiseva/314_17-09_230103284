import numpy as np
import multiprocessing as mp
import time

N = 10_284_000
MOD = 1_000_000_007


def collatz_chunk(args):
    start, end = args

    max_steps = 0
    checksum = 0

    for n in range(start, end):
        steps = 0
        x = n

        while x > 1:
            if x % 2 == 0:
                x //= 2
            else:
                x = 3 * x + 1

            steps += 1

        if steps > max_steps:
            max_steps = steps

        checksum += steps

    return max_steps, checksum


def run_parallel(k):

    # Делим диапазон на k частей
    chunk_size = N // k
    ranges = []

    for i in range(k):
        start = i * chunk_size + 1

        if i == k - 1:
            end = N + 1
        else:
            end = (i + 1) * chunk_size + 1

        ranges.append((start, end))

    start_time = time.perf_counter()

    with mp.Pool(processes=k) as pool:
        results = pool.map(collatz_chunk, ranges)

    end_time = time.perf_counter()

    max_steps = max(result[0] for result in results)
    checksum = sum(result[1] for result in results) % MOD

    return end_time - start_time, max_steps, checksum


if __name__ == "__main__":

    print("N =", N)
    print("CPU cores:", mp.cpu_count())

    thread_counts = [1, 2, 4, 8, 12]

    results = {}

    for k in thread_counts:

        print(f"\nStarting k = {k}...", flush=True)

        # Run 1 — Cold
        t1, max1, check1 = run_parallel(k)

        # Run 2
        t2, max2, check2 = run_parallel(k)

        # Run 3
        t3, max3, check3 = run_parallel(k)

        avg = (t2 + t3) / 2

        results[k] = (t1, t2, t3, avg)

        print(
            f"k={k} | "
            f"Run1={t1:.4f}s | "
            f"Run2={t2:.4f}s | "
            f"Run3={t3:.4f}s | "
            f"Avg={avg:.4f}s | "
            f"Max={max2} | "
            f"Checksum={check2}",
            flush=True
        )