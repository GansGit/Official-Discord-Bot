import ezcord
import discord
import logging

import EconomyManager
from discord.ext import commands
from discord.commands import option, slash_command


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

    @slash_command(name='balance', description="Display's the account of a user")
    @option('user', description="Pick a user")
    async def balance(self, ctx: discord.ApplicationContext, user: discord.User = None):
        if user is None:
            user = ctx.author

        await ctx.respond('')


# setup for the cog
def setup(bot):
    bot.add_cog(Economy(bot))
