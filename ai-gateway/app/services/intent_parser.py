import json


class IntentParser:

    @staticmethod
    def parse(response: str):

        try:

            servers = json.loads(response)

        except Exception:

            return ["filesystem"]

        if not isinstance(servers, list):

            return ["filesystem"]

        return servers