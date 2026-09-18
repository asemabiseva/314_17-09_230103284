import java.util.Random;

public class Part3 {

    static final long TOTAL_POINTS = 50_000_000;

    static class Worker extends Thread {
        private final long points;
        private long localHits = 0;

        Worker(long points) {
            this.points = points;
        }

        @Override
        public void run() {
            Random random = new Random();

            for (long i = 0; i < points; i++) {
                double x = random.nextDouble();
                double y = random.nextDouble();

                if (x * x + y * y <= 1.0) {
                    localHits++;
                }
            }
        }

        public long getLocalHits() {
            return localHits;
        }
    }

    static void runExperiment(int numThreads) throws InterruptedException {

        Worker[] threads = new Worker[numThreads];

        long pointsPerThread = TOTAL_POINTS / numThreads;

        long start = System.nanoTime();

        // Start threads
        for (int i = 0; i < numThreads; i++) {
            threads[i] = new Worker(pointsPerThread);
            threads[i].start();
        }

        // Wait for threads
        for (int i = 0; i < numThreads; i++) {
            threads[i].join();
        }

        // Reduction: add local results together
        long totalHits = 0;

        for (int i = 0; i < numThreads; i++) {
            totalHits += threads[i].getLocalHits();
        }

        long end = System.nanoTime();

        double pi = 4.0 * totalHits / TOTAL_POINTS;
        double timeMs = (end - start) / 1_000_000.0;

        System.out.println(
            "Threads: " + numThreads +
            " | Pi: " + pi +
            " | Time: " + timeMs + " ms"
        );
    }

    public static void main(String[] args) throws InterruptedException {

        int[] threadCounts = {1, 2, 4, 8, 16, 32};

        for (int threads : threadCounts) {
            runExperiment(threads);
        }
    }
}