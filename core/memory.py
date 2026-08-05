"""
memory.py
In-memory conversation history for a single chat session.
Nothing is written to disk — history is lost when the session ends
or the page is refreshed.
"""


class ConversationMemory:
    """Holds a conversation's messages in memory for the lifetime of a session."""

    def __init__(self):
        self.messages: list[dict[str, str]] = []

    def add_message(self, role: str, content: str):
        """Add a message to the history."""
        self.messages.append({"role": role, "content": content})

    def get_history(self) -> list[dict[str, str]]:
        """Return the full conversation history."""
        return self.messages

    def get_recent(self, n: int = 6) -> list[dict[str, str]]:
        """Return the last n messages for context window management."""
        return self.messages[-n:]

    def clear(self):
        """Wipe the conversation history."""
        self.messages = []

    def is_empty(self) -> bool:
        return len(self.messages) == 0