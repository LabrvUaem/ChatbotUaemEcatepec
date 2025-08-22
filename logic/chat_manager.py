class ChatManager:
    def __init__(self):
        self.history = []

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})
        if len(self.history) > 6:
            self.history = self.history[-6:]

    def get_context(self):
        return self.history.copy()

chat_manager = ChatManager()