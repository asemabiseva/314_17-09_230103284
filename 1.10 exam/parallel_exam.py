"""
================================================================================
CSS 314 OPENMP LAB EXAM - SUBMISSION HEADER
================================================================================
STUDENT NAME : Assem Abisheva
STUDENT ID   : 230103284

--- AUTO-GENERATED MACHINE TELEMETRY (Paste from script terminal output) ---
CPU / Processor : AMD64 Family 23 Model 104 Stepping 1, AuthenticAMD
OS Platform     : Windows 10
Detected Cores  : 12 Logical Cores

--- TASK 3: EMPIRICAL BENCHMARK TABLE (Paste from script terminal output) ---
--------------------------------------------------------------------
Threads    | Run 1     | Run 2     | Run 3     | Avg Time   | Speedup 
--------------------------------------------------------------------
1          | 3.34    s | 3.36    s | 3.33    s | 3.34    s  | 1.00x   
2          | 1.84    s | 1.97    s | 1.76    s | 1.86    s  | 1.80x   
4          | 1.27    s | 1.25    s | 1.28    s | 1.26    s  | 2.65x   
8          | 1.23    s | 1.12    s | 1.09    s | 1.15    s  | 2.91x   
--------------------------------------------------------------------

--- HARDWARE OBSERVATIONS (Answer in 1-2 sentences each) ---
1. Physical vs Logical cores on your laptop: I have 6 physical and 12 logical cores in my laptop.
2. Did 8 threads give double the speedup of 4 threads? Why or why not? 
No it doesn't speed up for 2x only slightly (1.27 and 1.23). 
It's because the higher number of threads does not guarantee higher speed, cause at the end it will exceed actual number of cores which lead to thread overhead, CPU resourse limits and at the end it does not give such remarkable results (like 2x). 
3. Did your laptop fan kick in or did later runs slow down from thermal throttling? 
The fan does not kick in immideatly and didn't run fast just normaly. 
After executing code several times speed of threads incresed but do not affect fan's work dramatically.
================================================================================
"""

import sys
import os
import time
import platform
from concurrent.futures import ProcessPoolExecutor

# ==============================================================================
# 1. STUDENT CONFIGURATION
# ==============================================================================
STUDENT_ID = 230103284  # <--- ENTER YOUR NUMERIC STUDENT ID HERE (e.g. 20210045)

if STUDENT_ID == 0:
    print("[ERROR] You must set your numeric STUDENT_ID on line 34 before running.")
    sys.exit(1)

SEED = STUDENT_ID % 1000
N_ELEMENTS = 5_000_000 + (SEED * 100)
NUM_ITEMS = 2_500 + (SEED % 50) * 10


# ==============================================================================
# TOP-LEVEL WORKERS (DO NOT REMOVE FROM MODULE LEVEL)
# ==============================================================================

def task1_worker_chunk(start, end, seed):
    local_count = 0

    for i in range(start, end):
        if ((i ^ seed) % 7) == 0:
            local_count += 1

    return local_count


def heavy_kernel(idx, seed):
    steps = int((idx / 20) ** 2) + 15
    acc = 0
    for k in range(steps):
        acc += ((idx * 31) ^ (k + seed)) % 1000
    return acc


def task2_worker_bucket(bucket_indices, seed):
    subtotal = 0
    for idx in bucket_indices:
        subtotal += heavy_kernel(idx, seed)
    return subtotal


# ==============================================================================
# TASK 1: PARALLEL REDUCTION DISPATCHER
# ==============================================================================
def solve_task1_parallel(n, seed, num_workers=4):
    chunk_size = (n + num_workers - 1) 

    chunks = []

    for w in range(num_workers):
        start = w * chunk_size
        end = min((w + 1) * chunk_size, n)

        if start < end:
            chunks.append((start, end))

    total = 0

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [
            executor.submit(task1_worker_chunk, start, end, seed)
            for start, end in chunks
        ]

        for future in futures:
            total += future.result()

    return total


# ==============================================================================
# TASK 2: LOAD BALANCING (30 MARKS)
# ==============================================================================
def solve_task2_balanced(num_items, seed, num_workers=4):

    buckets = [[] for _ in range(num_workers)]

    for i in range(num_items):
        buckets[i % num_workers].append(i)

    total = 0

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [
            executor.submit(task2_worker_bucket, b, seed)
            for b in buckets
        ]

        for f in futures:
            total += f.result()

    return total

def _run_naive_reference(num_items, seed, num_workers=4):
    chunk_size = (num_items + num_workers - 1) // num_workers
    buckets = []
    for w in range(num_workers):
        start = w * chunk_size
        end = min((w + 1) * chunk_size, num_items)
        buckets.append(list(range(start, end)))
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(task2_worker_bucket, b, seed) for b in buckets]
        return sum(f.result() for f in futures)


# ==============================================================================
# MAIN TEST & TELEMETRY HARNESS
# ==============================================================================
if __name__ == "__main__":
    print("=" * 68)
    print("MACHINE HARDWARE TELEMETRY")
    print(f"Processor : {platform.processor() or platform.machine()}")
    print(f"OS        : {platform.system()} {platform.release()}")
    print(f"CPU Count : {os.cpu_count()} Logical Cores")
    print(f"Student ID: {STUDENT_ID} (Seed: {SEED})")
    print("=" * 68)

    # 1. VERIFY TASK 1
    print("\n[Running Task 1 Verification]...")
    expected_p1 = sum(1 for i in range(N_ELEMENTS) if ((i ^ SEED) % 7) == 0)
    actual_p1 = solve_task1_parallel(N_ELEMENTS, SEED, num_workers=4)

    if actual_p1 == expected_p1:
        print(f"-> TASK 1: [PASSED] (Checksum: {actual_p1})")
    else:
        print(f"-> TASK 1: [FAILED] (Expected: {expected_p1}, Got: {actual_p1})")
        print("   Hint: Implement counting logic inside 'task1_worker_chunk'.")

    # 2. VERIFY TASK 2 LOAD BALANCING
    print("\n[Running Task 2 Load Balancing Test] (4 workers)...")
    t_start = time.perf_counter()
    res_user = solve_task2_balanced(NUM_ITEMS, SEED, num_workers=4)
    t_user = time.perf_counter() - t_start

    t_start_ref = time.perf_counter()
    res_naive = _run_naive_reference(NUM_ITEMS, SEED, num_workers=4)
    t_naive = time.perf_counter() - t_start_ref

    if res_user == res_naive:
        print(f"-> TASK 2: [PASSED] (Checksum: {res_user})")
        print(f"   Your 4-Worker Time: {t_user:.2f}s | Naive 4-Worker Time: {t_naive:.2f}s")
        if t_user < t_naive:
            speedup = t_naive / t_user
            print(f"   Optimization: {speedup:.2f}x faster than naive static allocation.")
        else:
            print("   Note: Naive static allocation detected. Switch to cyclic (i % num_workers) to improve balance.")
    else:
        print(f"-> TASK 2: [FAILED] Checksum mismatch! All items must be processed.")

    # 3. RUN TASK 3 BENCHMARK SUITE
    print("\n[Running Task 3 Benchmark Suite] (1, 2, 4, 8 threads)...")
    print("-" * 68)
    print(f"{'Threads':<10} | {'Run 1':<9} | {'Run 2':<9} | {'Run 3':<9} | {'Avg Time':<10} | {'Speedup':<8}")
    print("-" * 68)

    t1_mean = None
    for p in [1, 2, 4, 8]:
        runs = []
        for _ in range(3):
            t0 = time.perf_counter()
            _ = solve_task2_balanced(NUM_ITEMS, SEED, num_workers=p)
            runs.append(time.perf_counter() - t0)
        avg_t = sum(runs) / len(runs)
        if p == 1:
            t1_mean = avg_t
            sp_str = "1.00x"
        else:
            sp = (t1_mean / avg_t) if avg_t > 0 else 1.0
            sp_str = f"{sp:.2f}x"
        print(f"{p:<10} | {runs[0]:<8.2f}s | {runs[1]:<8.2f}s | {runs[2]:<8.2f}s | {avg_t:<8.2f}s  | {sp_str:<8}")

    print("-" * 68)
    print("\n[EXAM COMPLETE] Copy telemetry and benchmark rows into top docstring header, then submit to Moodle.")
