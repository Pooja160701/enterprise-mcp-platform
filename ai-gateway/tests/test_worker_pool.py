import json
import time

from app.parallel.worker_pool import WorkerPool


print("\n=== Worker Pool Test ===\n")


# -------------------------------------------------
# Sample Tasks
# -------------------------------------------------

def square(x):
    time.sleep(0.2)
    return x * x


def add(a, b):
    time.sleep(0.1)
    return a + b


def greeting(name):
    return f"Hello {name}"


# -------------------------------------------------
# Initialize
# -------------------------------------------------

print("Initializing Worker Pool\n")

WorkerPool.initialize(max_workers=4)

print(
    json.dumps(
        WorkerPool.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Submit Tasks
# -------------------------------------------------

print("\nSubmitting Tasks\n")

task1 = WorkerPool.submit(
    square,
    5,
)

task2 = WorkerPool.submit(
    add,
    10,
    20,
)

task3 = WorkerPool.submit(
    greeting,
    "Pooja",
)

print("Task IDs")

print(task1)
print(task2)
print(task3)

# -------------------------------------------------
# Results
# -------------------------------------------------

print("\nResults\n")

print(
    WorkerPool.result(task1)
)

print(
    WorkerPool.result(task2)
)

print(
    WorkerPool.result(task3)
)

# -------------------------------------------------
# Done
# -------------------------------------------------

print("\nTask Status\n")

print(
    WorkerPool.done(task1)
)

print(
    WorkerPool.done(task2)
)

print(
    WorkerPool.done(task3)
)

# -------------------------------------------------
# Wait
# -------------------------------------------------

print("\nWaiting for All Tasks\n")

WorkerPool.wait()

print(
    json.dumps(
        WorkerPool.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Active Task IDs
# -------------------------------------------------

print("\nTask IDs\n")

print(

    json.dumps(

        WorkerPool.task_ids(),

        indent=2,

    )

)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

WorkerPool.cleanup()

print(

    json.dumps(

        WorkerPool.statistics(),

        indent=2,

    )

)

# -------------------------------------------------
# Cancel Example
# -------------------------------------------------

print("\nCancel Completed Task\n")

print(

    WorkerPool.cancel(task1)

)

# -------------------------------------------------
# Shutdown
# -------------------------------------------------

print("\nShutdown\n")

WorkerPool.shutdown()

print(

    "Worker Pool Shutdown Successfully"

)

print("\nWorker Pool Test Passed ✓")