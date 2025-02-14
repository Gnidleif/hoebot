#!/usr/bin/python3.12
from discord import Member
from discord.ext import commands

class Messages(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot