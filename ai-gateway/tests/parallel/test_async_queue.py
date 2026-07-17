import json
import time

from app.parallel.async_queue import AsyncQueue


print("\n=== Async Queue Test ===\n")


# -------------------------------------------------
# Sample Tasks
# -------------------------------------------------

def square(x):
    time.sleep(1)
    return x * x


def add(a, b):
    time.sleep(1)
    return a + b


def greet(name):
    time.sleep(1)
    return f"Hello {name}"


# -------------------------------------------------
# Initialize
# -------------------------------------------------

print("Initializing Queue\n")

queue = AsyncQueue()

print(
    json.dumps(
        queue.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Enqueue
# -------------------------------------------------

print("\nAdding Tasks\n")

queue.enqueue(
    square,
    5,
)

queue.enqueue(
    add,
    10,
    20,
)

queue.enqueue(
    greet,
    "Pooja",
)

print(
    json.dumps(
        queue.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Execute
# -------------------------------------------------

print("\nProcessing Queue\n")

queue.run()

# -------------------------------------------------
# Wait
# -------------------------------------------------

print("\nWaiting\n")

queue.wait()

# -------------------------------------------------
# Results
# -------------------------------------------------

print("\nResults\n")

print(
    json.dumps(
        queue.results(),
        indent=2,
    )
)

# -------------------------------------------------
# Done
# -------------------------------------------------

print("\nCompleted\n")

print(queue.done())

# -------------------------------------------------
# Statistics
# -------------------------------------------------

print("\nStatistics\n")

print(
    json.dumps(
        queue.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

queue.clear()

print(
    json.dumps(
        queue.statistics(),
        indent=2,
    )
)

print("\nAsync Queue Test Passed")