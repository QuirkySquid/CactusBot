"""Parse Beam packets."""

import json
from os import path

from ...packets import EventPacket, MessagePacket


class BeamParser:
    """Parse Beam packets."""

    # TODO: update with accurate values
    ROLES = {
        "Owner": 100,
        "Founder": 91,
        "Staff": 90,
        "Global Mod": 85,
        "Mod": 50,
        "Subscriber": 20,
        "Pro": 5,
        "User": 1,
        "Muted": 0,
        "Banned": 0
    }

    with open(path.join(path.dirname(__file__), "emoji.json")) as file:
        EMOJI = json.load(file)

    @classmethod
    def parse_message(cls, packet):
        """Parse a Beam message packet."""

        message = []
        for component in packet["message"]["message"]:
            chunk = {
                "type": component["type"],
                "data": "",
                "text": component["text"]
            }
            if component["type"] == "emoticon":
                chunk["type"] = "emoji"
                chunk["data"] = cls.EMOJI.get(component["text"], "")
                message.append(chunk)
            elif component["type"] == "inaspacesuit":
                chunk["type"] = "emoji"
                chunk["data"] = ""
                message.append(chunk)
            elif component["type"] == "link":
                chunk["data"] = component["url"]
                message.append(chunk)
            elif component["type"] == "tag":
                chunk["data"] = str(component["id"])
                message.append(chunk)
            elif component["text"]:
                chunk["data"] = component["text"]
                message.append(chunk)

        return MessagePacket(
            *message,
            user=packet["user_name"],
            role=cls.ROLES[packet["user_roles"][0]],
            action=packet["message"]["meta"].get("me", False),
            target=packet["message"]["meta"].get(
                "whisper", None) and packet["target"]
        )

    @classmethod
    def parse_follow(cls, packet):
        """Parse follow packet."""

        return EventPacket(
            "follow",
            packet["user"]["username"],
            packet["following"]
        )

    @classmethod
    def parse_subscribe(cls, packet):
        """Parse subscribe packet."""

        return EventPacket("subscribe", packet["user"]["username"])

    @classmethod
    def parse_host(cls, packet):
        """Parse host packet."""

        return EventPacket("host", packet["hoster"]["token"])

    @classmethod
    def synthesize(cls, packet):
        """Create a Cactus MessagePacket from Beam packets."""

        message = ""
        emoji = dict(zip(cls.EMOJI.values(), cls.EMOJI.keys()))

        if packet.action:
            message = "/me "

        for index, component in enumerate(packet):
            if component.type == "emoji":
                message += emoji.get(component.data, component.text)
                if (index < len(packet) - 1 and
                        not packet[index + 1].startswith(' ')):
                    message += ' '
            elif component.type == "tag":
                message += '@' + component.text
            else:
                message += component.text

        if packet.target:
            return (packet.target, message), {"method": "whisper"}

        return (message,), {}
