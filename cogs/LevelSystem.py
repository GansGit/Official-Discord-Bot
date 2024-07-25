from discord.ext import commands
from discord.commands import slash_command, option
import discord
import ezcord

import json
import random
import math
from easy_pil import Editor, load_image_async, Font

from cogs.Config import Config


class LevelSystem(ezcord.Cog, emoji='✨'):
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        def xp_to_level(xp, k=100):
            result = math.sqrt(xp / k)

            if result <= 0:
                return 1
            else:
                if result > 1:
                    return math.floor(result)
                else:
                    return 1

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
                data[user_id_str] = {'xp': xp_to_add, 'level': 1}
            return data

        channels = Config.get_config('level-system')['allowed-channels']

        for channel in channels:
            if message.channel.id == channel:
                random_xp = random.randint(5, 20)
                data = load_json()
                user_id = str(message.author.id)
                try:
                    current_level = data[user_id]['level']
                    data = add_or_update_xp(data=data, user_id=user_id, xp_to_add=random_xp)
                    save_json(data=data)

                    new_data = load_json()
                    if new_data[user_id]['level'] > current_level:
                        new_level = new_data[user_id]['level']
                        await message.channel.send(f'{message.author.mention} achieved a new level: {new_level}')
                except Exception:
                    data = add_or_update_xp(data=data, user_id=user_id, xp_to_add=random_xp)
                    save_json(data=data)




    @slash_command(name='rank', description="Show's the current rank.")
    @option("user", description="Pick a user")
    async def rank(self, ctx: discord.ApplicationContext, user: discord.User = None):
        if user is None:
            user = ctx.author

        if user.bot:
            await ctx.respond(f'{user.mention} is a bot.', ephemeral=True)
            return

        def get_user_level(user_id):
            with open('levels.json', 'r') as f:
                json_file = json.load(f)
            return json_file[str(user_id)]['level']

        def get_user_xp(user_id):
            with open('levels.json', 'r') as f:
                json_file = json.load(f)
            return json_file[str(user_id)]['xp']

        await ctx.defer()
        background = Editor("img/space.png").resize((800, 250))

        avatar = await load_image_async(user.display_avatar.url)
        circle_avatar = Editor(avatar).resize((200, 200)).circle_image()

        background.paste(circle_avatar, (25, 25))

        current_xp = get_user_xp(user.id)
        current_level = get_user_level(user.id)

        big_text = Font.poppins(size=50, variant="bold")
        background.text((490, 50), f'{user.display_name}', color="white", font=big_text, align="center")
        small_text = Font.poppins(size=30, variant='regular')
        background.text(
            (490, 125), f'Level: {current_level} XP: {current_xp}', color="#00ced1", font=small_text, align="center"
        )

        file = discord.File(fp=background.image_bytes, filename='rank.png')

        await ctx.followup.send(file=file)


def setup(bot):
    bot.add_cog(LevelSystem(bot))
