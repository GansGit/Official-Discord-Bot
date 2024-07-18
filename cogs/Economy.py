from discord.ext import commands
from discord.commands import slash_command
import discord
import ezcord
import sqlite3

from EconomyManager import Manager


class Economy(ezcord.Cog, emoji='🍪', description="Show information about the bot", hidden=True):
    def __int__(self, bot):
        self.bot = bot
        self.manager = Manager(self=bot) # defining database manager
    @commands.Cog.listener()
    async def on_ready(self):
        # creating economy database, if not exists
        self.manager.create_database()

    @slash_command()
    async def setup(self, ctx:discord.ApplicationContext):
        self.manager.createUser(user_id=ctx.user.id)
        await ctx.respond('Created user', ephemeral=True)

def setup(bot):
    bot.add_cog(Economy(bot))