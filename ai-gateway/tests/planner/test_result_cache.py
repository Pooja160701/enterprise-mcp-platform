import json

from app.planner.result_cache import ResultCache


server = "github"

tool = "list_repositories"

arguments = {}


result = [
    {
        "name": "enterprise-mcp-platform",
    }
]


print("\nInitial Cache Stats\n")

print(
    json.dumps(
        ResultCache.stats(),
        indent=2,
    )
)


print("\nWriting Cache\n")

ResultCache.put(

    server=server,

    tool=tool,

    arguments=arguments,

    result=result,

)


print("\nReading Cache\n")

cached = ResultCache.get(

    server=server,

    tool=tool,

    arguments=arguments,

)

print(
    json.dumps(
        cached,
        indent=2,
    )
)


print("\nCache Statistics\n")

print(
    json.dumps(
        ResultCache.stats(),
        indent=2,
    )
)


print("\nClearing Cache\n")

ResultCache.clear()


print(
    json.dumps(
        ResultCache.stats(),
        indent=2,
    )
)