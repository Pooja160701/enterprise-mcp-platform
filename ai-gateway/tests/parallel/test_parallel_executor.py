import json
import time

from app.parallel.parallel_executor import ParallelExecutor


def add(a, b):
    time.sleep(1)
    return a + b


def multiply(a, b):
    time.sleep(1)
    return a * b


def greet(name):
    time.sleep(1)
    return f"Hello {name}"


print("\n=== Parallel Executor Test ===\n")

#
# Initialize
#

print("Initializing Parallel Executor\n")

executor = ParallelExecutor()

print(
    json.dumps(
        executor.statistics(),
        indent=2,
    )
)

#
# Add Tasks
#

print("\nSubmitting Tasks\n")

executor.submit(add, 10, 15)
executor.submit(multiply, 6, 7)
executor.submit(greet, "Pooja")

print(
    json.dumps(
        executor.statistics(),
        indent=2,
    )
)

#
# Execute
#

print("\nExecuting\n")

executor.run()

#
# Wait
#

print("\nWaiting\n")

executor.wait()

#
# Results
#

print("\nResults\n")

print(
    json.dumps(
        executor.results(),
        indent=2,
    )
)

#
# Completed
#

print("\nCompleted\n")

print(
    executor.done()
)

#
# Statistics
#

print("\nStatistics\n")

print(
    json.dumps(
        executor.statistics(),
        indent=2,
    )
)

#
# Cleanup
#

print("\nCleanup\n")

executor.clear()

print(
    json.dumps(
        executor.statistics(),
        indent=2,
    )
)

print("\nParallel Executor Test Passed")