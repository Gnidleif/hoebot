#!/usr/bin/python3.12
import asyncio
from discord import Member
from discord.ext import commands
from random import randint
from datetime import datetime, timedelta

class Members(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self._random_timeout_list = {}

    @commands.command(name="random_timeout", aliases=["rto"])
    @commands.has_guild_permissions(moderate_members=True)
    async def cmd_random_timeout(self, ctx,
                                 member: Member = commands.parameter(description="Member to time out"),
                                 sides: int = commands.parameter(default=1000,
                                                                  description="Sides of the die"),
                                 timeout_time: int = commands.parameter(default=60,
                                                                        description="Timeout time")) -> None:
        """
        Sometimes randomly times out given member
        """
        if member.id in self._random_timeout_list:
            self._random_timeout_list[member.id].cancel()
            await ctx.send(f"{member.mention} is no longer randomly set on timeout")
            _ = self._random_timeout_list.pop(member.id)
            return
        
        self._random_timeout_list[member.id] = self.bot.loop.create_task(
            self.random_timeout(ctx, member, sides, timeout_time))
        await ctx.send(f"{ctx.author.mention}: {member.mention} now has a {1/sides}% chance every second to be set on timeout for {timeout_time} seconds")
        
    async def random_timeout(self, ctx, member: Member, sides: int, timeout_time: int) -> None:
        while not self.bot.is_closed():
            sleep_time: int = 1
            roll: int = randint(1, sides)
            if roll == 1:
                sleep_time = timeout_time
                until = datetime.now() + timedelta(seconds=timeout_time)
                await ctx.send(f"{member.mention} is now timed out until {until.strftime('%H:%M:%S')}")
                try:
                    await member.timeout(until, reason="lol")
                except:
                    ...
            await asyncio.sleep(sleep_time)

async def setup(bot):
    await bot.add_cog(Members(bot))