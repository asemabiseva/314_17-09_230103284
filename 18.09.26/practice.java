import java.util.Random;

public class practice {

    static long totalHits = 0;

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
                    totalHits++;   // DATA RACE
                }
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {

        int numThreads = 4;
        long totalPoints = 50_000_000;
        long pointsPerThread = totalPoints / numThreads;

        totalHits = 0;

        Worker[] threads = new Worker[numThreads];

        long start = System.currentTimeMillis();

        for (int i = 0; i < numThreads; i++) {
            threads[i] = new Worker(pointsPerThread);
            threads[i].start();
        }

        for (int i = 0; i < numThreads; i++) {
            threads[i].join();
        }

        long end = System.currentTimeMillis();

        double pi = 4.0 * totalHits / totalPoints;

        System.out.println("Total hits: " + totalHits);
        System.out.println("Total points: " + totalPoints);
        System.out.println("Pi ≈ " + pi);
        System.out.println("Time: " + (end - start) + " ms");
    }
}