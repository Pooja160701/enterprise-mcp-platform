import json

from app.observability.structured_logger import StructuredLogger


def pretty(data):
    print(json.dumps(data, indent=2))


print("\n=== Structured Logger Test ===\n")

# -------------------------------------------------
# Initialize
# -------------------------------------------------

print("Initializing Structured Logger\n")

logger = StructuredLogger()

pretty(
    logger.statistics()
)

# -------------------------------------------------
# Correlation ID
# -------------------------------------------------

print("\nSetting Correlation ID\n")

cid = logger.set_correlation_id(
    "CORR-12345"
)

print(cid)

# -------------------------------------------------
# INFO
# -------------------------------------------------

print("\nLogging INFO\n")

logger.info(
    "Application started.",
    service="api-gateway",
    component="startup",
)

pretty(
    logger.latest()
)

# -------------------------------------------------
# DEBUG
# -------------------------------------------------

print("\nLogging DEBUG\n")

logger.debug(
    "Loading configuration.",
    service="config",
    component="loader",
    metadata={
        "file": "config.yaml"
    },
)

# -------------------------------------------------
# WARNING
# -------------------------------------------------

print("\nLogging WARNING\n")

logger.warning(
    "High memory usage detected.",
    service="monitoring",
    component="memory",
    metadata={
        "usage": "82%"
    },
)

# -------------------------------------------------
# ERROR
# -------------------------------------------------

print("\nLogging ERROR\n")

logger.error(
    "Database connection failed.",
    service="database",
    component="postgres",
    metadata={
        "host": "localhost",
        "port": 5432,
    },
)

# -------------------------------------------------
# CRITICAL
# -------------------------------------------------

print("\nLogging CRITICAL\n")

logger.critical(
    "System shutdown imminent.",
    service="system",
    component="kernel",
)

# -------------------------------------------------
# Statistics
# -------------------------------------------------

print("\nStatistics\n")

pretty(
    logger.statistics()
)

# -------------------------------------------------
# Latest Log
# -------------------------------------------------

print("\nLatest Log\n")

pretty(
    logger.latest()
)

# -------------------------------------------------
# Search by Level
# -------------------------------------------------

print("\nERROR Logs\n")

pretty(
    logger.by_level(
        StructuredLogger.ERROR
    )
)

# -------------------------------------------------
# Search by Service
# -------------------------------------------------

print("\nDatabase Logs\n")

pretty(
    logger.by_service(
        "database"
    )
)

# -------------------------------------------------
# Search Keyword
# -------------------------------------------------

print("\nSearch: database\n")

pretty(
    logger.search(
        "database"
    )
)

# -------------------------------------------------
# All Logs
# -------------------------------------------------

print("\nAll Logs\n")

pretty(
    logger.logs()
)

# -------------------------------------------------
# JSON Export
# -------------------------------------------------

print("\nJSON Export\n")

print(
    logger.to_json()
)

# -------------------------------------------------
# Export
# -------------------------------------------------

print("\nExport\n")

pretty(
    logger.export()
)

# -------------------------------------------------
# Cleanup
# -------------------------------------------------

print("\nCleanup\n")

logger.clear()

pretty(
    logger.statistics()
)

print("\nStructured Logger Test Passed")