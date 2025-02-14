#!/usr/bin/python3.12
from tools import ts_print
from discord import Message, Member
from discord.ext import commands

class Messages(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="hello")
    async def hello_cmd(self, ctx, *, member: Member = None) -> None:
        """Says hello to the @mentioned member"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f"Hello, {member.mention}~")
        else:
            await ctx.send(f"Hello, {member.mention}... this feels familiar")
        self._last_member = member