import discord
from discord.commands import Option
import os
from cogs.Config import Config
import ezcord

status = discord.Status.online
activity = discord.Activity(type=discord.ActivityType.playing, name="Visual Studio Code", language='en')
loaded_cogs = 0


help_embed = discord.Embed(
    title='☕ Coding Soul・Help',
    description='Get a overview over a couple of commands by choosing a category.',
    color=discord.Color.green()
)

bot = ezcord.Bot(
    intents=discord.Intents.all(),
    debug_guilds=[1254423118315917392],
    status=status,
    activity=activity
)
bot.add_help_command(style=ezcord.HelpStyle.codeblocks, embed=help_embed)


if __name__ == "__main__":
    for filename in os.listdir("cogs"):
        if filename == 'Config.py':
            pass
        elif filename == 'AcademyConfig.py':
            pass
        elif filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")
            loaded_cogs = loaded_cogs + 1
    
    print(f'Sucessfully loaded {loaded_cogs} cogs!')


bot.run(Config.get_config('bot')['token'])