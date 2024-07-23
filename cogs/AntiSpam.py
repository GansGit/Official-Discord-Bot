
import ezcord
import discord

from discord.ext import commands
from cogs.Config import Config


class AntiSpam(ezcord.Cog, hidden=True):

    async def check_message(self, message: discord.Message):
        if message.author.bot:
            return

        msg = message.content.split()

        blacklist = Config.get_config('anti-spam')['blacklist']

        for word in msg:
            print("Überprüftes Wort:", word)
            if word.lower() in [b.lower() for b in blacklist]:

                await message.delete()
                await message.channel.send('Test!!!')
                break

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        await self.check_message(message=message)


def setup(bot):
    bot.add_cog(AntiSpam(bot))
