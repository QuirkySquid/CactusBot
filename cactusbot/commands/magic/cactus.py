"""Cactus command."""


from . import Command
from ...packets import MessagePacket


@Command.command()
class Cactus(Command):
    """Ouch! That's pokey!"""

    COMMAND = "cactus"

    @Command.command(name="cactus")
    async def default(self):
        """Default response."""

        return MessagePacket(
            ("text", "Ohai! I'm CactusBot! "),
            ("emoji", ":cactus:", ":cactus:")
        )

    @Command.command()
    async def docs(self):
        """Documentation response."""

        return MessagePacket(
            ("text", "Check out my documentation at "),
            ("url", "https://cactusbot.rtfd.org", "cactusbot.rtfd.org"),
            ("text", ".")
        )

    @Command.command()
    async def twitter(self):
        """Twitter response."""

        return MessagePacket(
            ("text", "You can follow the team behind CactusBot at: "),
            ("url", "https://twitter.com/CactusDevTeam",
             "twitter.com/CactusDevTeam")
        )

    @Command.command()
    async def github(self, project=None):
        """Github response."""

        if project is None or project.lower() in ("bot", "cactusbot"):
            return MessagePacket(
                "Check out my GitHub repository at: ",
                ("url", "https://github.com/CactusDev/CactusBot",
                 "github.com/CactusDev/CactusBot")
            )
        elif project.lower() == "issue":
            return MessagePacket(
                "Create a GitHub issue at: ",
                ("url", "https://github.com/CactusDev/CactusBot/issues",
                 "github.com/CactusDev/CactusBot/issues")
            )
        elif project.lower() in ("api", "cactusapi"):
            return MessagePacket(
                "Check out the GitHub repository for CactusAPI at: ",
                ("url", "https://github.com/CactusDev/CactusAPI",
                 "github.com/CactusDev/CactusAPI")
            )
        elif project.lower() == "sepal":
            return MessagePacket(
                "Check out the GitHub repository for Sepal at: ",
                ("url", "https://github.com/CactusDev/Sepal",
                 "github.com/CactusDev/Sepal")
            )
        return MessagePacket("Unknown project '{0}'.".format(project))

    @Command.command()
    async def help(self):
        """Help response."""

        return ("Try our docs (!cactus docs). If that doesn't help, tweet at"
                " us (!cactus twitter)!")
