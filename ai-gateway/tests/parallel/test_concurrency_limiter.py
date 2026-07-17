import json
import time

from app.parallel.concurrency_limiter import ConcurrencyLimiter


def slow_square(x):
    time.sleep(1)
    return x * x


print("\n=== Concurrency Limiter Test ===\n")

#
# Initialize
#

print("Initializing Limiter\n")

limiter = ConcurrencyLimiter(max_concurrent=2)

print(
    json.dumps(
        limiter.statistics(),
        indent=2,
    )
)

#
# Add Tasks
#

print("\nSubmitting Tasks\n")

limiter.submit(slow_square, 5)
limiter.submit(slow_square, 6)
limiter.submit(slow_square, 7)

print(
    json.dumps(
        limiter.statistics(),
        indent=2,
    )
)

#
# Execute
#

print("\nRunning\n")

limiter.run()

#
# Wait
#

print("\nWaiting\n")

limiter.wait()

#
# Results
#

print("\nResults\n")

print(
    json.dumps(
        limiter.results(),
        indent=2,
    )
)

#
# Completed
#

print("\nCompleted\n")

print(
    limiter.done()
)

#
# Statistics
#

print("\nStatistics\n")

print(
    json.dumps(
        limiter.statistics(),
        indent=2,
    )
)

#
# Cleanup
#

print("\nCleanup\n")

limiter.clear()

print(
    json.dumps(
        limiter.statistics(),
        indent=2,
    )
)

print("\nConcurrency Limiter Test Passed")