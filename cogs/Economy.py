import datetime

import ezcord
import discord
import logging

import EconomyManager
from discord.ext import commands
from discord.commands import option, slash_command
from cogs.Config import Config

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
    @discord.default_permissions(administrator=True)
    async def balance(self, ctx: discord.ApplicationContext, user: discord.User = None):
        if user is None:  # check if user was not typed in
            user = ctx.user  # sets user to the author of the cmd

        if user.bot:  # check if user is bot
            await ctx.respond("Can't display the balance of a bot", ephemeral=True)  # sending mistake to user
            return

        rs = EconomyManager.doesUserExist(ctx.user.id)

        if rs is not None:
            bal_embed = discord.Embed(  # designing the embed
                title=f'Balance of {user.display_name}',
                color=discord.Colour.orange(),
                timestamp=datetime.datetime.now()
            )

            bal_embed.add_field(name='Bank', value=f'{rs[0][1]} :dollar:', inline=True)
            bal_embed.add_field(name='Wallet', value=f'{rs[0][2]} :dollar:', inline=True)
            bal_embed.set_footer(text='Coding Soul', icon_url=Config.get_config('footer')['icon-url'])

            await ctx.respond(embed=bal_embed)  # responding to the user

        else:
            EconomyManager.createUser(ctx.user.id)
            await ctx.respond('Account successfully created!', ephemeral=True)


# setup for the cog
def setup(bot):
    bot.add_cog(Economy(bot))
