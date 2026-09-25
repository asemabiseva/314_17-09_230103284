import numpy as np
import time
from numba import njit, prange, set_num_threads

N_STEPS = 100_000_000


# Variant A: Naive Race Condition
@njit(parallel=True)
def calc_pi_naive(num_steps):
    step = 1.0 / num_steps

    # Shared variable stored in an array
    total_sum = np.zeros(1)

    for i in prange(num_steps):
        x = (i + 0.5) * step

        # UNSAFE shared update — intentional race condition
        total_sum[0] += 4.0 / (1.0 + x * x)

    return total_sum[0] * step


if __name__ == "__main__":

    # Warm-up JIT compilation
    calc_pi_naive(1000)

    thread_counts = [1, 2, 4, 8]

    print("===== VARIANT A: NAIVE RACE =====")

    for p in thread_counts:

        # Set number of threads
        set_num_threads(p)

        # Start timing
        start = time.perf_counter()

        # Calculate Pi
        pi_value = calc_pi_naive(N_STEPS)

        # Stop timing
        end = time.perf_counter()

        # Calculate absolute error
        error = abs(pi_value - np.pi)

        print(
            f"P = {p} | "
            f"Pi = {pi_value:.12f} | "
            f"Error = {error:.2e} | "
            f"Time = {end - start:.4f}s"
        )