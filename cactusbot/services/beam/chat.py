"""Interact with Beam chat."""


import itertools
import json
import logging

from .. import WebSocket


class BeamChat(WebSocket):
    """Interact with Beam chat."""

    def __init__(self, channel, *endpoints):
        super().__init__(*endpoints)

        self.logger = logging.getLogger(__name__)

        assert isinstance(channel, int), "Channel ID must be an integer."
        self.channel = channel

        self._packet_counter = itertools.count()

    async def send(self, *args, max_length=360, **kwargs):
        """Send a packet."""

        # TODO: lock before auth

        packet = {
            "type": "method",
            "method": "msg",
            "arguments": args,
            "id": kwargs.get("id") or self._packet_id
        }

        packet.update(kwargs)

        if packet["method"] == "msg":
            for message in packet.copy()["arguments"]:
                for index in range(0, len(message), max_length):
                    packet["arguments"] = (message[index:index + max_length],)
                    await super().send(json.dumps(packet))
        else:
            await super().send(json.dumps(packet))

    async def initialize(self, *auth):
        """Send an authentication packet."""
        if auth:
            user_id, get_chat = auth
            authkey = (await get_chat())["authkey"]
            await self.send(self.channel, user_id, authkey, method="auth")
        else:
            await self.send(self.channel, method="auth")

    async def parse(self, packet):
        """Parse a chat packet."""

        try:
            packet = json.loads(packet)
        except (TypeError, ValueError):
            self.logger.exception("Invalid JSON: %s.", packet)
            return None
        else:
            if packet.get("error") is not None:
                self.logger.error(packet)
            else:
                self.logger.debug(packet)
            return packet

    @property
    def _packet_id(self):
        return next(self._packet_counter)
