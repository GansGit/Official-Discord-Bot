import discord
from discord.ext import commands

from cogs.Config import Config 

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_member_join(self, member):

        embed = discord.Embed(
            title='Member joined',
            description=f'{member.mention}',
            color=discord.Color.dark_theme(),
        )
        
        embed.set_footer(text = Config.get_config('footer')['text'] + ' - Logging')
        
        log_channel = await self.bot.fetch_channel(Config.get_config('log')['channel'])
        await log_channel.send(embed=embed)
        await member.add_roles(member.guild.get_role(1256611699230904350))
        
def setup(bot):
    bot.add_cog(Logs(bot))