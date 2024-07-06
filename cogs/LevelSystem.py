from discord.ext import commands
from discord.commands import slash_command
import discord
import ezcord

import json
import random
import math
from easy_pil import Editor, load_image_async, Font

from cogs.Config import Config

class LevelSystem(ezcord.Cog, emoji='✨'):
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
                random_xp = random.randint(5, 20)
                data = load_json()
                user_id = message.author.id
                current_level = data[str(user_id)]['level']
                
                print('Received message: ' + message.content + ", xp: " + str(random_xp)) # Logging for control

                data = add_or_update_xp(data=data, user_id=user_id, xp_to_add=random_xp)
                save_json(data=data)
                
                new_data = load_json()
                if new_data[str(user_id)]['level'] > current_level:
                    new_level = new_data[str(user_id)]['level']
                    await message.channel.send(f'{message.author.mention} achieved a new level: {new_level}')
    
    @slash_command(name='rank', description="Show's the current rank.")
    async def rank(self, ctx):
        def get_user_level(user_id):
            with open('levels.json', 'r') as file:
                json_file =  json.load(file)
            return json_file[str(user_id)]['level']
        
        def get_user_xp(user_id):
            with open('levels.json', 'r') as file:
                json_file = json.load(file)
            return json_file[str(user_id)]['xp']
            
        
        await ctx.defer()
        background = Editor("img/space.png").resize((800, 250))

        avatar = await load_image_async(ctx.author.display_avatar.url)
        circle_avatar = Editor(avatar).resize((200, 200)).circle_image()
        
        background.paste(circle_avatar, (25,25))
        
        current_xp = get_user_xp(ctx.author.id)
        current_level = get_user_level(ctx.author.id)
        
        big_text = Font.poppins(size=50, variant="bold")
        background.text((490, 50), f'{ctx.author.display_name}', color="white", font=big_text, align="center")
        small_text = Font.poppins(size=30, variant='regular')
        background.text(
            (490, 125), f'Level: {current_level} XP: {current_xp}', color="#00ced1", font=small_text, align="center"
        )
        
        
        file = discord.File(fp=background.image_bytes, filename='rank.png')
        
        
        await ctx.followup.send(file=file)
        
    
    
        
def setup(bot):
    bot.add_cog(LevelSystem(bot))