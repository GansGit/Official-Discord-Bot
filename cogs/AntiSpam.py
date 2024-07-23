import datetime
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

                embed = discord.Embed(
                    title='Insult-Warning!',
                    description=f'Hey {message.author.mention}, \n'
                                f'Insults are not permitted on this Server!',
                    color=discord.Colour.dark_red(),
                    timestamp=datetime.datetime.now()
                )
                embed.set_footer(text='Coding Soul - AntiSpam', icon_url=Config.get_config('footer')['icon-url'])

                await message.delete()
                await message.channel.send(embed=embed)
                break

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        await self.check_message(message=message)


def setup(bot):
    bot.add_cog(AntiSpam(bot))
