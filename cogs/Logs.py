import discord
from discord.ext import commands

from cogs.Config import Config 
from update_stats import Updater

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.updater = Updater(bot=bot)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.updater.update()
        
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.updater.update()
        
        embed = discord.Embed(
            title='Member joined',
            description=f'{member.mention}',
            color=discord.Color.blue(),
        )
        
        embed.set_footer(text = Config.get_config('footer')['text'] + ' - Logging')
        
        log_channel = await self.bot.fetch_channel(Config.get_config('log')['channel'])
        await log_channel.send(embed=embed)
        await member.add_roles(member.guild.get_role(1256611699230904350))
        await member.add_roles(member.guild.get_role(1260600394460172389))
        await member.add_roles(member.guild.get_role(1260600444271460444))
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.updater.update()
        
        embed = discord.Embed(
            title='Member left',
            description=f'{member.mention}',
            color=discord.Color.red(),
        )
        
        embed.set_footer(text = Config.get_config('footer')['text'] + ' - Logging')
        
        log_channel = await self.bot.fetch_channel(Config.get_config('log')['channel'])
        await log_channel.send(embed=embed)
    
    
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        await self.updater.update()
    
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        await self.updater.update()
    
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        await self.updater.update()
        
def setup(bot):
    bot.add_cog(Logs(bot))