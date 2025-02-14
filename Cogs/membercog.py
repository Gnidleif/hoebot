#!/usr/bin/python3.12
from discord import Member, Guild, Message
from discord.ext import commands
from tools import ts_print

class MemberCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_ready(self) -> None:
    #     for guild in self.bot.guilds:
    #         ts_print(f"Members of {guild}({guild.id}):")
    #         await self.write_members(guild)

    async def write_members(self, guild: Guild):
        for member in guild.members:
            ts_print(f"{member.display_name}({member.id})")