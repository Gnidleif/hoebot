#!/usr/bin/python3.12
import asyncio
from discord import Member, Status
from discord.ext import commands
from random import randint
from tools import ts_print, write_json, read_json
from datetime import datetime, timedelta

class Members(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self._random_timeout_list = {}
        self._random_timeout_tasks = {}

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        self._random_timeout_list = read_json("storage/random_timeouts")
        for member_id in self._random_timeout_list:
            data = self._random_timeout_list[member_id]

            guild = self.bot.get_guild(data["guild"])
            if guild is None:
                continue

            member = await guild.fetch_member(member_id)
            if member is None:
                continue

            self._random_timeout_tasks[member_id] = self.bot.loop.create_task(
                self._random_timeout(
                    member, 
                    data["sides"], 
                    data["timeout_time"], 
                    data["channel"]))

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
            self._random_timeout_tasks[member.id].cancel()
            await ctx.send(f"{member.mention} is no longer randomly set on timeout")
            _ = self._random_timeout_list.pop(member.id)
            _ = self._random_timeout_tasks.pop(member.id)
        else:
            self._random_timeout_tasks[member.id] = self.bot.loop.create_task(
                self._random_timeout(
                    member, 
                    sides, 
                    timeout_time, 
                    ctx))
            self._random_timeout_list[member.id] = {
                "guild": ctx.guild.id,
                "channel": ctx.channel.id,
                "sides": sides,
                "timeout_time": timeout_time
            }
            await ctx.send(f"{ctx.author.mention}: {member.mention} now has a {1/sides}% chance every second to be set on timeout for {timeout_time} seconds")

        write_json(self._random_timeout_list, "storage/random_timeouts")
        
    async def _random_timeout(self, member: Member, sides: int, timeout_time: int, ctx = None) -> None:
        while not self.bot.is_closed():
            sleep_time: int = 1
            roll: int = randint(1, sides)
            if member.status is not Status.online:
                ts_print(f"{member} is offline")
                await asyncio.sleep(600)

            if roll == 1:
                sleep_time = timeout_time
                delta = timedelta(seconds=timeout_time)
                until = datetime.now() + delta
                try:
                    await member.timeout(delta, reason="lol")
                except Exception as ex:
                    ts_print(ex)

                msg = f"{member.mention} is now timed out until {until.strftime('%H:%M:%S')}"

                if type(ctx) is not int:
                    await ctx.send(msg)
                else:
                    channel = self.bot.get_channel(ctx)
                    await channel.send(msg)
                ts_print(msg)

            await asyncio.sleep(sleep_time)

async def setup(bot):
    await bot.add_cog(Members(bot))