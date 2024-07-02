from discord.ext import commands
from discord.commands import slash_command
import discord
import ezcord

import datetime, time
import platform

from cogs.Config import Config

class Botinfo(ezcord.Cog, emoji='🍪', description="Show information about the bot"):
    def __init__(self, bot):
        self.bot = bot
        self.startTime = time.time() # creating a variable, that is counting the time since booting up
    
    # on_ready event 
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Bot is now online!')
            
    @slash_command(description="Show's general information about the bot", name='botinfo')
    async def botinfo(self, ctx):
        # Uptime
        current_time = time.time()
        difference = int(round(current_time - self.startTime))
        uptime_text = str(datetime.timedelta(seconds=difference))
        # Slash Command Counter
        slash_commands = len(self.bot.application_commands)
        # Bot Version
        bot_version = Config.get_config('bot')['version']
        
        
        embed = discord.Embed(
            title='Bot Statistics',
            description='Here are some general information about the bot',
            color=discord.Color.green()
        )
        
        embed.add_field(name='Uptime', value=f'{uptime_text}', inline=True)
        embed.add_field(name='Bot Version', value=f'{bot_version}', inline=True)
        embed.add_field(name='Slash Commands', value=f'{slash_commands}', inline=True)
        embed.add_field(name='OS', value=platform.system(), inline=True)
        embed.add_field(name='OS Version', value=platform.version(), inline=True)
        embed.set_footer(text=Config.get_config('footer')['text'] + " - Botinfo", icon_url=ctx.author.avatar)
                
        await ctx.respond(embed=embed)
           
def setup(bot):
    bot.add_cog(Botinfo(bot))