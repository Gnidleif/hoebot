#!/usr/bin/python3.12
from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy
from tools import ts_print, read_json, setup_logging
from discord import Intents
from discord.ext import commands

class HoeBot(commands.Bot):
    def __init__(self) -> None:
        intents = Intents.default()
        intents.presences = True
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix=commands.when_mentioned_or('$'), 
                         intents=intents)

    async def setup_hook(self) -> None:
        await self.load_extension("cogs.membercog")

    async def on_ready(self) -> None:
        ts_print(f"{self.user} started, member of:")
        for guild in self.guilds:
            ts_print(f"\t{guild} ({guild.id})")

if __name__ == "__main__":
    set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    setup_logging()
    config = read_json("config")
    HoeBot().run(token=config["token"])