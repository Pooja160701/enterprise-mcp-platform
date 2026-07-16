import json
import threading
import time

from app.approval.pause_resume import PauseResume


print("\n=== Pause / Resume Test ===\n")

# -------------------------------------------------
# Initialize
# -------------------------------------------------

controller = PauseResume()

print("Initializing Pause / Resume\n")

print(
    json.dumps(
        controller.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Pause
# -------------------------------------------------

print("\nPausing Execution\n")

print(
    controller.pause()
)

print("\nPaused\n")

print(
    controller.paused()
)

print("\nStatistics\n")

print(
    json.dumps(
        controller.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Wait / Resume
# -------------------------------------------------

print("\nTesting Wait / Resume\n")


def worker():

    print("Worker waiting...")

    controller.wait()

    print("Worker resumed.")


thread = threading.Thread(target=worker)

thread.start()

time.sleep(1)

print("\nResuming Execution\n")

print(
    controller.resume()
)

thread.join()

print("\nRunning\n")

print(
    controller.running()
)

print("\nStatistics\n")

print(
    json.dumps(
        controller.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Stop
# -------------------------------------------------

print("\nStopping Controller\n")

controller.stop()

print("\nStopped\n")

print(
    controller.stopped()
)

print("\nStatistics\n")

print(
    json.dumps(
        controller.statistics(),
        indent=2,
    )
)

# -------------------------------------------------
# Export
# -------------------------------------------------

print("\nExport\n")

print(
    json.dumps(
        controller.export(),
        indent=2,
    )
)

# -------------------------------------------------
# Reset
# -------------------------------------------------

print("\nReset\n")

controller.reset()

print(
    json.dumps(
        controller.statistics(),
        indent=2,
    )
)

print("\nPause / Resume Test Passed ✓")