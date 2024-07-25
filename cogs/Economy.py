import ezcord
import discord

from discord.ext import commands


class Economy(ezcord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass


def setup(bot):
    bot.add_cog(Economy(bot))
