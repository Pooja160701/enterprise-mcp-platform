import json
import time

from app.parallel.task_scheduler import TaskScheduler


print("\n=== Task Scheduler Test ===\n")


# -------------------------------------------------
# Sample Tasks
# -------------------------------------------------

def hello(name):
    print(f"Hello {name}")
    return f"Hello {name}"


def add(a, b):
    return a + b


def slow():
    time.sleep(2)
    return "done"


# -------------------------------------------------
# Initialize
# -------------------------------------------------

print("Initializing Scheduler\n")

TaskScheduler.initialize()

print(
    json.dumps(
        TaskScheduler.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Immediate Task
# -------------------------------------------------

print("\nScheduling Immediate Task\n")

task1 = TaskScheduler.submit(
    hello,
    "Pooja",
)

print(task1)

# -------------------------------------------------
# Delayed Task
# -------------------------------------------------

print("\nScheduling Delayed Task (2 sec)\n")

task2 = TaskScheduler.schedule(
    delay=2,
    func=add,
    a=10,
    b=20,
)

print(task2)

# -------------------------------------------------
# Another Delayed Task
# -------------------------------------------------

print("\nScheduling Another Task\n")

task3 = TaskScheduler.schedule(
    delay=1,
    func=hello,
    name="Enterprise MCP",
)

print(task3)

# -------------------------------------------------
# Statistics
# -------------------------------------------------

print("\nScheduler Statistics\n")

print(
    json.dumps(
        TaskScheduler.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Wait
# -------------------------------------------------

print("\nWaiting...\n")

TaskScheduler.wait()

# -------------------------------------------------
# Results
# -------------------------------------------------

print("\nResults\n")

print(TaskScheduler.result(task1))
print(TaskScheduler.result(task2))
print(TaskScheduler.result(task3))

# -------------------------------------------------
# Completed
# -------------------------------------------------

print("\nCompleted\n")

print(TaskScheduler.done(task1))
print(TaskScheduler.done(task2))
print(TaskScheduler.done(task3))

# -------------------------------------------------
# Task IDs
# -------------------------------------------------

print("\nTask IDs\n")

print(
    json.dumps(
        TaskScheduler.task_ids(),
        indent=2,
    )
)

# -------------------------------------------------
# Cancel Finished Task
# -------------------------------------------------

print("\nCancel Finished Task\n")

print(
    TaskScheduler.cancel(task1)
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

TaskScheduler.cleanup()

print(
    json.dumps(
        TaskScheduler.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Shutdown
# -------------------------------------------------

print("\nShutdown\n")

TaskScheduler.shutdown()

print("Scheduler Shutdown Successfully")

print("\nTask Scheduler Test Passed ✓")