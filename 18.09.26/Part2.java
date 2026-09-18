import java.util.Random;
import java.util.concurrent.atomic.AtomicLong;

public class Part2 {

    static final long TOTAL_POINTS = 50_000_000;
    static AtomicLong totalHits = new AtomicLong(0);

    static class Worker extends Thread {
        private final long points;

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
                    totalHits.incrementAndGet();
                }
            }
        }
    }

    // 4 threads
    static void runMultiThreaded() throws InterruptedException {
        totalHits.set(0);

        long pointsPerThread = TOTAL_POINTS / 4;
        Worker[] threads = new Worker[4];

        long start = System.nanoTime();

        for (int i = 0; i < 4; i++) {
            threads[i] = new Worker(pointsPerThread);
            threads[i].start();
        }

        for (int i = 0; i < 4; i++) {
            threads[i].join();
        }

        long end = System.nanoTime();

        double pi = 4.0 * totalHits.get() / TOTAL_POINTS;

        System.out.println("4 Threads + AtomicLong");
        System.out.println("Pi = " + pi);
        System.out.println("Time = " + (end - start) / 1_000_000.0 + " ms");
    }

    // Single thread
    static void runSingleThreaded() {
        Random random = new Random();
        long hits = 0;

        long start = System.nanoTime();

        for (long i = 0; i < TOTAL_POINTS; i++) {
            double x = random.nextDouble();
            double y = random.nextDouble();

            if (x * x + y * y <= 1.0) {
                hits++;
            }
        }

        long end = System.nanoTime();

        double pi = 4.0 * hits / TOTAL_POINTS;

        System.out.println("Single Thread");
        System.out.println("Pi = " + pi);
        System.out.println("Time = " + (end - start) / 1_000_000.0 + " ms");
    }

    public static void main(String[] args) throws InterruptedException {
        runSingleThreaded();
        runMultiThreaded();
    }
}