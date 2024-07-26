import datetime
import random

import ezcord
import discord

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

    @slash_command(name='balance', description="Display your Money balance ;)")
    @option('user', description="Pick a user")
    @discord.default_permissions(administrator=True)
    async def balance(self, ctx: discord.ApplicationContext):
        rs = EconomyManager.doesUserExist(ctx.user.id)

        if rs is not None:  # Checking if user exists
            bal_embed = discord.Embed(  # designing the embed
                title=f'Balance of {ctx.user.display_name}',
                color=discord.Colour.orange(),
                timestamp=datetime.datetime.now()
            )

            bal_embed.add_field(name='Bank', value=f'{rs[0][1]} :dollar:', inline=True)
            bal_embed.add_field(name='Wallet', value=f'{rs[0][2]} :dollar:', inline=True)
            bal_embed.set_footer(text='Coding Soul', icon_url=Config.get_config('footer')['icon-url'])

            await ctx.respond(embed=bal_embed)  # responding to the user

        else:
            EconomyManager.createUser(ctx.user.id)  # creating user
            await ctx.respond('Account successfully created!', ephemeral=True)

    @slash_command(name='work', description="Work to get some money")
    @commands.cooldown(1, 5, commands.BucketType.user)  # cooldown
    async def work(self, ctx: discord.ApplicationContext):
        rs = EconomyManager.doesUserExist(ctx.user.id)

        if rs is None:  # checking if user exists
            EconomyManager.createUser(ctx.user.id)  # creating an account for the user

        earnings = random.randint(25, 250)

        await ctx.respond(f"You've worked as a freelancer and earned {earnings} :dollar:")


# setup for the cog
def setup(bot):
    bot.add_cog(Economy(bot))
