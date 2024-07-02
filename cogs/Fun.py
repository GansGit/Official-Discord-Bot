from discord.ext import commands
from discord.commands import slash_command
import discord

import ezcord
import requests
import json

from cogs.Config import Config

class Fun(ezcord.Cog, emoji='🐧'):
    @slash_command(description="Show's a random fact about anything in the world.")
    async def fact(self, ctx):
        api_url = f'https://api.api-ninjas.com/v1/facts'
        response = requests.get(api_url, headers={'X-Api-Key': '5mL4GuH2YS67IP3mCTilXQ==6YtvGhWWOjJqU6OT'})
        
        print(response.text)
        
        if response.status_code == requests.codes.ok:
            
            data = json.loads(response.text)
            fact = data[0]['fact']
            ft_text = Config.get_config('footer')['text']
            
            embed = discord.Embed(
                title='Random Fact',
                description=f'{fact}',
                color=discord.Color.green()
            )
            embed.set_footer(text=f'{ft_text} - Fact by api-ninjas.com')
            
            await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))