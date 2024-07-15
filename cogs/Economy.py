from discord.ext import commands
from discord.commands import slash_command
import discord
import ezcord
import sqlite3

from EconomyManager import Manager
from cogs.Config import Config


class Economy(ezcord.Cog, emoji='🍪', description="Show information about the bot"):
    @commands.Cog.listener()
    async def on_ready(self):
        createDB()


def setup(bot):
    bot.add_cog(Economy(bot))