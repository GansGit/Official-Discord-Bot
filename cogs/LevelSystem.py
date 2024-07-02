from discord.ext import commands
from discord.commands import slash_command
import discord
import ezcord

import json
import random
import math

from cogs.Config import Config

class LevelSystem(ezcord.Cog):
    @commands.Cog.listener()
    async def on_message(self, message : discord.Message):
        if message.author.bot:
            return
        
        def xp_to_level(xp, k=100):
            return int(math.sqrt(xp/k))
        
        def load_json():
            with open('levels.json', 'r') as file:
                return json.load(file)
    
        def save_json(data):
            with open('levels.json', 'w') as file:
                json.dump(data, file, indent=4)
            
        def add_or_update_xp(data, user_id, xp_to_add):
            user_id_str = str(user_id)
            if user_id_str in data:
                data[user_id_str]['xp'] += xp_to_add
                data[user_id_str]['level'] = xp_to_level(data[user_id_str]['xp'])
                
            else:
                data[user_id_str] = {'xp':xp_to_add, 'level':xp_to_level}
            return data
            
        channels = Config.get_config('level-system')['allowed-channels']
        
        
        for channel in channels:
            if message.channel.id == channel:
                random_xp = random.randint(15, 43)
                data = load_json()
                user_id = message.author.id
                current_level = data[str(user_id)]['level']
                
                print('Received message: ' + message.content + ", xp: " + str(random_xp)) # Logging for control

                data = add_or_update_xp(data=data, user_id=user_id, xp_to_add=random_xp)
                save_json(data=data)
                
                new_data = load_json()
                if new_data[str(user_id)]['level'] > current_level:
                    await message.channel.send(f'{message.author.mention} achieved a new level: {new_data[str(user_id)]['level']}')
    
    @slash_command()
    async def level(self, ctx):
        def get_user_level(user_id):
            with open('levels.json', 'r') as file:
                json_file =  json.load(file)
            return json_file[str(user_id)]['level']
        
        
        current_level = get_user_level(ctx.author.id)
        await ctx.respond(f"Your current level is {current_level}!")
        
            
def setup(bot):
    bot.add_cog(LevelSystem(bot))