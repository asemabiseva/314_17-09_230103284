public class CollatzSeq {

    static final long MOD = 1_000_000_007L;

    // Collatz Stopping Time
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

    public static void main(String[] args) {

        // N = 10,000,000 + (284 * 1,000)
        long N = 10_284_000L;

        long maxSteps = 0;
        long checksum = 0;

        // Start timer
        long startTime = System.nanoTime();

        // Sequential loop: i = 1 ... N
        for (long i = 1; i <= N; i++) {

            long steps = collatzSteps(i);

            // Find maximum stopping time
            if (steps > maxSteps) {
                maxSteps = steps;
            }

            // Anti-cheat checksum
            checksum = (checksum + steps) % MOD;
        }

        // Stop timer
        long endTime = System.nanoTime();

        double timeMs = (endTime - startTime) / 1_000_000.0;

        System.out.println("N: " + N);
        System.out.println("Max stopping time: " + maxSteps);
        System.out.println("Checksum: " + checksum);
        System.out.printf("Time: %.4f ms%n", timeMs);
    }
}