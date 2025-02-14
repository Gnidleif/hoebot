#!/usr/bin/python3.12
import json, asyncio
from tools import ts_print
from discord import Intents, Message
from discord.ext import commands
from pathlib import Path
from Cogs import *

__location__ = Path(__file__).parent.resolve()

class HoeBot(commands.Bot):
    def __init__(self) -> None:
        intents = Intents.default()
        intents.presences = True
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix="$", intents=intents)

    async def setup_hook(self) -> None:
        await self.add_cog(membercog.MemberCog(self))
        await self.add_cog(messagecog.Messages(self))

    async def on_ready(self) -> None:
        ts_print(f"{self.user} started, member of:")
        for guild in self.guilds:
            ts_print(f"\t{guild} ({guild.id})")

    async def on_command_error(self, context, exception):
        return await super().on_command_error(context, exception)

def main(config: dict[str, str]):
    HoeBot().run(token=config["token"])
    return False

if __name__ == "__main__":
    with open(__location__ / "config.json", 'r', encoding="utf-8") as r_json:
        config = json.load(r_json)
    main(config)