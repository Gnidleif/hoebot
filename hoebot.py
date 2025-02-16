#!/usr/bin/python3.12
import asyncio
from tools import ts_print, read_json, setup_logging
from discord import Intents, Status
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
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    setup_logging()
    config = read_json("config")
    client = HoeBot()

    try:
        client.run(token=config["token"])
    except KeyboardInterrupt:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(client.change_presence(status=Status.offline))
        client.close()
        for task in asyncio.all_tasks():
            task.cancel()