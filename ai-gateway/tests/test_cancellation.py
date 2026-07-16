import json
import time

from app.parallel.cancellation import Cancellation


def long_task():

    time.sleep(5)

    return "Finished"


print("\n=== Cancellation Test ===\n")

#
# Initialize
#

print("Initializing Cancellation\n")

cancel = Cancellation()

print(
    json.dumps(
        cancel.statistics(),
        indent=2,
    )
)

#
# Submit Tasks
#

print("\nSubmitting Tasks\n")

task1 = cancel.submit(long_task)
task2 = cancel.submit(long_task)
task3 = cancel.submit(long_task)

print(task1)
print(task2)
print(task3)

print(
    json.dumps(
        cancel.statistics(),
        indent=2,
    )
)

#
# Cancel One Task
#

print("\nCancelling First Task\n")

print(
    cancel.cancel(task1)
)

#
# Wait
#

print("\nWaiting\n")

cancel.wait()

#
# Results
#

print("\nResults\n")

print(
    json.dumps(
        cancel.results(),
        indent=2,
    )
)

#
# Completed
#

print("\nCompleted\n")

print(
    cancel.done()
)

#
# Statistics
#

print("\nStatistics\n")

print(
    json.dumps(
        cancel.statistics(),
        indent=2,
    )
)

#
# Cleanup
#

print("\nCleanup\n")

cancel.clear()

print(
    json.dumps(
        cancel.statistics(),
        indent=2,
    )
)

print("\nCancellation Test Passed ✓")