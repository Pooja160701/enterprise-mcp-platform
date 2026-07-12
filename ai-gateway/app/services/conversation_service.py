import uuid


class ConversationService:

    @staticmethod
    def create():

        return {
            "id": str(uuid.uuid4()),
            "message_id": str(uuid.uuid4())
        }