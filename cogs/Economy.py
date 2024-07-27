import asyncio
import datetime
import random

import ezcord
import discord
import utils.TimeConverter as TimeConverter
from utils import EconomyManager

from discord.ext import commands
from discord.commands import option, slash_command
from cogs.Config import Config


async def random_slot():
    emoji_list = ['🍎', '🪙', '🍐', '🍆']
    rs: list = []

    while len(rs) < 3:
        rs.append(random.choice(emoji_list))
    return rs


async def check_prize(rs_list: list) -> int:
    if len(rs_list) != 3:
        raise ValueError()

    count = 0

    if rs_list[0] == rs_list[1]:
        count += 1
    if rs_list[1] == rs_list[2]:
        count += 1

    return count


class Economy(ezcord.Cog, emoji='💵'):
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
    async def balance(self, ctx: discord.ApplicationContext):
        rs = EconomyManager.doesUserExist(ctx.user.id)

        if rs is not None:  # Checking if user exists
            bal_embed = discord.Embed(  # designing the embed
                title=f'Balance of {ctx.user.display_name}',
                color=discord.Colour.orange(),
                timestamp=datetime.datetime.now()
            )

            bal_embed.add_field(name='Bank', value=f'{rs[0][1]} <:souls:1266390733821317230>', inline=True)
            bal_embed.add_field(name='Wallet', value=f'{rs[0][2]} <:souls:1266390733821317230>', inline=True)
            bal_embed.set_footer(text='Coding Soul', icon_url=Config.get_config('footer')['icon-url'])

            await ctx.respond(embed=bal_embed)  # responding to the user

        else:
            EconomyManager.createUser(ctx.user.id)  # creating user
            await ctx.respond('Account successfully created!', ephemeral=True)

    @slash_command(name='work', description="Work to get some money")
    @commands.cooldown(1, TimeConverter.h_in_s(0.5), commands.BucketType.user)  # cooldown
    async def work(self, ctx: discord.ApplicationContext):
        rs = EconomyManager.doesUserExist(ctx.user.id)

        if rs is None:  # checking if user exists
            EconomyManager.createUser(ctx.user.id)  # creating an account for the user

        earnings = random.randint(25, 250)

        EconomyManager.add_coins(ctx.user.id, earnings, 'bank')  # adding coins in database
        await ctx.respond(
            f"You've worked as a freelancer and earned {earnings} <:souls:1266390733821317230> ")  # responding to user

    @slash_command(name='add-coins', description='Set currency of a user')
    @discord.default_permissions(administrator=True)
    @option('User', description='Pick a user where you want to', required=True)
    @option('Method', description='Pick the method', choices=['bank', 'wallet'], required=True)
    async def add_coins(self, ctx, user: discord.User, method: str, amount: int):
        EconomyManager.add_coins(user.id, amount, method=method)
        await ctx.respond(f'Added {amount} <:souls:1266390733821317230> to {user.mention}', ephemeral=True)

    @slash_command(name='leaderboard', description='Check the leaderboard!')
    async def leaderboard(self, ctx: discord.ApplicationContext):
        leaderboard_list = EconomyManager.get_leaderboard()

        pos = 1

        desc = "## Top 10 Users:\n"

        for i in leaderboard_list:
            user = await self.bot.fetch_user(i[0])
            pos_str = await self.conv_pos(pos)
            desc += f"{pos_str}. {user.mention} • {i[1]} <:souls:1266390733821317230>\n"
            pos += 1

        board_embed = discord.Embed(
            title='Leaderboard',
            color=discord.Color.orange(),
            description=desc,
            timestamp=datetime.datetime.now()
        )
        board_embed.set_footer(text='Coding Soul - Economy', icon_url=Config.get_config('footer')['icon-url'])

        await ctx.respond(embed=board_embed)

    async def conv_pos(self, pos: int):
        if pos == 1:
            return ":first_place:"
        elif pos == 2:
            return ":second_place:"
        elif pos == 3:
            return ":third_place:"
        else:
            return '<:silver_medal:1266388617140371497>'

    @slash_command(name='shop', description='Check the shop!')
    async def shop(self, ctx: discord.ApplicationContext):
        # list for role: id, prize, function
        roles = Config.get_config('economy')['shop-roles']
        description = ""

        for role in roles:
            guild = ctx.guild
            get_role = discord.utils.get(guild.roles, id=role[0])
            description += f"\n{get_role.mention}: `{role[1]}` <:souls:1266390733821317230>"

        embed = discord.Embed(  # embed
            title='<:home:1264678646531227751> › Soul Shop',
            color=discord.Color.orange(),
            description=description,
            timestamp=datetime.datetime.now()
        )
        embed.set_footer(text='Coding Soul - Economy', icon_url=Config.get_config('footer')['icon-url'])  # set footer
        await ctx.respond(embed=embed, ephemeral=True)  # responding user

    @slash_command(name='slots', description='Play some slots, bro!')
    @option(name='Amount', required=True, description='Select the amount you wanna play with!')
    @commands.cooldown(1, 7, commands.BucketType.user)  # cooldown
    async def slots(self, ctx: discord.ApplicationContext, amount: int):

        current_coins = EconomyManager.get_coins(ctx.user.id, method='wallet')

        if current_coins < amount:
            await ctx.respond('To less money to play!', ephemeral=True)
            return
        if amount < 0:
            await ctx.respond("You can't play with 0 or negative bet!", ephemeral=True)
            return

        # First slot row
        slot: list = await random_slot()
        embed = discord.Embed(
            title='Slots',
            description=f'{slot[0]} | {slot[1]} | {slot[2]}',
            color=discord.Color.orange()
        )
        msg: discord.Message = await ctx.respond(embed=embed)
        await asyncio.sleep(1)

        a = 0
        while a < 3:
            # Going through 3x random slots
            slot: list = await random_slot()
            embed = discord.Embed(
                title='Slots',
                description=f'{slot[0]} | {slot[1]} | {slot[2]}',
                color=discord.Color.orange()
            )
            await msg.edit(embed=embed)
            await asyncio.sleep(1)
            a += 1

        rs = await check_prize(slot)
        if rs == 0:
            await ctx.respond(f"You've lost {amount} <:souls:1266390733821317230>")
            EconomyManager.remove_coins(user_id=ctx.user.id, method='wallet', amount=amount)
        elif rs == 1:
            await ctx.respond(f"You've got {amount * 2} <:souls:1266390733821317230>")
            EconomyManager.add_coins(user_id=ctx.user.id, method='wallet', amount=amount * 2)
        elif rs == 2:
            await ctx.respond(f"You've got {amount * 3} <:souls:1266390733821317230>")
            EconomyManager.add_coins(user_id=ctx.user.id, method='wallet', amount=amount * 3)

    @slash_command(name='withdraw', description='Withdraw some money!')
    @option(name='amount', description='The amount of the money.')
    async def withdraw(self, ctx: discord.ApplicationContext, amount: int):
        current_coins = EconomyManager.get_coins(ctx.user.id, method='bank')

        if current_coins < amount:
            await ctx.respond("You have too less money on the bank!", ephemeral=True)
            return
        if amount < 0:
            await ctx.respond("You can't withdraw 0 or negative money!", ephemeral=True)
            return

        EconomyManager.remove_coins(user_id=ctx.user.id, method='bank', amount=amount)
        EconomyManager.add_coins(user_id=ctx.user.id, method='wallet', amount=amount)
        await ctx.respond("The money was successfully withdrawn.", ephemeral=True)

    @slash_command(name='deposit', description='Deposit some money!')
    @option(name='amount', description='The amount of the money.')
    async def deposit(self, ctx: discord.ApplicationContext, amount: int):
        current_coins = EconomyManager.get_coins(ctx.user.id, method='wallet')

        if current_coins < amount:
            await ctx.respond("You have too less money on the wallet!", ephemeral=True)
            return
        if amount < 0:
            await ctx.respond("You deposit 0 or negative money!", ephemeral=True)
            return

        EconomyManager.remove_coins(user_id=ctx.user.id, method='wallet', amount=amount)
        EconomyManager.add_coins(user_id=ctx.user.id, method='bank', amount=amount)
        await ctx.respond("The money was successfully deposited.", ephemeral=True)


# setup for the cog
def setup(bot):
    bot.add_cog(Economy(bot))
