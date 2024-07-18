from discord.ext import commands
from discord.commands import slash_command
import discord
import ezcord
import sqlite3

from EconomyManager import Manager


class Economy(ezcord.Cog, emoji='🍪', description="Show information about the bot", hidden=True):
    @commands.Cog.listener()
    async def on_ready(self):
        Manager.create_database()
        


def setup(bot):
    bot.add_cog(Economy(bot))