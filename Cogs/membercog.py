#!/usr/bin/python3.12
import asyncio
from discord import Member
from discord.ext import commands
from tools import ts_print
from random import randint
from datetime import datetime, timedelta

class Members(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self._random_timeout_list = {}

    async def cog_check(self, ctx):
        return ctx.author.guild_permissions.administrator

    @commands.command(name="random_timeout")
    async def cmd_random_timeout(self, ctx, *, 
                                 member: Member, 
                                 chance: int = 2) -> None:
        """Attempts to randomly timeout a member for a minute every second"""
        if member is None:
            return

        if member.id in self._random_timeout_list:
            self._random_timeout_list[member.id].cancel()
            await ctx.send(f"{member.mention} is no longer randomly set on timeout")
            return
        
        self._random_timeout_list[member.id] = self.bot.loop.create_task(
            self.random_timeout(ctx=ctx,
                                member=member,
                                chance=chance))
        await ctx.send(f"{member.mention} is now randomly set on timeout")
        
    async def random_timeout(self, ctx, *, member: Member, chance: int) -> None:
        while True:
            sleep_time: int = 1
            roll: int = randint(1, chance)
            if roll == 1:
                sleep_time = 5
                timeout_time = datetime.now() + timedelta(seconds=sleep_time)

                await ctx.send(f"Random timeout: {member.mention} until {timeout_time.strftime('%H:%M:%S')}")
                try:
                    await member.timeout(timeout_time, reason="lol")
                except:
                    ...
            await asyncio.sleep(sleep_time)
            # await member.timeout(60, reason="lol")