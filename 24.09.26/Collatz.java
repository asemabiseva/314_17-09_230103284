import java.util.concurrent.*;

public class Collatz {

    // Calculate Collatz stopping time
    static long collatzSteps(long n) {
        long steps = 0;

        while (n > 1) {
            if ((n & 1) == 0) {
                n >>= 1;
            } else {
                n = 3 * n + 1;
            }
            steps++;
        }

        return steps;
    }

    // Worker for a range of numbers
    static class Worker implements Callable<Long> {

        private final long start;
        private final long end;

        Worker(long start, long end) {
            this.start = start;
            this.end = end;
        }

        @Override
        public Long call() {

            long maxSteps = 0;

            for (long n = start; n <= end; n++) {

                long steps = collatzSteps(n);

                if (steps > maxSteps) {
                    maxSteps = steps;
                }
            }

            return maxSteps;
        }
    }

    public static void main(String[] args) throws Exception {

        // N = 10,000,000 + (284 * 1,000)
        long N = 10_284_000;

        // Number of threads to test
        int[] threadCounts = {1, 2, 4, 8, 16};

        for (int threads : threadCounts) {

            ExecutorService executor =
                    Executors.newFixedThreadPool(threads);

            long chunk = N / threads;

            Future<Long>[] results = new Future[threads];

            long startTime = System.nanoTime();

            // Divide the range between threads
            for (int i = 0; i < threads; i++) {

                long start = i * chunk + 1;

                long end;

                if (i == threads - 1) {
                    end = N;
                } else {
                    end = (i + 1) * chunk;
                }

                results[i] = executor.submit(
                        new Worker(start, end)
                );
            }

            // Find maximum stopping time
            long maxSteps = 0;

            for (int i = 0; i < threads; i++) {

                long threadMax = results[i].get();

                if (threadMax > maxSteps) {
                    maxSteps = threadMax;
                }
            }

            long endTime = System.nanoTime();

            executor.shutdown();

            double timeMs =
                    (endTime - startTime) / 1_000_000.0;

            System.out.printf(
                    "Threads: %d | Max stopping time: %d | Time: %.4f ms%n",
                    threads,
                    maxSteps,
                    timeMs
            );
        }
    }
}