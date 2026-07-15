from app.services.argument_resolver import ArgumentResolver

results = [
    {
        "id": 1,
        "result": {
            "name": "enterprise-mcp-platform",
            "owner": "Pooja160701",
        },
    }
]

arguments = {
    "repository": "$1.name",
    "owner": "$1.owner",
}

print(
    ArgumentResolver.resolve(
        arguments,
        results,
    )
)