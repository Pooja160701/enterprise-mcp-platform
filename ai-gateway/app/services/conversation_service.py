import uuid
from datetime import datetime, UTC


class ConversationService:

    @staticmethod
    def create():

        now = datetime.now(UTC).isoformat()

        return {
            "id": str(uuid.uuid4()),
            "message_id": str(uuid.uuid4()),
            "created_at": now
        }