import json
import time

from app.parallel.parallel_group import ParallelGroup


print("\n=== Parallel Group Test ===\n")


# -------------------------------------------------
# Sample Tasks
# -------------------------------------------------

def square(x):
    time.sleep(1)
    return x * x


def multiply(a, b):
    time.sleep(1)
    return a * b


def greet(name):
    time.sleep(1)
    return f"Hello {name}"


# -------------------------------------------------
# Create Group
# -------------------------------------------------

print("Creating Parallel Group\n")

group = ParallelGroup()

print(
    json.dumps(
        group.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Add Tasks
# -------------------------------------------------

print("\nAdding Tasks\n")

group.add(
    square,
    5,
)

group.add(
    multiply,
    6,
    7,
)

group.add(
    greet,
    "Pooja",
)

print(
    json.dumps(
        group.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Execute
# -------------------------------------------------

print("\nExecuting Group\n")

results = group.run()

print(
    json.dumps(
        results,
        indent=2,
    )
)

# -------------------------------------------------
# Wait
# -------------------------------------------------

print("\nWaiting\n")

group.wait()

# -------------------------------------------------
# Results
# -------------------------------------------------

print("\nResults\n")

print(
    json.dumps(
        group.results(),
        indent=2,
    )
)

# -------------------------------------------------
# Status
# -------------------------------------------------

print("\nCompleted\n")

print(group.done())

# -------------------------------------------------
# Statistics
# -------------------------------------------------

print("\nStatistics\n")

print(
    json.dumps(
        group.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

group.clear()

print(
    json.dumps(
        group.statistics(),
        indent=2,
    )
)

print("\nParallel Group Test Passed")