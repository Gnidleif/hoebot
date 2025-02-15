#!/usr/bin/python3.12
from discord import Member
from discord.ext import commands

class Randoms(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self._last_member: Member = None

    @commands.command(name="hello")
    async def hello_cmd(self, ctx, *, member: Member = None) -> None:
        """Says hello to the @mentioned member"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f"Hello, {member.mention}~")
        else:
            await ctx.send(f"Hello, {member.mention}... this feels familiar")
        self._last_member = member