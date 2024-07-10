from discord.commands import slash_command, SlashCommandGroup
import discord
import ezcord
from cogs.AcademyConfig import Config
from cogs.Config import Config as BotConfig
import json
import ast
import io
from contextlib import redirect_stdout

class Academy(ezcord.Cog, hidden=True):
    academy = SlashCommandGroup('academy', description='The Academy is the place where you can learn coding from Zero!')
    lesson = academy.create_subgroup('lesson')
    
    def __init__(self, bot):
        super().__init__(bot)
        self.config = Config('courses.json')

    @academy.command(description="Show's the profile of a user!")
    async def profile(self, ctx):
        user_id_str = str(ctx.user.id)
        courses = self.config.load_config()
        # Initialisiere value standardmäßig
        value = "No courses enrolled"
        # Prüfe, ob die Benutzer-ID in der Konfiguration existiert
        if user_id_str in courses:
            data = courses[user_id_str].get('courses', [])
            
            if 'python' in data:
                level = courses[user_id_str].get('courses')['python']['level']
                
                if level >= 5:
                    value = '<:py_rank_2:1259426955393241192>'
                if level >= 10:
                    value = '<:python:1259196508906197054>'
                if level < 5:
                    value = '<:py_rank_1:1259426957175685170>'
        
        embed = discord.Embed(
            title=f"{ctx.author.display_name}'s profile",
            color=discord.Color.blue()
        )
        embed.add_field(name='Courses', value=value)
        
        await ctx.respond(embed=embed)
    
    @academy.command(description="Gives you a overview over all the courses")
    async def courses(self, ctx):
        
        embed = discord.Embed(
            title='Course Selection',
            description='1. <:python:1259196508906197054> Python',
            color=discord.Color.blue()
        )
        embed.set_footer(text=f'Coding Soul - Course Selection', icon_url=self.bot.user.avatar.url)
        
        await ctx.respond(embed=embed, view=CourseView(self.config), ephemeral=True)
    
    @lesson.command(description="Show's your current lesson.", name='task')
    @discord.option('language', type=discord.SlashCommandOptionType.string)
    async def task(self, ctx, language: str):
        
        user_id_str = str(ctx.user.id)
        courses = self.config.load_config()
        
        # Initialisiere value standardmäßig
        value = "No courses enrolled"
        # Prüfe, ob die Benutzer-ID in der Konfiguration existiert
        if user_id_str in courses:
            data = courses[user_id_str].get('courses', [])
            
            if language in data:
                module = data[language]['module']
                level = data[language]['level']
                print(module)
                print(level)
        
            with open(f'{language}.json', 'r') as f:
                json_data = json.load(f)
            
            task = json_data[f'level-{level}'][f'module-{module}']['task']
            
            embed = discord.Embed(
                title=f'Current lesson | {language}',
                description=f"### Todo: {task}\n\n**Tip:** Prepare the code in your IDE. When you are finished, you enter: /academy lesson send and you'll get an Modal.",
                color=discord.Color.blue()
            )
            embed.set_footer(text=f'Coding Soul - Lesson', icon_url=self.bot.user.avatar.url)
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            await ctx.respond('This course is not enrolled.')
    
    @lesson.command(description="Show's you a modal for entering your code!")
    async def solve(self, ctx):
        
        result = "abc"
        
        await ctx.send_modal(LessonModal(title='Lesson', result=result))
    
def setup(bot):
    bot.add_cog(Academy(bot))

class CourseView(discord.ui.View):
    def __init__(self, config):
        super().__init__()
        self.config = config

    @discord.ui.button(label="Python", style=discord.ButtonStyle.secondary, emoji="<:python:1259196508906197054>")
    async def python_callback(self, button, interaction):
        self.config.add_course_to_user(interaction.user.id, 'python')
        await interaction.response.send_message('Python Course was added to your courses!', ephemeral=True)

class LessonModal(discord.ui.Modal):
    def __init__(self, result, *args, **kwargs):
        super().__init__(
            discord.ui.InputText(
                label=f'Solution',
                placeholder='Print the code out here!',
                style=discord.InputTextStyle.long
            )
            ,*args, **kwargs)
        self.solution = result
        
    async def callback(self, interaction):
        pass