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
        self._random_timeout_info = {}
        self._random_timeout_tasks = {}

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        self._random_timeout_info = read_json("storage/random_timeouts")
        if len(self._random_timeout_info) == 0:
            return
        
        for member_id in self._random_timeout_info:
            data = self._random_timeout_info[member_id]

            guild = self.bot.get_guild(data["guild"])
            if guild is None:
                continue

            async for fetched in guild.fetch_members():
                if fetched.id == int(member_id):
                    member = guild.get_member(fetched.id)
                    break

            if member is None or member.status is Status.offline:
                continue

            self._random_timeout_tasks[member_id] = self.bot.loop.create_task(
                self._random_timeout(
                    member, 
                    data["sides"], 
                    data["timeout_time"], 
                    self.bot.get_channel(data["channel"])))
            
    @commands.Cog.listener()
    async def on_presence_update(self, before: Member, after: Member) -> None:
        member_id = str(after.id)
        if member_id not in self._random_timeout_info or before.status == after.status:
            return
        
        if after.status is not Status.offline and member_id not in self._random_timeout_tasks:
            data = self._random_timeout_info[member_id]

            self._random_timeout_tasks[member_id] = self.bot.loop.create_task(
                self._random_timeout(
                    after,
                    data["sides"],
                    data["timeout_time"],
                    self.bot.get_channel(data["channel"])))
        elif member_id in self._random_timeout_tasks:
            self._random_timeout_tasks[member_id].cancel()
            self._random_timeout_tasks.pop(member_id)

    @commands.command(name="random_timeout", aliases=["rto"])
    @commands.has_guild_permissions(moderate_members=True)
    async def cmd_random_timeout(self, ctx,
                                 member: Member = commands.parameter(description="Member to time out"),
                                 sides: int = commands.parameter(default=1800,
                                                                  description="Sides of the die"),
                                 timeout_time: int = commands.parameter(default=60,
                                                                        description="Timeout time")) -> None:
        """
        Sometimes randomly times out given member
        """
        member_id = str(member.id)
        if member_id in self._random_timeout_info:
            if member_id in self._random_timeout_tasks:
                self._random_timeout_tasks[member_id].cancel()
                _ = self._random_timeout_tasks.pop(member_id)
            _ = self._random_timeout_info.pop(member_id)
            msg = f"{member.mention} is no longer randomly set on timeout"
        else:
            if member.status is not Status.offline:
                self._random_timeout_tasks[member_id] = self.bot.loop.create_task(
                    self._random_timeout(
                        member, 
                        sides, 
                        timeout_time, 
                        ctx.channel))
            self._random_timeout_info[member_id] = {
                "guild": ctx.guild.id,
                "channel": ctx.channel.id,
                "sides": sides,
                "timeout_time": timeout_time
            }
            msg = f"{member.mention} now has a {100/sides:.4f}% chance every second to be set on timeout for {timeout_time} seconds"
        
        ts_print(msg)
        await ctx.send(msg)
        write_json(self._random_timeout_info, "storage/random_timeouts")
        
    async def _random_timeout(self, member: Member, sides: int, timeout_time: int, channel) -> None:
        ts_print(f"Timeout coroutine started for {member.mention}")
        while not self.bot.is_closed():
            sleep_time: int = 1
            roll: int = randint(1, sides)
            if roll == 1 and not member.is_timed_out():
                sleep_time = timeout_time
                delta = timedelta(seconds=timeout_time)
                until = datetime.now() + delta
                try:
                    await member.timeout(delta, reason="lol")
                    msg = f"{member.mention} is now timed out until {until.strftime('%H:%M:%S')}"
                    await channel.send(msg)
                    ts_print(msg)
                except Exception as ex:
                    ts_print(ex)
                    sleep_time = 1

            await asyncio.sleep(sleep_time)

async def setup(bot):
    await bot.add_cog(Members(bot))