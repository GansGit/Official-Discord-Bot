import ezcord
import discord
import logging

import EconomyManager
from discord.ext import commands


class Economy(ezcord.Cog, hidden=True):
    def __init__(self, bot):
        self.bot = bot

    # On-Cog-Load
    @commands.Cog.listener()
    async def on_ready(self):
        # Creating database if not exists
        try:
            EconomyManager.create_database()
            print('Database is now available!')
        except Exception as e:
            print(f'Error creating database: {e}')


# setup for the cog
def setup(bot):
    bot.add_cog(Economy(bot))
