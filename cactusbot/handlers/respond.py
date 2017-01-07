"""Handle bot responses."""

from ..handler import Handler


class ResponseHandler(Handler):
    """Handle bot responses."""

    def __init__(self, username):
        super().__init__()

        self.username = username

    async def on_message(self, packet):
        """Stop iteration if the bot is responding to itself."""
        return self._check_packet(packet, self.username)

    async def on_join(self, packet):
        """Stop iteration if the bot is the user that joined."""
        return self._check_packet(packet, self.username)

    async def on_leave(self, packet):
        """Stop iteration if the bot is the user that left."""
        return self._check_packet(packet, self.username)

    @staticmethod
    def _check_packet(packet, username):
        if packet.user.lower() == username.lower():
            return StopIteration
