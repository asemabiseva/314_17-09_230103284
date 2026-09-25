from concurrent.futures import ThreadPoolExecutor
import threading
import time
import math


def worker_task(thread_id: int, team_size: int):
    native_tid = threading.get_native_id()

    # Artificial CPU workload:
    # compute 10,000,000 floating-point square roots
    result = 0.0

    for i in range(10_000_000):
        result += math.sqrt(i)

    print(
        f"Thread {thread_id} of {team_size} "
        f"| Native OS TID: {native_tid} "
        f"| Result: {result:.2f}"
    )


def run_team(num_threads: int):
    print(f"\n--- Running {num_threads} threads ---")

    start_time = time.perf_counter()

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [
            executor.submit(worker_task, tid, num_threads)
            for tid in range(num_threads)
        ]

        # Wait for all threads to finish
        for f in futures:
            f.result()

    end_time = time.perf_counter()

    elapsed = end_time - start_time

    print(f"Threads: {num_threads} | Time: {elapsed:.3f} seconds")


if __name__ == "__main__":

    thread_counts = [1, 2, 4, 8, 16, 32, 64]

    for p in thread_counts:
        run_team(p)