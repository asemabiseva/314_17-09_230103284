public class CollatzSeq2 {

    static final long MOD = 1_000_000_007L;
    static final long N = 10_284_000L;

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

    static void run() {

        long maxSteps = 0;
        long checksum = 0;

        for (long i = 1; i <= N; i++) {

            long steps = collatzSteps(i);

            if (steps > maxSteps) {
                maxSteps = steps;
            }

            checksum = (checksum + steps) % MOD;
        }

        // Prevent JVM from optimizing away the calculations
        System.out.println(
                "Max stopping time: " + maxSteps +
                " | Checksum: " + checksum
        );
    }

    public static void main(String[] args) {

        System.out.println("N = " + N);
        System.out.println();

        // =========================
        // RUN 1 - WARMUP
        // =========================

        System.out.println("Run 1 (Warmup)...");

        run();

        System.out.println("Run 1 discarded.");
        System.out.println();

        // =========================
        // RUN 2
        // =========================

        System.out.println("Run 2:");

        long start2 = System.nanoTime();

        run();

        long end2 = System.nanoTime();

        double time2 =
                (end2 - start2) / 1_000_000.0;

        System.out.printf(
                "Run 2 time: %.4f ms%n",
                time2
        );

        System.out.println();

        // =========================
        // RUN 3
        // =========================

        System.out.println("Run 3:");

        long start3 = System.nanoTime();

        run();

        long end3 = System.nanoTime();

        double time3 =
                (end3 - start3) / 1_000_000.0;

        System.out.printf(
                "Run 3 time: %.4f ms%n",
                time3
        );

        System.out.println();

        // =========================
        // FINAL RESULT
        // =========================

        double T_seq = (time2 + time3) / 2.0;

        System.out.printf(
                "T_seq = (Run 2 + Run 3) / 2 = %.4f ms%n",
                T_seq
        );
    }
}