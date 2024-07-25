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
        if user is None:  # check if user was not typed in
            user = ctx.user  # sets user to the author of the cmd

        if user.bot:  # check if user is bot
            await ctx.respond("Can't display the balance of a bot", ephemeral=True)  # sending mistake to user
            return

        rs = EconomyManager.doesUserExist(ctx.user.id)

        if rs is not None:
            print(rs[0][1])
        else:
            EconomyManager.createUser(ctx.user.id)

        await ctx.respond(f'{user.mention}')  # responding to the user

# setup for the cog
def setup(bot):
    bot.add_cog(Economy(bot))
