import time
import hashlib
import json
from copy import deepcopy


class ResultCache:
    """
    In-memory execution cache.

    Features

    ✓ TTL support
    ✓ Automatic expiration
    ✓ Cache statistics
    ✓ Cache invalidation
    ✓ Deep-copy protection

    Cache Key

    server + tool + arguments
    """

    #
    # Default TTL (seconds)
    #

    DEFAULT_TTL = 300

    #
    # Cache Store
    #

    _cache = {}

    _stats = {

        "hits": 0,

        "misses": 0,

        "writes": 0,

        "evictions": 0,

    }

    #
    # ------------------------------------------
    # Key Builder
    # ------------------------------------------
    #

    @classmethod
    def key(
        cls,
        server,
        tool,
        arguments,
    ):

        payload = {

            "server": server,

            "tool": tool,

            "arguments": arguments,

        }

        text = json.dumps(
            payload,
            sort_keys=True,
        )

        return hashlib.sha256(
            text.encode()
        ).hexdigest()

    #
    # ------------------------------------------
    # Read
    # ------------------------------------------
    #

    @classmethod
    def get(
        cls,
        server,
        tool,
        arguments,
    ):

        key = cls.key(

            server,

            tool,

            arguments,

        )

        item = cls._cache.get(
            key
        )

        if item is None:

            cls._stats["misses"] += 1

            return None

        #
        # Expired?
        #

        if time.time() > item["expires"]:

            cls._cache.pop(
                key,
                None,
            )

            cls._stats["evictions"] += 1

            cls._stats["misses"] += 1

            return None

        cls._stats["hits"] += 1

        return deepcopy(
            item["value"]
        )

    #
    # ------------------------------------------
    # Write
    # ------------------------------------------
    #

    @classmethod
    def put(
        cls,
        server,
        tool,
        arguments,
        result,
        ttl=None,
    ):

        ttl = ttl or cls.DEFAULT_TTL

        key = cls.key(

            server,

            tool,

            arguments,

        )

        cls._cache[key] = {

            "value": deepcopy(result),

            "created": time.time(),

            "expires": time.time() + ttl,

        }

        cls._stats["writes"] += 1

    #
    # ------------------------------------------
    # Exists
    # ------------------------------------------
    #

    @classmethod
    def contains(
        cls,
        server,
        tool,
        arguments,
    ):

        return (

            cls.get(

                server,

                tool,

                arguments,

            )

            is not None

        )

    #
    # ------------------------------------------
    # Delete
    # ------------------------------------------
    #

    @classmethod
    def delete(
        cls,
        server,
        tool,
        arguments,
    ):

        key = cls.key(

            server,

            tool,

            arguments,

        )

        if key in cls._cache:

            del cls._cache[key]

    #
    # ------------------------------------------
    # Clear
    # ------------------------------------------
    #

    @classmethod
    def clear(
        cls,
    ):

        cls._cache.clear()

    #
    # ------------------------------------------
    # Cleanup Expired
    # ------------------------------------------
    #

    @classmethod
    def cleanup(
        cls,
    ):

        now = time.time()

        expired = []

        for key, value in cls._cache.items():

            if value["expires"] < now:

                expired.append(key)

        for key in expired:

            cls._cache.pop(
                key,
                None,
            )

            cls._stats["evictions"] += 1

    #
    # ------------------------------------------
    # Statistics
    # ------------------------------------------
    #

    @classmethod
    def stats(
        cls,
    ):

        total = (

            cls._stats["hits"]

            +

            cls._stats["misses"]

        )

        hit_rate = (

            cls._stats["hits"] / total

            if total

            else 0

        )

        return {

            "entries": len(
                cls._cache
            ),

            "hits": cls._stats["hits"],

            "misses": cls._stats["misses"],

            "writes": cls._stats["writes"],

            "evictions": cls._stats["evictions"],

            "hit_rate": round(
                hit_rate,
                3,
            ),

        }

    #
    # ------------------------------------------
    # Debug
    # ------------------------------------------
    #

    @classmethod
    def dump(
        cls,
    ):

        return deepcopy(
            cls._cache
        )